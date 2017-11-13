# -*- coding: utf-8 -*-
"""
Main Dash App

"""
import dash
import os

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np

#import loadspreadsheet as ls1
import loadsql as ls2

app = dash.Dash(__name__)
server = app.server

app.config.supress_callback_exceptions = True
app.title = 'Pepsi Project'
app.css.append_css({"external_url": "https://codepen.io/tenoli/pen/RjREVV.css"})  # Boostrap stylesheet

# Insert your MapBox token here
mapbox_access_token = 'pk.eyJ1IjoibWN5b3VrcyIsImEiOiJjajgzNmtjMXQ5MTRqMnFucGp0MXZ4ZWMxIn0.fYyxOFJPPkYGmaBBOXePgw'

df_monitoring = ls1.load_monitoring_data()
df_stores = ls2.load_stores_data()

traces = [df_monitoring, df_stores[['lon', 'lat']].loc[df_monitoring.index]]
df_monitoring = pd.concat(traces, axis=1)
df_monitoring = df_monitoring.loc[df_monitoring[['lon', 'lat']].dropna().index]


# HEADER
def header():
    """Returns the page header. 

    """
    return html.Div([
                html.Div([
                    html.A([
                        html.Img(
                            src='https://s3.amazonaws.com/dashboard-sales/logo.png',
                            className="logo",
                            style=dict(height='5.0rem', padding='.8rem 0 0 0'))

                    ], className="logo-link", href='http://tenoli.org/language/en/home/', target='_blank'),

                ], style={'height':'100%', 'margin-left': '3rem', 'margin-right': '15rem'})

            ], className='header', style={'margin-bottom': '12px'})

translate = {'invitation': 'Invitación',
             'workshop1': 'Taller 1',
             'workshop2': 'Taller 2',
             'workshop3': 'Taller 3',
             'spotlights_received': 'Focos recibidos',
             'spotlights_placed': 'Focos colocados',
             'paint_received': 'Pintura recibida',
             'paint_placed': 'Pintura colocada',
             'cover_received': 'Lona colocada',
             'cover_placed': 'Lona colocada'}

