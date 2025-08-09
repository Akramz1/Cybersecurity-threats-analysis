import plotly.graph_objects as go
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import numpy as np


app = Dash(__name__)


df = pd.read_csv(
    'Cybersecurity_Threats(2015-2024)/Global_Cybersecurity_Threats_2015-2024.csv')


app.layout = html.Div(style={'backgroundColor': '#0e1726'}, children=[
    html.H1("Cybersecurity Threats (2015-2024) Globally",
            style={'textAlign': 'center', 'color': 'white'}),

    dcc.Dropdown(
        id="select_attack_type",
        options=[{"label": atype, "value": atype}
                 for atype in df["Attack Type"].unique()],
        multi=False,
        value='SQL Injection',
    ),

    html.Div(id='output_container'),
    html.Br(),

    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around'}, children=[
        html.Div(style={'width': '48%', 'marginBottom': '20px'}, children=[
            dcc.Graph(id='my_map', style={
                      'height': '70vh', 'boxShadow': '0 0 20px #38bdf8', 'borderRadius': '10px'}),
        ]),
        html.Div(style={'width': '48%', 'marginBottom': '20px'}, children=[
            dcc.Graph(id='bar_chart'),
        ]),
        html.Div(style={'width': '48%', 'marginBottom': '20px'}, children=[
            dcc.Graph(id='attack_type_chart'),
        ]),
        html.Div(style={'width': '48%', 'marginBottom': '20px'}, children=[
            dcc.Graph(id='attack_source_chart'),
        ]),
        html.Div(style={'width': '48%', 'marginBottom': '20px'}, children=[
            dcc.Graph(id='defense_mechanism_chart'),
        ]),
        html.Div(style={'width': '48%', 'marginBottom': '20px'}, children=[
            dcc.Graph(id='resolution_time_chart')
        ]),
    ])
])


@app.callback(
    [Output('output_container', 'children'),
     Output('my_map', 'figure'),
     Output('bar_chart', 'figure'),
     Output('attack_type_chart', 'figure'),
     Output('attack_source_chart', 'figure'),
     Output('defense_mechanism_chart', 'figure'),
     Output('resolution_time_chart', 'figure')],
    [Input('select_attack_type', 'value')]
)
def update_graph(option_slctd):
    container = html.Span(
        f"The Attack Type chosen by user was: {option_slctd}",
        style={'color': 'white', 'fontWeight': 'bold', 'fontSize': '20px'}
    )

    dff = df[df["Attack Type"] == option_slctd]
    bar_data = dff.groupby('Country')['Financial Loss (in Million $)'].sum(
    ).sort_values(ascending=False).head(10)
    attack_source_data = dff['Attack Source'].value_counts()
    attack_type_data = df['Attack Type'].value_counts()
    defense_data = dff['Defense Mechanism Used'].value_counts()

    map_fig = go.Figure(
        data=go.Choropleth(
            locations=dff['Country'],
            locationmode='country names',
            z=dff['Number of Affected Users'],
            text=dff['Country'],
            colorscale='Reds',
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title='Affected Users'
        )
    )
    map_fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False,
                 projection_type='equirectangular', bgcolor='#0e1726'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': 'white'}, margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    bar_fig = go.Figure([go.Bar(
        x=bar_data.index,
        y=bar_data.values,
        orientation='v',
        marker_color='crimson'
    )])
    bar_fig.update_layout(
        title='Top 10 Countries by Financial Loss (in Millions)',
        xaxis=dict(
            tickformat=',.0f',
            ticksuffix='',
            color='white'
        ),
        yaxis=dict(
            ticksuffix='M',
            color='white'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        margin=dict(l=50, r=20, t=30, b=30)
    )

    attack_type_fig = go.Figure(
        data=[go.Pie(labels=attack_type_data.index,
                     values=attack_type_data.values, hole=0.3)]
    )
    attack_type_fig.update_layout(
        title='Attack Type Distribution',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'}
    )

    attack_source_fig = go.Figure(
        data=[go.Bar(x=attack_source_data.index,
                     y=attack_source_data.values, marker_color='orange')]
    )
    attack_source_fig.update_layout(
        title='Attack Source Distribution',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'}
    )

    defense_fig = go.Figure(
        data=[go.Bar(x=defense_data.values, y=defense_data.index,
                     orientation='h', marker_color='green')]
    )
    defense_fig.update_layout(title='Defense Mechanisms Used',
                              paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})

    resolution_fig = go.Figure(
        data=[go.Histogram(x=dff['Incident Resolution Time (in Hours)'],
                           marker_color='purple', nbinsx=20)]
    )
    resolution_fig.update_layout(title='Incident Resolution Time (in Hours)',
                                 paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})

    return container, map_fig, bar_fig, attack_type_fig, attack_source_fig, defense_fig, resolution_fig


if __name__ == '__main__':
    app.run(debug=True)
