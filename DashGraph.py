import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import networkx as nx

from CreateEdges import *

edges = []
edges2 = []
dictE = {}
edges, edges2 = create_edges(False)

graphData = []

#convert edges2 to dictionary for searching grades
for edge in edges2:
    dictE[tuple([edge[0], edge[1]])] = float(edge[2]) / float(edge[3]) * 100
    dictE[tuple([edge[1], edge[0]])] = float(edge[2]) / float(edge[3]) * 100

#create graph G
G = nx.Graph()
#G.add_nodes_from(node)
G.add_edges_from(edges)
#get a x,y position for each node
pos = nx.layout.spring_layout(G)

#add a pos attribute to each node
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

#--------------------------------------------------------
# edges
#--------------------------------------------------------
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
                       line=dict(width=width,color='#888'),
                       hoverinfo='none',
                       mode='lines')


for edge in G.edges():
    x0, y0 = G.node[edge[0]]['pos']
    x1, y1 = G.node[edge[1]]['pos']
    #edge_trace.append(make_edge(tuple([x0, x1, None]), tuple([y0, y1, None]), 0.05*int(dictE[edge])))
    #calculate a range for
    #print("grades",dictE[edge])
    ranges = {0.02 : [0,91], 0.1: [92,94], 1 : [95, 97], 3: [98,101]}
    gra = next((key for key, (low, high) in ranges.items() if low <= dictE[edge] <= high), 10)
    graphData.append(make_edge(tuple([x0, x1, None]), tuple([y0, y1, None]), gra))

#--------------------------------------------------------
# nodes
#--------------------------------------------------------
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
    print(node_trace['marker']['size'])
    node_trace['marker']['size'] += tuple([tmp])
    
    student = str(adjacencies[0])
    if student.isnumeric():
        node_trace['marker']['color']+=(15,)
    else:
        node_trace['marker']['color']+=tuple([len(adjacencies[1])])
    
    node_info = 'Name: ' + str(adjacencies[0]) + '<br># of connections: '+str(len(adjacencies[1]))
    node_trace['text']+=tuple([node_info])

graphData.append(node_trace)
################### START OF DASH APP ###################

app = dash.Dash()

# to add ability to use columns
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

fig = go.Figure(data=graphData,
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

app.layout = html.Div([
				html.Div(),
                html.Div(dcc.Graph(id='Graph',figure=fig)),
                
                html.Div([
                        dcc.Slider(
                            id='my-slider',
                            min=50, max=100, value=50,
                            marks={'50': '50', '60': '60', '70': '70', '80': '80', '90': '90', '100': '100'}
                        ),
                        html.Div(id='slider-output-container')
                    ], className='submit area'),
                    
                    
                html.Div(className='row', children=[
                
                    html.Div([html.H3('Overall Data'),
                              html.P('Number of nodes: ' + str(len(G.nodes))),
                              html.P('Number of edges: ' + str(len(G.edges)))],
                              className='three columns'),
                              
                    html.Div([
                            html.H3('Add Connections'),
                            dcc.Input(id='input-box', type='text'),
                            html.Button('Add Connection', id='add-button'),
                        ], className='three columns'),
                        
                    html.Div([
                    		html.H3('Select Connections'),
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
def update_output(n_clicks, new_value, current_options):
	if not n_clicks:
		return current_options
	current_options.append({'label': new_value, 'value': new_value})
	return current_options

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_output(value):
    # print(value)
    return 'You have selected "{}"'.format(value)
    
@app.callback(
    dash.dependencies.Output('check', 'value'),
    [dash.dependencies.Input('select-all', 'n_clicks')],
    [dash.dependencies.State('check', 'options')])
def update_value(n_clicks, current_options):

    new_value = []
    for elem in current_options:
        new_value.append(elem['value'])
    
    return new_value

if __name__ == '__main__':
    app.run_server(debug=True)