# LAYOUT
app.layout = html.Div([

    header(),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H5('Filters', className='no-spacing')

                ], className='card-header'),

                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.P(translate[workshop] + ':')

                            ], className='col-md-5 no-spacing'),

                            html.Div([
                                dcc.Checklist(
                                    id=workshop,
                                    options=[
                                        dict(label='SI', value=True),
                                        dict(label='NO', value=False)],
                                    values=[True, False],
                                    labelStyle=dict(display='inline-block'))

                            ], className='col-md-7 no-spacing')

                        ], className='row no-spacing') 

                        for workshop in ['invitation', 'workshop1', 'workshop2', 'workshop3']

                    ]),

                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.P(translate[status] + ':')

                                ], className='col-md-6 no-spacing'),

                                html.Div([
                                    dcc.Checklist(
                                        id=status,
                                        options=[
                                            dict(label='SI', value=True),
                                            dict(label='NO', value=False)],
                                        values=[True, False],
                                        labelStyle=dict(display='inline-block'))

                                ], className='col-md-6 no-spacing')

                            ], className='row no-spacing') 

                            for status in [f'{item}_received', f'{item}_placed']

                        ], style={'margin-top': '15px'})

                        for item in ['spotlights', 'paint', 'cover']

                    ]),


                ], className='card-block')

            ], className='card')

        ], className='col-md-3'),

        html.Div([
            html.Div([
                html.Div([
                    html.H5('View Map', className='no-spacing')

                ], className='card-header'),

                html.Div([
                    dcc.Graph(id='map-view-graph')

                ], className='card-block')

            ], className='card')

        ], className='col-md-5'),

        html.Div([
            html.Div([
                html.Div([
                    html.H5('Selection Info', className='no-spacing')

                ], className='card-header'),

                html.Div([
                    html.Div([
                        html.Div([
                            html.H6(id='store-info-id', children='00000', className='block-header no-spacing'),
                            html.P(id='store-info-name', children='-', className='text-muted'),

                        ], className='col-md-12 no-spacing'),

                    ], className='row no-spacing'),

                    html.Div([
                        html.Div([
                            html.P('Invitación', className='sub-header no-spacing'),
                            html.P(id='store-info-invitation', children='-', className='sub-info'),

                        ], className='col-md-3 no-spacing'),

                        html.Div([
                            html.P('Taller 1', className='sub-header no-spacing'),
                            html.P(id='store-info-workshop1', children='-', className='sub-info'),

                        ], className='col-md-3 no-spacing'),

                        html.Div([
                            html.P('Taller 2', className='sub-header no-spacing'),
                            html.P(id='store-info-workshop2', children='-', className='sub-info'),

                        ], className='col-md-3 no-spacing'),

                        html.Div([
                            html.P('Taller 3', className='sub-header no-spacing'),
                            html.P(id='store-info-workshop3', children='-', className='sub-info'),

                        ], className='col-md-3 no-spacing')

                    ], className='row no-spacing', style={'margin-top': '15px'}),

                    html.Div([
                        html.Div([
                            html.P('Focos recibidos', className='sub-header no-spacing'),
                            html.P(id='store-info-spotlights1', children='-', className='sub-info'),

                        ], className='col-md-6 no-spacing'),

                        html.Div([
                            html.P('Focos colocados', className='sub-header no-spacing'),
                            html.P(id='store-info-spotlights2', children='-', className='sub-info'),

                        ], className='col-md-6 no-spacing'),

                    ], className='row no-spacing', style={'margin-top': '20px'}),

                    html.Div([
                        html.Div([
                            html.P('Pintura recibida', className='sub-header no-spacing'),
                            html.P(id='store-info-paint1', children='-', className='sub-info'),

                        ], className='col-md-6 no-spacing'),

                        html.Div([
                            html.P('Pintura colocada', className='sub-header no-spacing'),
                            html.P(id='store-info-paint2', children='-', className='sub-info'),

                        ], className='col-md-6 no-spacing'),

                    ], className='row no-spacing', style={'margin-top': '15px'}),

                    html.Div([
                        html.Div([
                            html.P('Lona recibida', className='sub-header no-spacing'),
                            html.P(id='store-info-cover1', children='-', className='sub-info'),

                        ], className='col-md-6 no-spacing'),

                        html.Div([
                            html.P('Lona colocada', className='sub-header no-spacing'),
                            html.P(id='store-info-cover2', children='-', className='sub-info'),

                        ], className='col-md-6 no-spacing'),

                    ], className='row no-spacing', style={'margin-top': '15px'}),

                ], className='card-block')

            ], className='card')

        ], className='col-md-4'),

    ], className='row')

])

@app.callback(Output('map-view-graph', 'figure'),
              [Input('invitation', 'values'),
               Input('workshop1', 'values'),
               Input('workshop2', 'values'),
               Input('workshop3', 'values'),
               Input('spotlights_received', 'values'),
               Input('spotlights_placed', 'values'),
               Input('paint_received', 'values'),
               Input('paint_placed', 'values'),
               Input('cover_received', 'values'),
               Input('cover_placed', 'values')])
def update_map_view_graph(invitation, workshop1, workshop2, workshop3,
                          spotlights_received, spotlights_placed,
                          paint_received, paint_placed,
                          cover_received, cover_placed):
    """ Updates the Map View graph. 

    """
    filter0 = df_monitoring['invitation'].isin(invitation)

    filter1 = df_monitoring['workshop1'].isin(workshop1)
    filter2 = df_monitoring['workshop2'].isin(workshop2)
    filter3 = df_monitoring['workshop3'].isin(workshop3)

    filter4 = df_monitoring['spotlights_received'].isin(spotlights_received)
    filter5 = df_monitoring['spotlights_placed'].isin(spotlights_placed)

    filter6 = df_monitoring['paint_received'].isin(paint_received)
    filter7 = df_monitoring['paint_placed'].isin(paint_placed)

    filter8 = df_monitoring['cover_received'].isin(cover_received)
    filter9 = df_monitoring['cover_placed'].isin(cover_placed)

    filter = filter0 & filter1 & filter2 & filter3 & filter4 & filter5 & filter6 & filter7 & filter8 & filter9

    df = df_monitoring[filter]

    traces = []
    traces.append(
        go.Scattermapbox(
            lat=df['lat'],
            lon=df['lon'],
            mode='markers',
            marker=go.Marker(
                # color=colors[i],
                size=8, 
                opacity=0.7),
            text=df.index, # store ID
            #name=df.index, # store ID
            hoverinfo='text'))

    return {

        'data': traces,

        'layout': go.Layout(
            height=370,
            autosize=True,
            hovermode='closest',
            margin=dict(l=0, r=0, t=0, b=0),
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=19.380434,
                    lon=-99.050932),
                pitch=0,
                zoom=11.4),
            legend=go.Legend(
                xanchor='right',
                x=1,
                bgcolor='white',
                bordercolor='#DEDEDE',
                borderwidth=1)
        )

    }

