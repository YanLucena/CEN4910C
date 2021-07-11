# Magnificent 7
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import json
from datetime import datetime

# This CSS was 100% stolen from someone on GitHub, LOL! We must iterate on this.
# credits: https://gist.github.com/alistairewj
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# System Date and Time
now = datetime.now()
dt = now.strftime("%d/%m/%Y %H:%M:%S")

# Read geojson files
d1 = open(r"backend_resources\results\orlando_averaged_2019-01-01.geojson")
data = json.load(d1)
d2 = data["features"][0]

# Extract data from JSON file
d3 = pd.json_normalize(data, record_path=['features'])
base = d3.loc[:, ["properties.NeighName", 'properties.avg_d_mbps']]
base.columns = ["NeighName", "avg_d_mbps"]  # change column name

# Function to generate drop-down list (Neighborhood names)

def Neigh_names():

    global base
    base["label"] = base.loc[:, "NeighName"]
    base["value"] = base.loc[:, "NeighName"]
    col_list = base.loc[:, ["label", "value"]]
    col_list = col_list.drop_duplicates("label")
    base = base.drop(["label", "value"], axis=1)  # removing the added coloumn
    new_row = {'label': 'All', 'value': "All"}
    col_list = col_list.append(new_row, ignore_index=True)
    return col_list.to_dict("records")

# ----------Dash App---------------------------------------

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# reset button
reset_data = html.A(html.Button('Reset Data',
                                style={
                                    "marginLeft": "70px",
                                    "position": "absolute",
                                    "marginTop": "230px",
                                    "backgroundColor": "#FF8C00",
                                    "borderRadius": "20px"
                                }

                                ), href='/')

# Banner with titles and reset button

banner = html.Div([
    html.H3(["Orlando's Digital Divide"],
            style={
            "position": "absolute",
            "marginLeft": "20px",
            "padding": "50px",
            "width": "500px",
            "height": "222px",
            "fontFamily": "Arial",
            "fontSize": "30px",
            "color": "white",
            "display": "block"
            }
            ),  # ------- First Title
    html.H3(["This dashboard is intended to assist with displaying Orlando's download and upload speeds by its neighborhoods over time."],
            style={
            "marginLeft": "70px",
            "position": "absolute",
            "paddingTop": "140px",
            "width": "600px",
            "height": "222px",
            "display": "block",
            "fontSize": "20px",
            "color": "darkblue",
            }
            ),  # -----------Second Title

    html.H1("^",
            style={
                "position": "absolute",
                "marginLeft": "720px",
                "paddingTop": "40px",
                "fontSize": "300px",
                "color": "darkblue",
            }
            ),  # -------Internet symbol

    reset_data  # -----Reset button

],

    style={
        "backgroundColor": "#4169E1",
        "width": "1000px",
        "height": "300px",
        "display": "inline-block"
}
)

# ---Quarter Drop Down element

drop_down = html.Div([
    dcc.Dropdown(
        id="time",
        options=[
            {'label': 'Q1 2019', 'value': '2019-01-01'},
            {'label': 'Q2 2019', 'value': '2019-04-01'},
            {'label': 'Q3 2019', 'value': '2019-07-01'},
            {'label': 'Q4 2019', 'value': '2019-10-01'},
            {'label': 'Q1 2020', 'value': '2020-01-01'},
            {'label': 'Q2 2020', 'value': '2020-04-01'},
            {'label': 'Q3 2020', 'value': '2020-07-01'},
            {'label': 'Q4 2020', 'value': '2020-10-01'},
            {'label': 'Q1 2021', 'value': '2021-01-01'},

        ],
        value="2019-01-01",
        searchable=True,
        placeholder="Select a Quarter from drop-down",
                    style={"marginLeft": "10px",
                           "width": "200px", "color": "grey"},
    )],
    style={
    "borderColor": "black",
    "display": "inline-block",
    "marginLeft": "50px"
},
)

