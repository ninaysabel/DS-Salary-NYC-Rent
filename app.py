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
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('data_nyc.csv', low_memory=False)
df = df[df['rent'] < 7000] #98.3% of data have rent values less than 7000

#############################################################################################
###################################### Initialize App #######################################
#############################################################################################
# Initialize app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Define neighborhood group variable
neighbourhood_group = df['neighbourhood_group'].unique().tolist()

# Define the pie chart figure
pie_fig = px.pie(df, names='job_category', title='Job Categories Distribution')

# Set up Geopandas
gdf = gpd.GeoDataFrame(df, 
                        geometry=gpd.points_from_xy(df.longitude, df.latitude))

nyc_shapefile = 'geo_export_d02ff8e6-e0b7-41a7-90a4-bfbded2003ee.shx'
newcity = gpd.read_file(nyc_shapefile)

# Set color scale for radio buttons
color_scales = {
    'Original': 'Original',
    'Colorblind Friendly': 'white-blue'
}
#############################################################################################
######################################   App Layout   #######################################
#############################################################################################
app.layout= html.Div(children=[ 
    html.Div([
    # TOP BLUE BAR
        html.Div([
            html.Div(className='six columns', children=[
            ])
        ], style={'background-color': '#bdd8db', 'padding': '52px', 'z-index': '0'}),
        html.Div([
            html.Div(children=[
                html.H1('Welcome to New York City!', className='navbar-title', style={'color': 'black', 'font-size': '54px', 'position': 'relative', 'z-index': '2','fontFamily': 'Times New Roman'})
            ])
        ], style={'position': 'absolute', 'top': '20px', 'width': '100%', 'text-align': 'center', 'z-index': '2', 'border-radius': '15px'}),
    # SKYLINE
        html.Div([
            html.Img(src=app.get_asset_url('skyline.png'),
                    style={'position': 'fixed', 'top': 24, 'left': 8, 'width': '12%', 'height': '100px', 'z-index': '0', 'opacity': '0.6'}),
            html.Img(src=app.get_asset_url('skyline.png'),
                    style={'position': 'fixed', 'top': 24, 'left': '12.5%', 'width': '12.5%', 'height': '100px', 'z-index': '0', 'opacity': '0.6'}),
            html.Img(src=app.get_asset_url('skyline.png'),
                    style={'position': 'fixed', 'top': 24, 'left': '25%', 'width': '12.5%', 'height': '100px', 'z-index': '0', 'opacity': '0.6'}),
            html.Img(src=app.get_asset_url('skyline.png'),
                    style={'position': 'fixed', 'top': 24, 'left': '37.5%', 'width': '12.5%', 'height': '100px', 'z-index': '0', 'opacity': '0.6'}),
            html.Img(src=app.get_asset_url('skyline.png'),
                    style={'position': 'fixed', 'top': 24, 'left': '50%', 'width': '12.5%', 'height': '100px', 'z-index': '0', 'opacity': '0.6'}),
            html.Img(src=app.get_asset_url('skyline.png'),
                    style={'position': 'fixed', 'top': 24, 'left': '62.5%', 'width': '12.5%', 'height': '100px', 'z-index': '0', 'opacity': '0.6'}),
            html.Img(src=app.get_asset_url('skyline.png'),
                    style={'position': 'fixed', 'top': 24, 'left': '75%', 'width': '12.5%', 'height': '100px', 'z-index': '0', 'opacity': '0.6'}),
            html.Img(src=app.get_asset_url('skyline.png'),
                    style={'position': 'fixed', 'top': 24, 'left': '87.5%', 'width': '12%', 'height': '100px', 'z-index': '0', 'opacity': '0.6'}),        
        ], style={ 'z-index': '1'}),
    ]),
    # RECTANGLE LEFT UPPER
    html.Div(className='row', children=[
        html.Div([
            html.H3("Welcome to the Big Apple, fellow data scientist!", style={'color': 'black', 'padding': '5px', 'margin-bottom': '0','text-align': 'center','fontFamily': 'Times New Roman'}),
            html.H6("We understand that the NYC apartment hunt can be really difficult, so we created this so you can get a head start.", style={'color': 'black', 'padding': '5px 20px', 'font-weight': 'normal', 'margin-top': '0','fontFamily': 'Times New Roman'}),
        ], style={'position': 'fixed', 'top': '135px', 'left': '0.5%', 'width': '33%', 'height': '220px', 'background-color': '#d4d2d2', 'border-radius': '15px'}),
    ]),
    # RECTANGLE LEFT LOWER
    html.Div(className='row', children=[
        html.Div([
            html.H4("Please select your preferences.", style={'color': '#5d99c2', 'padding': '0px', 'margin-bottom': '10px', 'text-align': 'center','fontFamily': 'Times New Roman'}),
            # NEIGHBORHOOD DROPDOWN
            html.Div(className='row', children=[
                html.Div(className='six columns', children=[
                    html.Img(src=app.get_asset_url('home-icon-transparent-free-png.png'),
                            style={'width':'30px', 'height': '30px'}),
                    html.H4("Desired Neighborhood", style={'color': 'black', 'font-size': '18px', 'margin-left': '3px','fontFamily': 'Times New Roman'}),
                ], style={'width': '100%','margin-left': '3%','display': 'flex', 'align-items': 'center'}),  # Adjust the width here
            ]),
            html.Div(className='row', children=[
                html.Div(className='six columns', children=[
                    dcc.Dropdown(
                        id='neighborhood-group-selector',
                        options=[{'label': group, 'value': group} for group in neighbourhood_group],
                        multi=True,
                        placeholder="Select your desired neighborhood!",
                        className='neighborhood-group-dropdown'
                    )
                ], style={'width':'83%', 'margin-left': '6%', 'margin-bottom': '15px'}),
            ]),
            # RENT SLIDER
            html.Div(className='six columns', children=[
                html.Img(src=app.get_asset_url('money-39.png'),
                         style={'width':'22px', 'height':'22px'}),
                html.H4("Expected Rent", style={'color': 'black', 'font-size': '19px', 'margin-left': '10px','fontFamily': 'Times New Roman'}),
            ], style={'width': '100%','display': 'flex', 'align-items': 'center'}),  # Adjust the width here
            html.Div(className='six columns', children=[
                dcc.RangeSlider(
                    id='rent-range-slider',
                    min=df['rent'].min(),
                    max=df['rent'].max(),
                    step=750,
                    marks={i: f'${i}' for i in range(int(df['rent'].min()), int(df['rent'].max()) + 1, 750)},
                    value=[df['rent'].min(), df['rent'].max()]
                ),
            ], style={'width': '90%','display': 'inline-block', 'vertical-align': 'middle', 'margin-bottom': '15px'}),
            # AMENITIES DROPDOWN
            html.Div(className='row', children=[
                html.Div(className='six columns', children=[
                    html.Img(src=app.get_asset_url('3832100.png'),
                             style={'width':'26px', 'height':'24px'}),
                    html.H4("Desired Amenities", style={'color': 'black', 'font-size': '20px', 'margin-left': '8px','fontFamily': 'Times New Roman'}),
                ], style={'width': '100%','margin-left': '3%','display': 'flex', 'align-items': 'center'}),
            ]),
            html.Div(className='row', children=[
                html.Div(className='six columns', children=[
                    dcc.Dropdown(
                    id='amenity-selector',
                    options=[{'label': amenity, 'value': amenity} for amenity in df['amenity'].unique()],
                    multi=True,
                    placeholder="Select your desired amenities!",
                    className='amenity-dropdown'
                )
                ], style={'width':'83%', 'margin-left': '6%'})
            ]),
        ], style={'position': 'fixed', 'top': '365px', 'left': '0.5%', 'width': '33%', 'height': '440px',
                  'background-color': '#bdd8db', 'border-radius': '15px'}),
    ]),
    # RECTANGLE MIDDLE
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            html.Div([
                html.H4("Your Available Apartments!", style={'color': "white", 'padding': '8px','margin-top':'42px', 'display': 'inline-block', 'margin-left':'70px', 'text-align': 'center','fontFamily': 'Times New Roman'}),
                html.Img(src=app.get_asset_url('pngegg.png'),
                        style={'height': '40px', 'margin-right': '0px', 'vertical-align': 'middle', 'left': '30%', 'display': 'inline-block'}),
            ], style={'position': 'absolute', 'width': '100%', 'top': '-25px', 'left': '0', 'z-index': '1', 'margin-left': '0px'}),
            html.Br(style={'height': '50px'}),
            dcc.Graph(id='map',
                    style={'width': '90%', 'margin-left': '5%', 'z-index': '1', 'margin-top': '70px', 'border-radius': '15px'}),
            dcc.RadioItems(
                id='colorscale-radio',
                options=[{'label': k, 'value': k} for k in color_scales.keys()],
                value='Original',
                labelStyle={'display': 'inline-block'},
                style={'text-align': 'center', 'margin-top': '20px','fontFamily': 'Times New Roman'}
            ),
        ], style={'position': 'fixed', 'top': '135px', 'left': '35%', 'width': '35%', 'height': '670px',
            'background-color': '#5d99c2', 'overflow': 'hidden', 'z-index': '1', 'border-radius': '15px'}),
    ]),
    #RECTANGLE RIGHT
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            html.Div(style={'position': 'absolute', 'top': '11px', 'left': '%', 'width': '182px', 'height': '182px', 'border-radius': '50%', 'background-color': '#5d99c2'}),
            dcc.Graph(
                id="neighborhood-pie-chart"
            ),
        ], style={'position': 'fixed', 'top': '135px', 'left': '71%', 'width': '28.5%', 'height': '200px',
                'background-color': '#d4d2d2', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-right': '25px', 'border-radius': '15px'}),
    ]),
    # RECTANGLE RIGHT LOWER
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            html.H4("Your Amenities, Visualized", style={'color': "#5d99c2", 'padding': '10px', 'margin-bottom': '0',
                                                'text-align': 'center','fontFamily': 'Times New Roman'}),
            html.Br(),
            dcc.Graph(
                id='salary-graph',
                style={ 'height': '260px', 'width': '88%', 'margin-left': '5%', 'margin-top': '-20px'},  # Adjust the width of the graph
            ),
        ], style={'position': 'fixed', 'top': '350px', 'left': '71%', 'width': '28.5%', 'height': '365px',
                  'background-color': '#bdd8db', 'border-radius': '15px'}),
    ]),
    #RECTANGLE RIGHT LOWEST
    html.Div(className='row', children=[
    html.Div(className='twelve columns', children=[
        html.Div(style={'position': 'fixed', 'top': '726px', 'left': '71%', 'width': '28.5%', 'height': '77px', 'background-color': '#d4d2d2', 'border-radius': '15px', 'display': 'flex', 'align-items': 'center'}),
        html.Div([
            html.A(
                html.Img(
                    src=app.get_asset_url('25231.png'),
                    style={'width': '20px', 'height': '20px', 'vertical-align': 'middle'}
                ),
                href='https://github.com/ninaysabel/DS-Salary-NYC-Rent',
                target='_blank',
                style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '40px', 'margin-right': '10px'}
            ),
            html.P("Nina Ysabel Alinsonorin", style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '10px', 'color': 'black','fontFamily': 'Times New Roman'})
        ], style={'position': 'absolute', 'top': '726px', 'left': '75%', 'width': '20%', 'height': '77px', 'display': 'flex', 'align-items': 'center'}),
    ])
])

])

