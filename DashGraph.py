import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import networkx as nx

from CreateEdges import *

def make_graph(n):
    edges = create_edges(False, n)

    # create graph G
    G = nx.Graph()
    # G.add_nodes_from(node)
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
            colorscale='Hot',
            reversescale=True,
            color=[],
            size=[],
            colorbar=dict(
                thickness=15,
                title='Node Connections',
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
				html.Div(),
                html.Div(dcc.Graph(id='Graph', )),

                html.Div([
                        dcc.Slider(
                            id='my-slider',
                            min=50, max=100, value=50,
                            marks={50: '50', 60: '60', 70: '70', 80: '80', 90: '90', 100: '100'}
                        ),
                        html.Div(id='slider-output-container')
                    ], className='submit area'),


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
    et, nt, nodes, edges = make_graph(n)
    fig = go.Figure(data=[et, nt],
                 layout=go.Layout(
                    title='<b>Systems Curriculum</b><br>',
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

# @app.callback(
# 	dash.dependencies.Output('Graph', 'figure'),
# 	[dash.dependencies.Input('update-graph', 'n_clicks_timestamp'),
# 	dash.dependencies.Input('pull-canvas', 'n_clicks_timestamp')])
# def update_graph(n_clicks1, n_clicks2):
#
# 	if n_clicks1 is None:
# 		print('data update')
# 		return fig
# 	elif n_clicks2 is None:
# 		print('graph update')
# 		return fig
# 	elif int(n_clicks1) > int(n_clicks2):
# 		print('graph update')
# 	else:
# 		print('data update')
#
# 	return fig

if __name__ == '__main__':
    app.run_server(debug=True)
