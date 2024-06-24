from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from src.dash1 import generate_visualizations as generate_visualizations1
from src.dash2 import generate_visualizations as generate_visualizations2
from src.dash3 import generate_visualizations as generate_visualizations3
from src.dash4 import generate_visualizations as generate_visualizations4

movies = pd.read_csv('./movie_after_cleaning.csv')
movies_splits = pd.read_excel("./splits_movie.xlsx", sheet_name=None)
series = pd.read_csv('./series_after_cleaning.csv')
series_splits = pd.read_excel("./splits_series.xlsx", sheet_name=None)
dO = pd.read_csv('./Ofile.out.csv', sep=";")
dR = pd.read_csv('./Rfile.out.csv', sep=";")
VO = pd.read_csv('./Ofile.veh.csv', sep=";")
VR = pd.read_csv('./Rfile.veh.csv', sep=";")
traffic = ''

# Define function to load data based on tab selection
def load_data(tab):
    if tab == 'movie':
        return movies, movies_splits
    elif tab == 'series':
        return series, series_splits

#num_of_works,num_of_countries,num_of_lang,avg_votes = get_constants(movies, series, movies_splits, series_splits)


# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title='TULIPE - Traffic management')
server = app.server

def generate_stats_card (title, value, image_path):
    return html.Div(
        dbc.Card([
            dbc.CardImg(src=image_path, top=True, style={'width': '50px','alignSelf': 'center'}),
            dbc.CardBody([
                html.P(value, className="card-value", style={'margin': '0px','fontSize': '22px','fontWeight': 'bold'}),
                html.H4(title, className="card-title", style={'margin': '0px','fontSize': '18px','fontWeight': 'bold'})
            ], style={'textAlign': 'center'}),
        ], style={'paddingBlock':'10px',"backgroundColor":'#deb522','border':'none','borderRadius':'10px'})
    )


tab_style = {
    'idle':{
        'borderRadius': '10px',
        'padding': '0px',
        'marginInline': '5px',
        'display':'flex',
        'alignItems':'center',
        'justifyContent':'center',
        'fontWeight': 'bold',
        'backgroundColor': '#deb522',
        'border':'none'
    },
    'active':{
        'borderRadius': '10px',
        'padding': '0px',
        'marginInline': '5px',
        'display':'flex',
        'alignItems':'center',
        'justifyContent':'center',
        'fontWeight': 'bold',
        'border':'none',
        'textDecoration': 'underline',
        'backgroundColor': '#deb522'
    }
}

MAX_OPTIONS_DISPLAY = 3300

# Generate options for the dropdown
dropdown_options = [{'label': title, 'value': title} for title in ['traveltime', 'density','occupancy', 'timeLoss', 'waitingTime', 'speed', 'speedRelative', 'sampledSeconds']]
dropdown_options_vehicles = [{'label': title, 'value': title} for title in ['duration', 'routeLength', 'timeLoss', 'waitingTime']]

offcanvas = html.Div(
    [
        dbc.Button("Traffic indicators", id="open-movie-offcanvas", n_clicks=0, style={'backgroundColor':'#deb522','color':'black','fontWeight': 'bold','border':'none'}),
        dbc.Offcanvas(html.Div([
            html.Div(id="street-ind",
                children="Street indicators",
            ),
            dcc.Dropdown(
            id='traffic-dropdown',
            options=dropdown_options,
            value='traveltime',
            placeholder='Select a traffic indicator...',
            searchable=True,
            style={'color':'black'}
            ),
            html.Div(id="vehicle-ind",
                children="Vehicle indicators",
            ),
            dcc.Dropdown(
            id='vehicle-dropdown',
            options=dropdown_options_vehicles,
            value='duration',
            placeholder='Select a vehicular traffic indicator...',
            searchable=True,
            style={'color':'black'}
            ),
            #dcc.Store(id='traffic-store', storage_type='session'),
            #dcc.Store(id='vehicular-traffic-store', storage_type='session'),
            dcc.Loading(html.Div(id='movie-recommendation-content'),type='circle',color='#deb522',style={'marginTop': '60px'})]),
            id="movie-recommendation-offcanvas",
            title="Traffic indicator",
            is_open=False,
            style={'backgroundColor':"black",'color':'#deb522'},
        )
    ],
    style={'display': 'flex', 'justifyContent': 'space-between','marginTop': '20px'}
)

