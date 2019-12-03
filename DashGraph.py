import collections
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import networkx as nx
from CreateEdges import *

conns = create_edges(False)

def make_graph(range, user_id, assignment):

    edges = []
    scores = collections.defaultdict(int)
    if user_id == -1 and assignment == '-1':
        for conn in conns:
            if conn[2] <= range[1] and conn[2] >= range[0]:
                edges.append((conn[0], conn[1]))
                scores[(conn[0], conn[1])] = conn[2]
    elif user_id == -1 and assignment != '-1':
        for conn in conns:
            if conn[2] <= range[1] and conn[2] >= range[0]:
                if conn[0] == assignment:
                    edges.append((conn[0], conn[1]))
                    scores[(conn[0], conn[1])] = conn[2]
    elif user_id != -1 and assignment == '-1':
        for conn in conns:
            if conn[1] == user_id:
                if conn[2] <= range[1] and conn[2] >= range[0]:
                    edges.append((conn[0], conn[1]))
                    scores[(conn[0], conn[1])] = conn[2]

    # create graph G
    G = nx.Graph()
    # G.add_nodes_from(node)

    def find_range(score):
        if score <= 60:
            return 0.5
        elif score > 60 and score <= 80:
            return 1.0
        elif score > 80 and score <= 90:
            return 2.0
        else:
            return 3.0

    G.add_edges_from(edges)

    # get a x,y position for each node
    pos = nx.layout.spring_layout(G)

    # add a pos attribute to each node
    for node in G.nodes:
        G.nodes[node]['pos'] = list(pos[node])

    pos=nx.get_node_attributes(G,'pos')

    dmin=1
    ncenter=0
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d

    p=nx.single_source_shortest_path_length(G,ncenter)

    #Create Edges
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']

        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])
        edge_trace['line']['width'] = find_range(scores[edge])
        print(edge, scores[edge], edge_trace['line']['width'])

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='Rainbow',
            reversescale=True,
            color=[],
            size=[],
            colorbar=dict(
                thickness=15,
                title='Number of connected components',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    #add color to node points
    for node, adjacencies in enumerate(G.adjacency()):

        #add size to nodes
        tmp = 10 + len(adjacencies[1])
        # print(node_trace['marker']['size'])
        node_trace['marker']['size'] += tuple([tmp])

        student = str(adjacencies[0])
        if unicode(student, 'utf-8').isnumeric():
            node_trace['marker']['color']+=(15,)
        else:
            node_trace['marker']['color']+=tuple([len(adjacencies[1])])

        node_info = 'Name: ' + str(adjacencies[0]) + '<br># of connections: '+str(len(adjacencies[1]))
        node_trace['text']+=tuple([node_info])

    return (edge_trace, node_trace, len(G.nodes), len(G.edges))

################### START OF DASH APP ###################

app = dash.Dash()

# to add ability to use columns
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

app.layout = html.Div([
                html.Div([
                    dcc.Graph(
                        id='Graph',
                        hoverData = {}
                    ),
                    dcc.RangeSlider(
                        id='my-slider',
                        min=50, max=100, value=[50,60],
                        step=None,
                        marks={50: '50', 60: '60', 70: '70', 80: '80', 90: '90', 100: '100'} # edit here
                    ),
                ], style={'width': '49%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(id='single-student-graph'),
                    dcc.RadioItems(
                        options = [
                            {'label': 'User Network', 'value': 'UN'},
                            {'label': 'User Bar Graph', 'value': 'UBG'}
                        ],
                        value = 'UN'
                    )
                ], style={'display': 'inline-block', 'width': '49%'}),


                html.Div(className='row', children=[

                    html.Div([html.H3('Overall Data'),
                              html.P('Number of nodes: ' + '', id='num_nodes'),
                              html.P('Number of edges: ' + '', id='num_edges')],
                              className='three columns'),

                    html.Div([
                            html.H3('Add Nodes'),
                            dcc.Input(id='input-box', type='text'),
                            html.Button('Add Connection', id='add-button'),
                        ], className='three columns'),

                    html.Div([
                    		html.H3('Select Nodes'),
                    		dcc.Dropdown(
                    			id='check',
                    			options=[
                    				{'label': 'A1', 'value': 'A1'},
                    				{'label': 'A2', 'value': 'A2'},
                    				{'label': 'A3', 'value': 'A3'},
                    				{'label': 'B1', 'value': 'B1'},
                    				{'label': 'B2', 'value': 'B2'},
                    				{'label': 'B3', 'value': 'B3'},
                    				{'label': 'C1', 'value': 'C1'},
                    				{'label': 'C2', 'value': 'C2'},
                    				{'label': 'C3', 'value': 'C3'}
                    			],
                    			value = [],
                    			multi=True),
                    		html.Button('Select All', id='select-all')
                    			],className='three columns'),

                    html.Div([
                    		html.H3('Update'),
                    		html.Button('Refresh graph', id='update-graph'),
                    		html.Button('Refresh data', id='pull-canvas')
                    ], className='three columns')

                    ])
                ])

@app.callback(
	dash.dependencies.Output('check', 'options'),
	[dash.dependencies.Input('add-button', 'n_clicks')],
	[dash.dependencies.State('input-box', 'value'), dash.dependencies.State('check', 'options')])
def update_options(n_clicks, new_value, current_options):
	if not n_clicks:
		return current_options
	current_options.append({'label': new_value, 'value': new_value})
	return current_options

@app.callback(
    [dash.dependencies.Output('Graph', "figure"),
    dash.dependencies.Output('num_nodes', "children"),
    dash.dependencies.Output('num_edges', "children")],
    [dash.dependencies.Input('my-slider', "value")])
def update_graph(n):
    et, nt, nodes, edges = make_graph(n, -1, '-1')
    fig = go.Figure(data=[et, nt],
                 layout=go.Layout(
                    title='<b>{}</b><br>'.format('Systems Curriculum'),
                    titlefont=dict(size=36),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=60),
                    annotations=[ dict(
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    return fig, 'Num of Nodes: ' + str(nodes), 'Num of Edges: ' + str(edges)

@app.callback(
    dash.dependencies.Output('check', 'value'),
    [dash.dependencies.Input('select-all', 'n_clicks')],
    [dash.dependencies.State('check', 'options')])
def update_selections(n_clicks, current_options):
    new_value = []
    for elem in current_options:
        new_value.append(elem['value'])
    return new_value

@app.callback(
    dash.dependencies.Output('single-student-graph', 'figure'),
    [dash.dependencies.Input('Graph', 'hoverData'),
    dash.dependencies.Input('my-slider', "value")])
def update_single_student_graph(hoverData, n):
    print('Hover Data: {}'.format(hoverData))
    print('n: {}'.format(n))
    flag = False
    user_id = -1
    assignment = '-1'
    try:
        sep = '#'
        rest = hoverData['points'][0]['text'].split(sep, 1)[0]
        sep = ": "
        user_id = int(rest.split(sep, 1)[1][:-4])
        flag = True
    except ValueError:
        print('Error: This is not a Student Node')
    except KeyError:
        print('Error: Could not locate dictionary key')

    if not flag:
        try:
            sep = '#'
            rest = hoverData['points'][0]['text'].split(sep, 1)[0]
            sep = ": "
            assignment = rest.split(sep, 1)[1][: -4]
        except ValueError:
            print('Error: This is not an Assignment Node')
        except KeyError:
            print('Error: Could not locate dictionary key')

    et, nt, nodes, edges = make_graph(n, user_id, assignment)
    fig = go.Figure(data=[et, nt],
                 layout=go.Layout(
                    title='<b>User ID: {}</b><br>'.format(user_id),
                    titlefont=dict(size=36),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=60),
                    annotations=[ dict(
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
