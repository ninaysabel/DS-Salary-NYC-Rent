############################################################################################
###################################### Import Dependencies #################################
############################################################################################
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import shapely 
import fiona
from shapely.geometry import Point
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px

df = pd.read_csv('data_nyc.csv', low_memory=False)

#############################################################################################
###################################### Initialize App #######################################
#############################################################################################
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=stylesheets)
server = app.server

#############################################################################################
###################################### App Layout ###########################################
#############################################################################################
neighbourhood_group = df['neighbourhood_group'].unique().tolist()
fig = px.bar(df, x='neighbourhood_group', y='amenity_value', color='amenity',
             title='Frequency of Amenities in Different Neighborhoods',
             labels={'neighbourhood_group': 'Neighborhood', 'amenity_value': 'Frequency', 'amenity': 'Amenity'})

app.layout = html.Div([
    # Top blue bar
    html.Div(style={'background-color': '#aecdcf', 'color': 'white', 'padding': '10px'}),
    html.Div([
        html.Div(className='navbar', style={'text-align': 'center'}, children=[
            html.H1('Data Science Salary x NYC Rent', className='navbar-title', style={'color': '#5d99c2'})
        ]),
    ]),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            html.H4("Expected Rent", style={'color': '#5d99c2'}),
            dcc.RangeSlider(
                id='rent-range-slider',
                min=df['rent'].min(),
                max=df['rent'].max(),
                step=2000,
                marks={i: f'${i}' for i in range(int(df['rent'].min()), int(df['rent'].max())+1, 2000)},
                value=[df['rent'].min(), df['rent'].max()]
            ),
            html.Div(id='output-container-range-slider')
        ]),
        html.Div(className='six columns', children=[
            html.H4("Desired Neighborhood", style={'color': '#5d99c2'}),
            dcc.Dropdown(
                id='neighborhood-group-selector',
                options=[{'label': group, 'value': group} for group in neighbourhood_group],
                multi=True,
                placeholder="Select your desired neighborhood!",
                className='neighborhood-group-dropdown'
            )
        ])
    ]),
    html.Div(className='row', style={'position': 'relative', 'z-index': '1'}, children=[
        html.Div(className='six columns', children=[
            html.H4("Desired Amenities", style={'color': '#5d99c2'}),
            dcc.Dropdown(
                id='amenity-selector',
                options=[{'label': amenity, 'value': amenity} for amenity in df['amenity'].unique()],
                multi=True,
                placeholder="Select your desired amenities!",
                className='amenity-dropdown'
            )
        ])
    ]),
     html.Div(className='row', style= {'z-index': '2'}, children=[
        html.Div(className='six columns', children=[
            dcc.Graph(id='salary-graph')
        ])
    ]),
    # Colored overlay
    html.Div(style={'position': 'absolute', 'top': '100px', 'left': '0', 'width': '100%', 'height': '800px', 'background-color': '#aecdcf', 'z-index': '-1'})
    
])

##############################################################################################
####################################### Callbacks ############################################
##############################################################################################
@app.callback(
    Output('salary-graph', 'figure'),
    [Input('rent-range-slider', 'value'),
     Input('amenity-selector', 'value')]
)
def update_graph(rent_range, selected_amenities):
    filtered_df = df[(df['rent'] >= rent_range[0]) & (df['rent'] <= rent_range[1])]
    if selected_amenities:
        filtered_df = filtered_df[filtered_df['amenity'].isin(selected_amenities)]
    
    fig = px.scatter(filtered_df, x='rent', y='salary_in_usd', color='amenity',
                     title='Salary vs Rent with Selected Amenities')
    
    return fig
##############################################################################################
####################################### Run App ##############################################
##############################################################################################
if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
