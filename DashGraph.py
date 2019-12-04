import collections
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import networkx as nx
from CreateEdges import *

conns = create_edges(False)
graphData = []
studentInfo = {}

for edge in conns:
    studentInfo[edge[1]] = edge[3]

def make_graph(range, user_id, assignment):

    graphdatafun = []
    edges = []
    scores = collections.defaultdict(int)

    if user_id == -1 and assignment == '-1':
        for conn in conns:
            if conn[2] <= range[1] and conn[2] >= range[0]:
                edges.append((conn[0], conn[1]))
                scores[(conn[0], conn[1])] = conn[2]
                scores[(conn[1], conn[0])] = conn[2]
    elif user_id == -1 and assignment != '-1':
        for conn in conns:
            if conn[2] <= range[1] and conn[2] >= range[0]:
                if conn[0] == assignment:
                    edges.append((conn[0], conn[1]))
                    scores[(conn[0], conn[1])] = conn[2]
                    scores[(conn[1], conn[0])] = conn[2]
    elif user_id != -1 and assignment == '-1':
        for conn in conns:
            if conn[1] == user_id:
                if conn[2] <= range[1] and conn[2] >= range[0]:
                    edges.append((conn[0], conn[1]))
                    scores[(conn[0], conn[1])] = conn[2]
                    scores[(conn[1], conn[0])] = conn[2]

    # create graph G
    G = nx.Graph()
    # G.add_nodes_from(node)

    #def find_range(score):
    #    if score <= 60:
    #        return 0.5
    #    elif score > 60 and score <= 80:
    #        return 1.0
    #    elif score > 80 and score <= 90:
    #        return 2.0
    #    else:
    #        return 3.0

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
    #Create Edges
    def make_edge(x, y, width):
        """
            Args:
            x: a tuple of the x from and to, in the form: tuple([x0, x1, None])
            y: a tuple of the y from and to, in the form: tuple([y0, y1, None])
            width: The width of the line

            Returns:
            a Scatter plot which represents a line between the two points given.
            """
        return  go.Scatter(
                           x=x,
                           y=y,
                           line=dict(width=width,color='#000000'),
                           hoverinfo='none',
                           mode='lines')

        #edge_trace = go.Scatter(
        #x=[],
        #y=[],
        #line=dict(width=0.5,color='#888'),
        #hoverinfo='none',
        #mode='lines')


    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        #edge_trace.append(make_edge(tuple([x0, x1, None]), tuple([y0, y1, None]), 0.05*int(dictE[edge])))
        #calculate a range for
        #print("grades",dictE[edge])
        #ranges = {0.021231 : [50,51], 0.111: [52,54], 1.01123 : [55, 57], 3.101: [58,60],
        #          0.02123 : [60,61], 0.11: [62,64], 1.0123 : [65, 67], 3.01: [68,70],
        #          0.0212 : [70,71], 0.112: [72,74], 1.012 : [75, 77], 3.02: [78,80],
        #          0.021 : [80,81], 0.1123: [82,84], 1.01 : [85, 87], 3.03: [88,90],
        #          0.02 : [90,91], 0.1: [92,94], 1 : [95, 97], 3: [98,101]}

        ranges = {0.1 : [0,54], 0.5 : [55, 60],
                  0.9 : [61,64], 1.3 : [65,70],
                  1.7 : [71,74], 2.1 : [75,80],
                  2.5 : [81,84], 2.9 : [85,90],
                  3.3 : [91,94], 3.7 : [95,101]}
        print("edge = ",edge, scores[edge])
        gra = next((key for key, (low, high) in ranges.items() if low <= scores[edge] <= high), 0.5)
        print("weights = ", gra)
        graphdatafun.append(make_edge(tuple([x0, x1, None]), tuple([y0, y1, None]), gra))

    #for edge in G.edges():
    #    x0, y0 = G.node[edge[0]]['pos']
    #    x1, y1 = G.node[edge[1]]['pos']

    #    edge_trace['x'] += tuple([x0, x1, None])
    #    edge_trace['y'] += tuple([y0, y1, None])
    #    edge_trace['line']['width'] = find_range(scores[edge])
    #    print(edge, scores[edge], edge_trace['line']['width'])

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
        if student.isnumeric():
            node_trace['marker']['color']+=(15,)
        else:
            node_trace['marker']['color']+=tuple([len(adjacencies[1])])

        tp = str(adjacencies[0])

        if tp.isnumeric():
            #print(tp)
            node_info = 'Id: ' + str(adjacencies[0]) + ':<br>Name: ' + studentInfo[int(tp)] + '<br># of connections: '+str(len(adjacencies[1]))
        else:
            node_info = 'Name: ' + str(adjacencies[0]) + '<br># of connections: '+str(len(adjacencies[1]))

        #node_info = 'Name: ' + str(adjacencies[0]) + '<br># of connections: '+str(len(adjacencies[1]))
        node_trace['text']+=tuple([node_info])

    graphdatafun.append(node_trace)

    return (graphdatafun, len(G.nodes), len(G.edges))

################### START OF DASH APP ###################

app = dash.Dash()
server = app.server

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
    global graphData
    graphData, nodes, edges = make_graph(n, -1, '-1')
    fig = go.Figure(data=graphData,
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
    global graphData
    print('Hover Data: {}'.format(hoverData))
    print('n: {}'.format(n))
    flag = False
    user_id = -1
    assignment = '-1'
    try:
        sep = '#'
        rest = hoverData['points'][0]['text'].split(sep, 1)[0]
        print(rest + 'rest end')
        sep = ":"
        print(rest.split(":",2)[1])
        user_id = int(rest.split(sep, 2)[1])
        flag = True
    except ValueError:
        print('Error: This is not a Student Node')
    except KeyError:
        print('Error: Could not locate dictionary key')

    #Not flag = Assignment Node
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


    graphData, nodes, edges = make_graph(n, user_id, assignment)
    fig = go.Figure(data=graphData,
                 layout=go.Layout(
                    title='<b>User: {}</b><br>'.format(studentInfo[user_id]),
                    titlefont=dict(size=24),
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