#############################################################################################
###################################### Callbacks     #######################################
#############################################################################################
# AMENITIES CALLBACK
@app.callback(
    Output('salary-graph', 'figure'),
    [Input('rent-range-slider', 'value'),
     Input('amenity-selector', 'value')]
)
def update_graph(rent_range, selected_amenities):
    filtered_df = df[(df['rent'] >= rent_range[0]) & (df['rent'] <= rent_range[1])]
    if selected_amenities:
        filtered_df = filtered_df[filtered_df['amenity'].isin(selected_amenities)]

    fig = px.scatter(filtered_df, x='rent', y='salary_in_usd', color='amenity')

    fig.update_layout(legend=dict(font=dict(size=10)))  # Adjust the font size as needed
    fig.update_layout(margin=dict(t=3, b=4))

    fig.update_layout(xaxis_title='Rent', yaxis_title='Salary',
                      xaxis_title_font=dict(size=15), yaxis_title_font=dict(size=15))
    
    fig.update_layout(plot_bgcolor='#bdd8db')

    return fig

# PIE CHART CALL BACK
@app.callback(
    Output('neighborhood-pie-chart', 'figure'),
    [Input('neighborhood-group-selector', 'value')]
)
def update_pie_chart(selected_neighborhoods):
    if selected_neighborhoods:
        filtered_df = df[df['neighbourhood_group'].isin(selected_neighborhoods)]  # Update column name here
        fig = px.pie(filtered_df, values='rent', names='neighbourhood_group')
        fig.update_traces(textposition='inside', textinfo='percent+label', hole=0.6)  # Set hole=0.6 for a circular progress bar effect
        fig.update_layout(autosize=False, width=150, height=150)  # Set fixed width and height for a circular chart
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),  # Remove margin to fit the chart within the block
            paper_bgcolor='rgba(0,0,0,0)',  # Set background color to transparent
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False  
        )
        return fig
    else:
        fig = px.pie(df, values='rent', names='neighbourhood_group')
        fig.update_traces(textposition='inside', textinfo='percent+label', hole=0.5)  # Set hole=0.6 for a circular progress bar effect
        fig.update_layout(autosize=False, width=155, height=155)  # Set fixed width and height for a circular chart
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),  # Remove margin to fit the chart within the block
            paper_bgcolor='rgba(0,0,0,0)',  # Set background color to transparent
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False  
        )
        return fig