d = {True: 'SI', False: 'NO'}

@app.callback(Output('store-info-id', 'children'),
              [Input('map-view-graph', 'hoverData')])
def update_store_id(hover_store):
    store_id = hover_store['points'][0]['text']
    return store_id

@app.callback(Output('store-info-name', 'children'),
              [Input('map-view-graph', 'hoverData')])
def update_store_name(hover_store):
    store_id = hover_store['points'][0]['text']
    name = df_monitoring.loc[store_id, 'name']
    return name

@app.callback(Output('store-info-invitation', 'children'),
              [Input('map-view-graph', 'hoverData')])
def update_store_id(hover_store):
    store_id = hover_store['points'][0]['text']
    bool = df_monitoring.loc[store_id, 'invitation']
    return d[bool]

@app.callback(Output('store-info-workshop1', 'children'),
              [Input('map-view-graph', 'hoverData')])
def update_store_workshop1(hover_store):
    store_id = hover_store['points'][0]['text']
    bool = df_monitoring.loc[store_id, 'workshop1']
    return d[bool]

@app.callback(Output('store-info-workshop2', 'children'),
              [Input('map-view-graph', 'hoverData')])
def update_store_workshop2(hover_store):
    store_id = hover_store['points'][0]['text']
    bool = df_monitoring.loc[store_id, 'workshop2']
    return d[bool]

@app.callback(Output('store-info-workshop3', 'children'),
              [Input('map-view-graph', 'hoverData')])
def update_store_workshop3(hover_store):
    store_id = hover_store['points'][0]['text']
    bool = df_monitoring.loc[store_id, 'workshop3']
    return d[bool]

@app.callback(Output('store-info-spotlights1', 'children'),
              [Input('map-view-graph', 'hoverData')])
def update_store_workshop3(hover_store):
    store_id = hover_store['points'][0]['text']
    bool = df_monitoring.loc[store_id, 'spotlights_received']
    return d[bool]

@app.callback(Output('store-info-spotlights2', 'children'),
              [Input('map-view-graph', 'hoverData')])
def update_store_workshop3(hover_store):
    store_id = hover_store['points'][0]['text']
    bool = df_monitoring.loc[store_id, 'spotlights_placed']
    return d[bool]

@app.callback(Output('store-info-paint1', 'children'),
              [Input('map-view-graph', 'hoverData')])
def update_store_workshop3(hover_store):
    store_id = hover_store['points'][0]['text']
    bool = df_monitoring.loc[store_id, 'paint_received']
    return d[bool]

@app.callback(Output('store-info-paint2', 'children'),
              [Input('map-view-graph', 'hoverData')])
def update_store_workshop3(hover_store):
    store_id = hover_store['points'][0]['text']
    bool = df_monitoring.loc[store_id, 'paint_placed']
    return d[bool]

@app.callback(Output('store-info-cover1', 'children'),
              [Input('map-view-graph', 'hoverData')])
def update_store_workshop3(hover_store):
    store_id = hover_store['points'][0]['text']
    bool = df_monitoring.loc[store_id, 'cover_received']
    return d[bool]

@app.callback(Output('store-info-cover2', 'children'),
              [Input('map-view-graph', 'hoverData')])
def update_store_workshop3(hover_store):
    store_id = hover_store['points'][0]['text']
    bool = df_monitoring.loc[store_id, 'cover_placed']
    return d[bool]


if 'DYNO' in os.environ:
    app.scripts.config.serve_locally = False
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })
else:
    app.scripts.config.serve_locally = True

if __name__ == '__main__':
    app.run_server(debug=True)

