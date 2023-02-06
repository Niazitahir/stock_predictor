import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import sys


def runAPP(first, valid):
    df= pd.read_csv("stock_data.csv")
    app = dash.Dash()
    #include a root call back here. This is doing it too many times
    server = app.server

    app.layout = html.Div([
    
        html.H1("Stock Price Analysis Dashboard", style={"textAlign": "center"}),
    
        dcc.Tabs(id="tabs", children=[
        
            dcc.Tab(label=first +' Stock Data',children=[
                html.Div([
                    html.H2("Actual closing price",style={"textAlign": "center"}),
                    dcc.Graph(
                        id="Actual Data",
                        figure={
                            "data":[
                                go.Scatter(
                                    x=valid.index,
                                    y=valid["Close"],
                                    mode='markers'
                                )

                            ],
                            "layout":go.Layout(
                                title='scatter plot',
                                xaxis={'title':'Date'},
                                yaxis={'title':'Closing Rate'}
                            )
                        }

                    ),
                    html.H2("LSTM Predicted closing price",style={"textAlign": "center"}),
                    dcc.Graph(
                        id="Predicted Data",
                        figure={
                            "data":[
                                go.Scatter(
                                    x=valid.index,
                                    y=valid["Predictions"],
                                    mode='markers'
                                )

                            ],
                            "layout":go.Layout(
                                title='scatter plot',
                                xaxis={'title':'Date'},
                                yaxis={'title':'Closing Rate'}
                            )
                        }

                    )
                ])        		
                    

            ]),
            dcc.Tab(label='Select Stock Data', children=[
                html.Div([
                    html.H1("Stocks High vs Lows", 
                            style={'textAlign': 'center'}),
                    
                    dcc.Dropdown(id='my-dropdown',
                                options=[{'label': 'Tesla', 'value': 'TSLA'},
                                        {'label': 'Apple','value': 'AAPL'}, 
                                        {'label': 'Facebook', 'value': 'FB'}, 
                                        {'label': 'Microsoft','value': 'MSFT'}], 
                                multi=True,value=['FB'],
                                style={"display": "block", "margin-left": "auto", 
                                        "margin-right": "auto", "width": "60%"}),
                    dcc.Graph(id='highlow'),
                    html.H1("Stocks Market Volume", style={'textAlign': 'center'}),
            
                    dcc.Dropdown(id='my-dropdown2',
                                options=[{'label': 'Tesla', 'value': 'TSLA'},
                                        {'label': 'Apple','value': 'AAPL'}, 
                                        {'label': 'Facebook', 'value': 'FB'},
                                        {'label': 'Microsoft','value': 'MSFT'}], 
                                multi=True,value=['FB'],
                                style={"display": "block", "margin-left": "auto", 
                                        "margin-right": "auto", "width": "60%"}),
                    dcc.Graph(id='volume')
                ], className="container"),
            ])


        ])
    ])







    @app.callback(Output('highlow', 'figure'),
                [Input('my-dropdown', 'value')])
    def update_graph(selected_dropdown):
        dropdown = {"TSLA": "Tesla","AAPL": "Apple","FB": "Facebook","MSFT": "Microsoft",}
        trace1 = []
        trace2 = []
        arg = ""
        for stock in selected_dropdown:
            if ("a"+ stock) in df.values:
                arg = "a"
            elif ("c" + stock) in df.values:
                arg = "b"
            elif ("y" + stock) in df.values:
                arg = "y"
            trace1.append(#x and y values based on stock_data.csv, i.e high values
            go.Scatter(x=df[df["Stock"] == (arg + stock)]["Date"],
                        y=df[df["Stock"] == (arg + stock)]["High"],
                        mode='lines', opacity=0.7, 
                        name=f'High {dropdown[stock]}',textposition='bottom center'))
            trace2.append(#appended low values
            go.Scatter(x=df[df["Stock"] == (arg + stock)]["Date"], #only use stock values which = chosen stock. kinda ingenius
                        y=df[df["Stock"] == (arg + stock)]["Low"],
                        mode='lines', opacity=0.6,
                        name=f'Low {dropdown[stock]}',textposition='bottom center'))
        traces = [trace1, trace2]#put em together in a dictionary
        data = [val for sublist in traces for val in sublist]
        figure = {'data': data,
                'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
                                                '#FF7400', '#FFF400', '#FF0056'],
                height=600,
                title=f"High and Low Prices for {', '.join(str(dropdown[i]) for i in selected_dropdown)} Over Time",
                xaxis={"title":"Date",
                    'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
                                                        'step': 'month', 
                                                        'stepmode': 'backward'},
                                                        {'count': 6, 'label': '6M', 
                                                        'step': 'month', 
                                                        'stepmode': 'backward'},
                                                        {'step': 'all'}])},
                    'rangeslider': {'visible': True}, 'type': 'date'},
                yaxis={"title":"Price (USD)"})}
        return figure


    @app.callback(Output('volume', 'figure'),
                [Input('my-dropdown2', 'value')])
    def update_graph(selected_dropdown_value):
        dropdown = {"TSLA": "Tesla","AAPL": "Apple","FB": "Facebook","MSFT": "Microsoft",}
        trace1 = []
        for stock in selected_dropdown_value:
            trace1.append(
            go.Scatter(x=df[df["Stock"] == stock]["Date"],
                        y=df[df["Stock"] == stock]["Volume"],
                        mode='lines', opacity=0.7,
                        name=f'Volume {dropdown[stock]}', textposition='bottom center'))
        traces = [trace1]
        data = [val for sublist in traces for val in sublist]
        figure = {'data': data, 
                'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', 
                                                '#FF7400', '#FFF400', '#FF0056'],
                height=600,
                title=f"Market Volume for {', '.join(str(dropdown[i]) for i in selected_dropdown_value)} Over Time",
                xaxis={"title":"Date",
                    'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
                                                        'step': 'month', 
                                                        'stepmode': 'backward'},
                                                        {'count': 6, 'label': '6M',
                                                        'step': 'month', 
                                                        'stepmode': 'backward'},
                                                        {'step': 'all'}])},
                    'rangeslider': {'visible': True}, 'type': 'date'},
                yaxis={"title":"Transactions Volume"})}
        return figure
    app.run_server()