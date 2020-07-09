import dash
import dash_table
from dashlib.ores import ore_df
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc

df = ore_df()

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    dcc.Tabs([
        dcc.Tab(label="Raw Ore", children=[
            html.H1(children="Mining output table"),
            html.H4("Current price in Amarr for 10,000 m3"),

            dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            sort_action='native',
            filter_action='native'
            )
            ]),

        dcc.Tab(label="Brains", children=[
            html.H1(children="Brains"),
            ])

        ])
    ])

if __name__ == '__main__':
    app.run_server(debug=True)