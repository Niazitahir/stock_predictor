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
from stock_app import runAPP
import webbrowser

from stock_pred import yeet 
n = 0
while n == 0:
    print("STARTING")
    first = input("What stock do you want to train? ")
    otherinput = input("Do you want Yesterday (Y) or all(A) or covid(C)? ")
    check_df = pd.read_csv("nasdaq_screener_1658433635358.csv")
    if first in check_df.values:
        yeet(first, otherinput)
        break
    else:
        print("Not correct")


#FIND A WAY TO INPUT AUTOMATICALLY INTO DATACOL AND SUBSEQUENT INPUTS

app = dash.Dash()
#include a root call back here. This is doing it too many times
server = app.server



df_nse = pd.read_csv(r"stock_data.csv")
df_nse = df_nse[df_nse['Stock'] == (otherinput + first)]
halflen = int(len(df_nse)/2)
df_nse["Date"]=pd.to_datetime(df_nse.Date,format="%Y-%m-%d")
df_nse.index=df_nse['Date']
data=df_nse.sort_index(ascending=True,axis=0)
new_data=pd.DataFrame(index=range(0,len(df_nse)),columns=['Date','Close'])

for i in range(0,len(data)):
    new_data["Date"][i]=data['Date'][i]
    new_data["Close"][i]=data["Close"][i]

new_data.index=new_data.Date
new_data.drop("Date",axis=1,inplace=True)

dataset=new_data.values

train=dataset[0:halflen,:]
valid=dataset[halflen:,:]

scaler=MinMaxScaler(feature_range=(0,1))
scaled_data=scaler.fit_transform(dataset)
print(scaled_data)
x_train,y_train=[],[]

for i in range(60,len(train)):
    x_train.append(scaled_data[i-60:i,0])
    y_train.append(scaled_data[i,0])
    
x_train,y_train=np.array(x_train),np.array(y_train)

x_train=np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))

first = otherinput + first
model=load_model(r"saved_lstm_models/saved_lstm_model"+first+".h5")

inputs=new_data[len(new_data)-len(valid)-60:].values
inputs=inputs.reshape(-1,1)
inputs=scaler.transform(inputs)
X_test=[]
for i in range(60,inputs.shape[0]):
    X_test.append(inputs[i-60:i,0])
X_test=np.array(X_test)

X_test=np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))
closing_price=model.predict(X_test)
closing_price=scaler.inverse_transform(closing_price)

train=new_data[:halflen]
valid=new_data[halflen:]
valid['Predictions']=closing_price




df = pd.DataFrame(valid)
df.insert(2, "first", first)
df.to_csv("valid-data.csv")
print("Please go to your web browser of choice and type http://127.0.0.1:8050/ into the url and allow the code some time to initialize the dashboard.")
runAPP(first, valid)
