import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import ssl
from urllib import request
from datetime import datetime, timezone, timedelta

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no, minimum-scale=0.75"}],
)
app.title = "Covid | Vibe Check"

server = app.server
app.config.suppress_callback_exceptions = True


def get_databases():
    ssl._create_default_https_context = ssl._create_unverified_context
    url = 'https://raw.githubusercontent.com/JalalElwazze/vibeDatabase/main/data.csv'
    urldf = request.urlopen(url)
    df = pd.read_csv(urldf, header=None, delim_whitespace=True)
    df.columns = ["Date", "Time", "Compound NSW", "Compound WA", "Compound ACT", "Compound SA", "Compound QLD", "Compound NT",
                  "Compound TAS", "Compound VIC", "Compound Aus", "Compound Scomo", "Compound Gladys", "Compound Dan", "Compound Vaxx"]

    df["Datetime"] = df["Date"] + " " + df["Time"]
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    df = df.tail(24*4)

    return df


def get_tweets():
    ssl._create_default_https_context = ssl._create_unverified_context
    url = 'https://raw.githubusercontent.com/JalalElwazze/vibeDatabase/main/key_tweets.json'
    urldf = request.urlopen(url)
    key_tweets = pd.read_json(urldf, typ='series')

    return key_tweets


df = get_databases()
key_tweets = get_tweets()


def create_fig(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Datetime"], y=df["Compound NSW"], mode='lines+markers', name='NSW'))
    fig.add_trace(go.Scatter(x=df["Datetime"], y=df["Compound VIC"], mode='lines+markers', name='VIC'))
    fig.add_trace(go.Scatter(x=df["Datetime"], y=df["Compound WA"], visible='legendonly', mode='lines+markers', name='WA'))
    fig.add_trace(go.Scatter(x=df["Datetime"], y=df["Compound ACT"], mode='lines+markers', name='ACT'))
    fig.add_trace(go.Scatter(x=df["Datetime"], y=df["Compound SA"], visible='legendonly', mode='lines+markers', name='SA'))
    fig.add_trace(go.Scatter(x=df["Datetime"], y=df["Compound QLD"], mode='lines+markers', name='QLD'))
    fig.add_trace(go.Scatter(x=df["Datetime"], y=df["Compound NT"], visible='legendonly', mode='lines+markers', name='NT'))
    fig.add_trace(go.Scatter(x=df["Datetime"], y=df["Compound TAS"], visible='legendonly', mode='lines+markers', name='TAS'))

    fig.update_layout(
        showlegend=True,
        legend_orientation="h",
        legend_y=1.25,
        plot_bgcolor="white",
        margin=dict(t=10,l=10,b=10,r=10)
    )

    return fig


def create_fig_2(df):
    fig2 = go.Figure()

    fig2.add_trace(go.Indicator(
        mode="number+delta",
        number={'prefix': "+", 'valueformat': '.2f'} if df["Compound NSW"].iloc[-1] >= 0 else {'prefix': "", 'valueformat': '.2f'},
        title={"text": "NSW"},
        value=df["Compound NSW"].iloc[-1],
        delta={'position': "top", 'reference': df["Compound NSW"].iloc[-5], 'relative': False},
        domain={'row': 0, 'column': 0}))

    fig2.add_trace(go.Indicator(
        mode="number+delta",
        number={'prefix': "+", 'valueformat': '.2f'} if df["Compound VIC"].iloc[-1] >= 0 else {'prefix': "", 'valueformat': '.2f'},
        title={"text": "VIC"},
        value=df["Compound VIC"].iloc[-1],
        delta={'position': "top", 'reference': df["Compound VIC"].iloc[-5], 'relative': False},
        domain={'row': 0, 'column': 1}))

    fig2.add_trace(go.Indicator(
        mode="number+delta",
        number={'prefix': "+", 'valueformat': '.2f'} if df["Compound QLD"].iloc[-1] >= 0 else {'prefix': "", 'valueformat': '.2f'},
        title={"text": "QLD"},
        value=df["Compound QLD"].iloc[-1],
        delta={'position': "top", 'reference': df["Compound QLD"].iloc[-5], 'relative': False},
        domain={'row': 0, 'column': 2}))

    fig2.add_trace(go.Indicator(
        mode="number+delta",
        number={'prefix': "+", 'valueformat': '.2f'} if df["Compound WA"].iloc[-1] >= 0 else {'prefix': "", 'valueformat': '.2f'},
        title={"text": "WA"},
        value=df["Compound WA"].iloc[-1],
        delta={'position': "top", 'reference': df["Compound WA"].iloc[-5], 'relative': False},
        domain={'row': 0, 'column': 3}))

    fig2.add_trace(go.Indicator(
        mode="number+delta",
        number={'prefix': "+", 'valueformat': '.2f'} if df["Compound SA"].iloc[-1] >= 0 else {'prefix': "", 'valueformat': '.2f'},
        title={"text": "SA"},
        value=df["Compound SA"].iloc[-1],
        delta={'position': "top", 'reference': df["Compound SA"].iloc[-5], 'relative': False},
        domain={'row': 1, 'column': 0}))

    fig2.add_trace(go.Indicator(
        mode="number+delta",
        number={'prefix': "+", 'valueformat': '.2f'} if df["Compound ACT"].iloc[-1] >= 0 else {'prefix': "", 'valueformat': '.2f'},
        title={"text": "ACT"},
        value=df["Compound ACT"].iloc[-1],
        delta={'position': "top", 'reference': df["Compound ACT"].iloc[-5], 'relative': False},
        domain={'row': 1, 'column': 1}))

    fig2.add_trace(go.Indicator(
        mode="number+delta",
        number={'prefix': "+", 'valueformat': '.2f'} if df["Compound TAS"].iloc[-1] >= 0 else {'prefix': "", 'valueformat': '.2f'},
        title={"text": "TAS"},
        value=df["Compound TAS"].iloc[-1],
        delta={'position': "top", 'reference': df["Compound TAS"].iloc[-5], 'relative': False},
        domain={'row': 1, 'column': 2}))

    fig2.add_trace(go.Indicator(
        mode="number+delta",
        title={"text": "NT"},
        number={'prefix': "+", 'valueformat': '.2f'} if df["Compound NT"].iloc[-1] >= 0 else {'prefix': "", 'valueformat': '.2f'},
        value=df["Compound NT"].iloc[-1],
        delta={'position': "top", 'reference': df["Compound NT"].iloc[-5], 'relative': False},
        domain={'row': 1, 'column': 3}))

    fig2.update_layout(
        grid={'rows': 2, 'columns': 4, 'pattern': "independent"},
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig2


def create_fig_3(df):
    fig3 = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=df["Compound Aus"].iloc[-1],
        number={'prefix': "+", 'valueformat': '.2f'} if df["Compound Aus"].iloc[-1] >= 0 else {'prefix': "",
                                                                                              'valueformat': '.2f'},
        mode="gauge+number+delta",
        delta={'reference': df["Compound Aus"].iloc[-1]},
        gauge={'bar': {'color': "rgba(160,68,255,1)", 'thickness': 0.5},
               'axis': {'range': [-1, 1], 'tickwidth': 0.01, 'tickcolor': "#f1f1f1"},
               'bordercolor': "white",
               'steps': [
                     {'range': [-1, 1], 'color': "#f1f1f1"}],
               }))

    fig3.update_layout(
        margin=dict(l=20, r=20, t=60, b=40),
    )

    return fig3