# Define the layout of the app
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Img(src="./assets/imdb.png",width=150), width=2),
            dbc.Col(
                dcc.Tabs(id='graph-tabs', value='overview', children=[
                    dcc.Tab(label='Overview', value='overview',style=tab_style['idle'],selected_style=tab_style['active']),
                    dcc.Tab(label='Integrated results', value='integrated',style=tab_style['idle'],selected_style=tab_style['active']),
                    dcc.Tab(label='By streets', value='streets',style=tab_style['idle'],selected_style=tab_style['active']),
                    dcc.Tab(label='By vehicles', value='vehicles',style=tab_style['idle'],selected_style=tab_style['active'])
                ], style={'marginTop': '15px', 'width':'600px','height':'50px'})
            ,width=6),dbc.Col(offcanvas, width=4)
        ]),
        # dbc.Row([
        #
        #     dbc.Col(generate_stats_card("Work",num_of_works,"./assets/movie-icon.png"), width=3),
        #     dbc.Col(generate_stats_card("Language", num_of_lang,"./assets/language-icon.svg"), width=3),
        #     dbc.Col(generate_stats_card("Country",num_of_countries,"./assets/country-icon.png"), width=3),
        #     dbc.Col(generate_stats_card("Average Votes",avg_votes,"./assets/vote-icon.png"), width=3),
        # ],style={'marginBlock': '10px'}),
        dbc.Row([
            dcc.Tabs(id='tabs', value='movie', children=[
                #dcc.Tab(label='Movie', value='movie',style={'border':'1px line white','backgroundColor':'black','color': '#deb522','fontWeight': 'bold'},selected_style={'border':'1px solid white','backgroundColor':'black','color': '#deb522','fontWeight': 'bold','textDecoration': 'underline'}),
                #dcc.Tab(label='Series', value='series',style={'border':'1px solid white','backgroundColor':'black','color': '#deb522','fontWeight': 'bold'},selected_style={'border':'1px solid white','backgroundColor':'black','color': '#deb522','fontWeight': 'bold','textDecoration': 'underline'}),
            ], style={'padding': '0px'})
        ]),
        dbc.Row([
            dcc.Loading([
                html.Div(id='tabs-content')
            ],type='default',color='#deb522')
        ])
    ], style={'padding': '0px'})
],style={'backgroundColor': 'black', 'minHeight': '100vh'})

@app.callback(
    Output("movie-recommendation-offcanvas", "is_open"),
    Input("open-movie-offcanvas", "n_clicks"),
    [State("movie-recommendation-offcanvas", "is_open")],
)
def toggle_offcanvas_movie(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(
    Output('tabs-content', 'children'),
    [Input('graph-tabs', 'value'), Input('tabs', 'value'), Input('traffic-dropdown', 'value'), Input('vehicle-dropdown', 'value')]
)
def update_tab(tab,tab2, traffic, vehicle):
    data, splits = load_data(tab2)
    if tab == 'overview':
        fig1, fig2, fig3, fig4 = generate_visualizations1(dO, dR, VO, VR, traffic, vehicle)
        return html.Div([
        html.Div([
            dcc.Graph(id='graph1', figure=fig1),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
                dcc.Graph(id='graph2', figure=fig2),
            ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
                dcc.Graph(id='graph3', figure=fig3),
        ], style={'width': '100%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph4', figure=fig4),
        ], style={'width': '100%', 'display': 'inline-block'})
    ])
    elif tab == 'integrated':
        figures = generate_visualizations2(dO, dR, traffic)
        return (
            html.Div(
                id="description-card",
                children=[
                    html.H4("Histograms with integrated results divided by time frames comparing the streets with and without deviations"),
                    html.Div(
                        id="intro",
                        children="A histogram shows the frequency distribution of the results.",
                    ),
                ],style={'color': 'white'}),
        html.Div([
        html.Div([
            dcc.Graph(id="graph" + str(i), figure=figure)
        ], style={'width': '50%', 'display': 'inline-block'}) for i, figure in enumerate(figures)
        ]))
    elif tab == 'streets':
        fig1, fig2, fig3, fig4 = generate_visualizations3(data, splits)
        return html.Div([
        html.Div([
            dcc.Graph(id='graph1', figure=fig1),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph2', figure=fig2),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph3', figure=fig3),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph4', figure=fig4),
        ], style={'width': '50%', 'display': 'inline-block'})
    ])
    elif tab == 'vehicles':
        fig1 = generate_visualizations4(VO, VR, vehicle)
        return html.Div([
        html.Div([
            dcc.Graph(id='graph1', figure=fig1),
        ], style={'width': '100%', 'display': 'inline-block'}),
        ])


if __name__ == '__main__':
    app.run_server(debug=False)