# Download and Upload speed dropdown element
speed = html.Div([
    dcc.Dropdown(
        id="internet",
        options=[
            {'label': 'Upload Speed', 'value': 'avg_u_mbps'},
            {'label': 'Download Speed', 'value': 'avg_d_mbps'},

        ],
        value="avg_d_mbps",
        searchable=True,
        placeholder="Upload or Download Speed",
        style={
            "marginLeft": "10px",
            "width": "200px",
            "color": "grey"
        },
    )],
    style={
    "borderColor": "black",
    "display": "inline-block",
    "marginLeft": "50px"
},
)

# Neighborhood names dropdown (this uses the function defined at the top)
NeighHood_names = html.Div([

    dcc.Dropdown(
        id="Neigh_names",
        options=Neigh_names(),  # function calling
        value="All",
        searchable=True,
        placeholder="Select neighbhood",
        style={
            "width": "200px",
            "color": "grey",
            "marginLeft": "10px",
        },
    )
],
    style={
    "borderColor": "red",
    "display": "inline-block",
    "marginLeft": "100px"
})


# Choropleth Map element

final_map = html.Div([dcc.Graph(id="map")],
                     style={

    "marginLeft": "50px",
    "paddingTop": "20px",
    "width": "910px",
    "height": "300px",
    "display": "inline-block"

})

# UI layout design (Include the formating, colors and the way drop downs will be arranged in the dashboard)

container_0 = html.Div([
    NeighHood_names,
    drop_down, speed,
    html.Br()
],
    style={
    "width": "900px",
    "backgroundColor": "#1E4B8F",
    "paddingTop": "20px",
    "paddingBottom": "20px",
    "display": "inline-block",
    "marginLeft": "50px",
    "position": "relative",
})

# Last updated element

Last_updated = html.Div(
    id='date', style={"display": "inline", "marginLeft": "50px"})

# Footer element
footer = html.H6(children='Magnificent 7',
                 style={"color": "black", "display": "inline", "marginLeft": "800px", "fontSize": "15px",
                        })

# Dashboard Title element
title = html.H3(children='Internet Speeds in Orlando',
                style={"marginLeft": "325px", "color": "#1E4B8F", "display": "inline", "fontSize": "25px",
                       })

# Final layout container with graphs and other elements

container_1 = html.Div([
    html.Div([
        banner,
        html.Br(),
        title,
        html.Br(),
        html.Br(),
        container_0,
        final_map,
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        footer,
        html.Br(),
        Last_updated,
    ],
        style={
        "width": "1000px",
        "height": "1000px",
        "backgroundColor": "#F5F5F5",
        "margin": "auto"
    }),
])

# Final Layout
app.layout = html.Div([container_1])

# App callback
@app.callback(
    [Output('map', "figure"), Output('date', "children")],
    [Input('time', 'value'), Input("Neigh_names",
                                   "value"), Input("internet", "value")],
    prevent_initial_callbacks=True
)
# call back function
def update_map(qrt, name, int_speed):
    d1 = open(r"backend_resources\results\orlando_averaged_" + qrt + ".geojson")
    data = json.load(d1)
    base = pd.json_normalize(data, record_path=['features'])
    base = base.iloc[:, [6, 7, 8]]
    base.columns = ["NeighName", "avg_d_mbps", "avg_u_mbps"]
    if name != "All":
        base = base.loc[base.loc[:, "NeighName"] == name, ]

    # Plotly Choropleth Graph
    fig = px.choropleth_mapbox(base, geojson=data, locations="NeighName", color=int_speed, featureidkey="properties.NeighName",
                               center={"lat": 28.5383, "lon": -81.3792},
                               color_continuous_scale="ice",
                               mapbox_style="carto-positron", zoom=11)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    #date and time
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")

    return fig, dt

if __name__ == '__main__':
    app.run_server(debug=True)