def create_fig_4(df):
    fig4 = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=df["Compound Scomo"].iloc[-1],
        number={'prefix': "+", 'valueformat': '.2f'} if df["Compound Scomo"].iloc[-1] >= 0 else {'prefix': "",
                                                                                              'valueformat': '.2f'},
        mode="gauge+number+delta",
        delta={'reference': df["Compound Scomo"].iloc[-1]},
        gauge={'axis': {'range': [-1, 1]},
                'bar': {'color': "rgba(160,68,255,1)"},
                'bordercolor': "white",
                 'steps': [
                     {'range': [-1, 1], 'color': "#f1f1f1"},],
               }))

    fig4.update_layout(
        margin=dict(l=20, r=20, t=60, b=40),
    )

    return fig4


def create_fig_5(df):
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(x=df["Datetime"], y=df["Compound Gladys"], mode='lines+markers', name='Gladys'))
    fig5.add_trace(go.Scatter(x=df["Datetime"], y=df["Compound Dan"], mode='lines+markers', name='Dan'))
    fig5.update_layout(
        showlegend=True,
        legend_orientation="h",
        legend_y=1.1,
        plot_bgcolor="white",
        margin=dict(t=10,l=10,b=10,r=10)
    )

    return fig5


def create_fig_6(df):
    fig6 = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=float(df["Compound Vaxx"].iloc[[-1]].mean()),
        number={'prefix': "+", 'valueformat': '.2f'} if float(df["Compound Vaxx"].iloc[[-1]].mean()) >= 0 else {'prefix': "",
                                                                                              'valueformat': '.2f'},
        mode="gauge+number+delta",
        delta={'reference': float(df["Compound Vaxx"].iloc[[-5]].mean())},
        gauge={'axis': {'range': [-1, 1]},
                'bar': {'color': "rgba(160,68,255,1)"},
                'bordercolor': "white",
                 'steps': [
                     {'range': [-1, 1], 'color': "#f1f1f1"},],
               }))

    fig6.update_layout(
        margin=dict(l=40, r=40, t=60, b=60),
    )

    return fig6