# MAP CALLBACK
@app.callback(
    Output('map', 'figure'),
    [Input('rent-range-slider', 'value'),
     Input('neighborhood-group-selector', 'value'),
     Input('amenity-selector', 'value'),
     Input('colorscale-radio', 'value')]  
)
def update_map(rent_range, selected_neighborhoods, selected_amenities, colorscale):
    # Define the color scales
    color_scales = {
        'Original': 'RdPu',  # Red hue color scale
        'Colorblind Friendly': 'blues',  # Blue color scale
    }

    # Filter the DataFrame based on selected rent, neighborhoods, and amenities
    filtered_df = df[(df['rent'] >= rent_range[0]) & (df['rent'] <= rent_range[1])]
    if selected_neighborhoods:
        filtered_df = filtered_df[filtered_df['neighbourhood_group'].isin(selected_neighborhoods)]
    if selected_amenities:
        filtered_df = filtered_df[filtered_df['amenity'].isin(selected_amenities)]
    
    # Create a GeoDataFrame from the filtered data
    gdf = gpd.GeoDataFrame(filtered_df, geometry=gpd.points_from_xy(filtered_df['longitude'], filtered_df['latitude']))
    
    # Create the map
    fig = px.scatter_mapbox(gdf, lat='latitude', lon='longitude', color='rent', size_max=3,
                            mapbox_style="carto-positron", zoom=10, color_continuous_scale=color_scales[colorscale])
    
    # Add the shapefile to the map
    fig.update_layout(mapbox_style="carto-positron")
    fig.add_trace(px.choropleth_mapbox(gdf, geojson=newcity.geometry.__geo_interface__, 
                                       locations=gdf.index, color=gdf['rent'],
                                       featureidkey="properties.name").data[0])
    # Update layout
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      paper_bgcolor= '#e9edf0')
    
    return fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True, port=8059)
