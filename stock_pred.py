#%%
from calendar import EPOCH
from turtle import color
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM,Dropout,Dense
from sklearn.preprocessing import MinMaxScaler, scale
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
# importing sys
import sys
 
# adding Folder_2 to the system path
 
# importing the add and odd_even
# function
from dataCol import main
def yeet(first, otherinput):
    main(first, otherinput)

    k = 1

    rcParams['figure.figsize']=20,10
    #Read dataset
    check_df = pd.read_csv(r"All_models.csv")

    """if first in check_df.values:
        pref = input("model already trained, would you like to retrain?")
        if pref == "N" or pref == "n":
            k = 2"""
    while k == 1:
        df=pd.read_csv("stock_data\\" + otherinput + first+".csv")
        df["Date"]=pd.to_datetime(df.Date,format="%Y-%m-%d")
        df.index=df['Date']

        plt.figure(figsize=(16,8))
        plt.plot(df["Close"],label='Close Price history')


        data=df.sort_index(ascending=True,axis=0) #sort by date

        new_dataset=pd.DataFrame(index=range(0,len(df)),columns=['Date','Close']) #new dataset without values of len(df) and with two columns


        for i in range(0,len(data)):
            new_dataset["Date"][i]=data['Date'][i]
            new_dataset["Close"][i]=data["Close"][i] #fill dataset with values 
        new_dataset.to_csv("new.csv")
        new_dataset.index=new_dataset.Date
        new_dataset.drop("Date",axis=1,inplace=True)#remove dates cause why not

        halflen = int(len(df)/2)
        final_dataset=new_dataset.values #make em all values rather than... non values? You get it, i swear to god if you dont imma hit you upside the head AHHHHHHH
        train_data=final_dataset[0:halflen,:]#take first 987
        valid_data=final_dataset[halflen:,:]#remaining go to hell

        scaler=MinMaxScaler(feature_range=(0,1)) #makes everything between 0 and 1
        scaled_data=scaler.fit_transform(final_dataset)

        x_train_data,y_train_data=[],[]

        for i in range(60,len(train_data)):
            x_train_data.append(scaled_data[i-60:i,0])
            y_train_data.append(scaled_data[i,0])
            
        x_train_data,y_train_data=np.array(x_train_data),np.array(y_train_data)

        x_train_data=np.reshape(x_train_data,(x_train_data.shape[0],x_train_data.shape[1],1))
        lstm_model=Sequential()
        lstm_model.add(LSTM(units=50,return_sequences=True,input_shape=(x_train_data.shape[1],1)))
        lstm_model.add(LSTM(units=50))
        lstm_model.add(Dense(1))
        
        #add backpropagation

        lstm_model.compile(loss='mean_squared_error',optimizer='adam')
        lstm_model.fit(x_train_data,y_train_data,epochs=1,batch_size=1,verbose=2)

        inputs_data=new_dataset[len(new_dataset)-len(valid_data)-60:].values
        inputs_data=inputs_data.reshape(-1,1)
        inputs_data=scaler.transform(inputs_data)


        X_test=[]
        for i in range(60,inputs_data.shape[0]):
            X_test.append(inputs_data[i-60:i,0])
        X_test=np.array(X_test)

        X_test=np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))
        closing_price=lstm_model.predict(X_test)
        closing_price=scaler.inverse_transform(closing_price)

        lstm_model.save(r"saved_lstm_models/saved_lstm_model"+otherinput+first+".h5")

        train_data=new_dataset[:halflen]
        valid_data=new_dataset[halflen:]
        valid_data['Predictions']=closing_price
        plt.plot(train_data["Close"], label='Train Price history')
        plt.plot(valid_data["Predictions"], label='Predicted Price history', color = "black")
        plt.legend()
        plt.show()
        file = open("All_models.csv")
        currentlen = len(file.readlines())
        check_df[currentlen+1] = first
        check_df.to_csv(r"All_models.csv", index = False)
        k = 2
if __name__ == "__main__":
    first = input("What stock do you want to train?")
    covidYN = input("Covid or Non-Covid data?(Y/N")
    otherinput = input("Do you want Yesterday (Y) or all(A) or covid(C)?")
    yeet(first, covidYN, otherinput)

    # %%