app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("logo.png")),
                      html.Div(
                          id='update-text-container',
                          children=["Updated: "]
                      ),
                      dcc.Interval(
                          id='interval-component',
                          interval=15*60*1*1000,  # in milliseconds
                          n_intervals=0
                      ),
                      ],
        ),


        html.Div(
            id='row-1',
            children=[
                html.Div(
                    id="left-column",
                    className="five columns",
                    children=[
                        # Patient Volume Heatmap
                        html.Div(
                            id="vibes_over_time_card",
                            children=[
                                html.B("Vibe Check - 24hr Change"),
                                html.Hr(),
                                dcc.Graph(id="vibes_over_time_graph", figure=create_fig_2(df)),
                            ],
                        ),
                        html.Div(
                            id="info_card",
                            children=[
                                html.Div(id='info-wrapper', children=[
                                    html.H1("What is this?"),
                                    html.P("Every 15 minutes this website checks twitter for the 100 most recent COVID "
                                           "related posts from each state. The overall vibe is calculated using machine learning "
                                           "and expressed as a number between -1 (extremely negative) "
                                           "and +1 (extremely positive). "
                                           "See how your vibe compares, remembering that this is "
                                           "only a small slice of the people and organisations bothered enough to post on twitter.",
                                    ),
                                ]
                                )
                            ],
                        ),
                    ],
                ),

                html.Div(
                    id="right-column",
                    className="seven columns",
                    children=[

                        html.Div(
                            id="vibe_check_card",
                            children=[
                                html.B("Vibes History - Search Term State + Covid"),
                                html.Hr(),
                                dcc.Graph(id="vibe_check_graph", figure=create_fig(df)),
                            ],
                        ),

                        html.Div(
                            id="country_card",
                            className="six columns",
                            children=[
                                html.B("Search - Australia Covid"),
                                html.Hr(),
                                dcc.Graph(id="country_graph", figure=create_fig_3(df)),
                            ],
                        ),

                        html.Div(
                            id="scomo_card",
                            className="six columns",
                            children=[
                                html.B("Search - Scott Morrison"),
                                html.Hr(),
                                dcc.Graph(id="scomo_graph", figure=create_fig_4(df)),
                            ],
                        ),
                    ],
                ),
            ]
        ),

        html.Div(
            id="row-three",
            children=[

                html.Div(
                    id="tweet_cards_header",
                    children=[
                        html.H1("see what people are saying"),
                    ],
                ),

                html.Div(
                    id="tweet_container_row",
                    children=[
                        html.Div(
                            className='four columns',
                            id="negative_tweet_card",
                            children=[
                                html.B("Most Negative - Pick a Search"),
                                html.Hr(id='negative-hr'),
                                dcc.Dropdown(
                                        id='negative-dropdown',
                                        options=[
                                            {'label': 'NSW', 'value': 'NSW Covid Negative'},
                                            {'label': 'VIC', 'value': 'VIC Covid Negative'},
                                            {'label': 'WA', 'value': 'WA Covid Negative'},
                                            {'label': 'SA', 'value': 'SA Covid Negative'},
                                            {'label': 'QLD', 'value': 'QLD Covid Negative'},
                                            {'label': 'NT', 'value': 'NT Covid Negative'},
                                            {'label': 'ACT', 'value': 'VIC Covid Negative'},
                                            {'label': 'TAS', 'value': 'VIC Covid Negative'},
                                            {'label': 'Gladys', 'value': 'Gladys Berejiklian Negative'},
                                            {'label': 'Scomo', 'value': 'Scott Morrison Negative'},
                                            {'label': 'Dan', 'value': 'Daniel Andrews Negative'},
                                            {'label': 'Vaccines', 'value': 'Australia Vaccinations Negative'},
                                        ],
                                        value='Gladys Berejiklian Negative',
                                        searchable=False,
                                    ),

                                html.Div(
                                    id='tweet-text-container-negative',
                                    children=[
                                        html.P(children=key_tweets['NSW Covid Negative'], id='negative-tweet'),
                                        html.H1(children="@" + key_tweets['NSW Covid Negative Author'],
                                                id='negative-author'),
                                    ]
                                ),
                            ],
                        ),

                        html.Div(
                            className='four columns',
                            id="positive_tweet_card",
                            children=[
                                html.B("Most Positive - Pick a Search"),
                                html.Hr(id='positive-hr'),
                                dcc.Dropdown(
                                    id='positive-dropdown',
                                    options=[
                                        {'label': 'NSW', 'value': 'NSW Covid Positive'},
                                        {'label': 'VIC', 'value': 'VIC Covid Positive'},
                                        {'label': 'WA', 'value': 'WA Covid Positive'},
                                        {'label': 'SA', 'value': 'SA Covid Positive'},
                                        {'label': 'QLD', 'value': 'QLD Covid Positive'},
                                        {'label': 'NT', 'value': 'NT Covid Positive'},
                                        {'label': 'ACT', 'value': 'VIC Covid Positive'},
                                        {'label': 'TAS', 'value': 'VIC Covid Positive'},
                                        {'label': 'Gladys', 'value': 'Gladys Berejiklian Positive'},
                                        {'label': 'Scomo', 'value': 'Scott Morrison Positive'},
                                        {'label': 'Dan', 'value': 'Daniel Andrews Positive'},
                                        {'label': 'Vaccines', 'value': 'Australia Vaccinations Positive'},
                                    ],
                                    value='WA Covid Positive',
                                    searchable=False,
                                ),
                                html.Div(
                                    id='tweet-text-container-positive',
                                    children=[
                                        html.P(children=key_tweets['NSW Covid Positive'], id='positive-tweet'),
                                        html.H1(children="@" + key_tweets['NSW Covid Positive Author'],
                                                id='positive-author'),
                                    ]
                                ),
                            ],
                        ),

                        html.Div(
                            className='four columns',
                            id="most_liked_tweet_card",
                            children=[
                                html.Div(id='tweet-text-container-popular',
                                         children=[html.H1(children="Popular in Australia Covid"),
                                                   html.H2(children=str(key_tweets['Australia Covid Popular Count']) + ' likes'),
                                                   html.P('"' + key_tweets['Australia Covid Popular'] + '"'),
                                                   html.H2("@" + key_tweets['Australia Covid Popular Author']),
                                                   ]
                                         ),
                            ],
                        ),
                    ],
                ),
            ],
        ),

        html.Div(
            id="row-four",
            children=[
                html.Div(
                    id="dan_v_gladys",
                    className='six columns',
                    children=[
                        html.B("Dan V Gladys"),
                        html.Hr(),
                        dcc.Graph(id="dan_v_gladys_graph", figure=create_fig_5(df)),
                    ],
                ),

                html.Div(
                    id="vaxx",
                    className='six columns',
                    children=[
                        html.B("Search Term - Vaccinations"),
                        html.Hr(),
                        dcc.Graph(id="vaxx_graph", figure=create_fig_6(df)),
                    ],
                ),

            ],
        ),



    ]
)


@app.callback(
    dash.dependencies.Output('negative-author', 'children'),
    [dash.dependencies.Input('negative-dropdown', 'value')])
def update_output(value):
    key_tweets = get_tweets()
    return '@{}'.format(key_tweets[value + " Author"])


@app.callback(
    dash.dependencies.Output('negative-tweet', 'children'),
    [dash.dependencies.Input('negative-dropdown', 'value')])
def update_output(value):
    key_tweets = get_tweets()
    return '{}'.format(key_tweets[value])


@app.callback(
    dash.dependencies.Output('tweet-text-container-popular', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_output(value):
    key_tweets = get_tweets()
    return [html.H1(children="Popular in Australia Covid"),
            html.H2(children=str(key_tweets['Australia Covid Popular Count']) + ' likes'),
            html.P('"' + key_tweets['Australia Covid Popular'] + '"'),
            html.H2("@" + key_tweets['Australia Covid Popular Author']),
            ]


@app.callback(
    dash.dependencies.Output('positive-author', 'children'),
    [dash.dependencies.Input('positive-dropdown', 'value')])
def update_output(value):
    key_tweets = get_tweets()
    return '@{}'.format(key_tweets[value + " Author"])


@app.callback(
    dash.dependencies.Output('positive-tweet', 'children'),
    [dash.dependencies.Input('positive-dropdown', 'value')])
def update_output(value):
    key_tweets = get_tweets()
    return '{}'.format(key_tweets[value])


@app.callback(
    dash.dependencies.Output('update-text-container', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_output(value):
    return 'Updated {}'.format(datetime.now(timezone(timedelta(hours=10))).strftime("%d %B %H:%M"))


@app.callback(
    dash.dependencies.Output('vibe_check_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_output(value):
    return create_fig(get_databases())


@app.callback(
    dash.dependencies.Output('vibes_over_time_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_output(value):
    return create_fig_2(get_databases())


@app.callback(
    dash.dependencies.Output('country_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_output(value):
    return create_fig_3(get_databases())


@app.callback(
    dash.dependencies.Output('scomo_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_output(value):
    return create_fig_4(get_databases())


@app.callback(
    dash.dependencies.Output('dan_v_gladys_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_output(value):
    return create_fig_5(get_databases())


@app.callback(
    dash.dependencies.Output('vaxx_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_output(value):
    return create_fig_6(get_databases())


if __name__ == '__main__':
    app.run_server(debug=False)
