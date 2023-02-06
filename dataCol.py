#https://pypi.org/project/yfinance/
import yfinance as yf
import pandas as pd
import csv
import pandas as pd
from datetime import date, timedelta
import openpyxl
import csv
from csv import writer
import sys
import os

def main(first, otherinput):
    path = os.path.join(os.path.dirname(__file__), "stock_data/")
    file_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(file_dir, '/stock_data/')
    print(first)
    k = 0
    n = 0
    check_df = pd.read_csv(r"nasdaq_screener_1658433635358.csv") 
    while n == 0:
        print(first in check_df.values)
        if first in check_df.values:
            check_df = pd.read_csv(r"stock_data.csv", index_col=None)
            if (otherinput + first) in check_df.values: 
                #check if exists
                    pref = input("already exists, would you like to renew? (Y/N) ")
                    if pref == "Y" or pref == "y":
                        break
                    else:
                        k=2
                        break
            else:
                break
        else:
            first = input("Stock doesnt exist, try again")

    while k!=2:
        today = date.today()
        yesterday = date.today() - timedelta(days = 1)
        #with open("stock_data.csv") as csv_file:
            #csv_reader = csv.reader(csv_file, delimiter=",")
            #line_count = 0
            
            

                
        def append_list_as_row(file_name, list_of_elem):
            with open(file_name, "a+", newline = "") as write_obj:
                csv_writer = writer(write_obj)
                csv_writer.writerow(list_of_elem)
            write_obj.close()
        #msft = yf.Ticker("MSFT")
        #hist = msft.history(period="max")

        if "A" or "a" in otherinput:
            tick = yf.Ticker(first)
            data = tick.history(period="15y")
            data["Stock"] = "a"+first
            data = data.drop(columns="Dividends")
            data = data.drop(columns="Stock Splits")

            #index = pd.DataFrame(range(1,len(data)+1))
            #data.insert(0,'ID', index)
            data.insert(0,'Date', data.index.date)
            data.to_csv(path + 'a'+ first + '.csv', index=False, encoding='utf-8')
            df = pd.read_csv("stock_data.csv")
            print(data.iloc[5])
            if "" in df.values:
                df = df[df['Stock'] != ""]
            if first in df.values:
                df = df[df['Stock'] != first]
            df.to_csv(r"stock_data.csv", index=None)
            for i in range(len(data)):
                append_list_as_row(r"stock_data.csv", data.iloc[i])
            print(data.iloc[5])
                
                
        if "Y" or "y" in otherinput:
            data = yf.download(first, start=yesterday, end=today, group_by= "ticker")
            data.to_csv(path + 'y'+ first + '.csv', index=True, encoding='utf-8')
        k = 2
        
        if "C" or "c" in otherinput:
            tick = yf.Ticker(first)
            data = tick.history(period="2y")
            data["Stock"] = first
            data = data.drop(columns="Dividends")
            data = data.drop(columns="Stock Splits")
            #index = pd.DataFrame(range(1,len(data)+1))
            #data.insert(0,'ID', index)
            data.insert(0,'Date', data.index.date)
            data.to_csv(path + 'c'+ first + '.csv', index=False, encoding='utf-8')
            print(data.iloc[1])
            df = pd.read_csv("stock_data.csv")
            if first in df.values:
                df = df[df['Stock'] != first]
                df.to_csv(r"stock_data.csv", index=None)
            for i in range(len(data)):
                append_list_as_row(r"stock_data.csv", data.iloc[i])
                
                
        if "M" or "m" in otherinput:
            tick = yf.Ticker(first)
            data = tick.history(period = "7d", interval = "1m")
            #index = pd.DataFrame(range(1,len(data)+1))
            #data.insert(0,'ID', index)
            data = data.drop(columns="Dividends")
            data = data.drop(columns="Stock Splits")
            data.insert(0,'Date', data.index.date)
            data.to_csv(path + 'm'+ first + '.csv', index=False, encoding='utf-8')
            df = pd.read_csv("stock_data.csv")
            if first in df.values:
                df = df[df['Stock'] != first]
                df.to_csv(r"stock_data.csv", index=None)
            for i in range(len(data)):
                append_list_as_row(r"stock_data.csv", data.iloc[i])
            print(data)
            
            
            
            
            
if __name__ == "__main__":
    first = input("What stock do you want to train?")
    covidYN = input("Covid or Non-Covid data?(Y/N")
    otherinput = input("Do you want Yesterday (Y) or all (A) or covid (C) or minute (M)?")
    main(first, otherinput)
            
            
            
                
            



#column is stock name, double brackets means specific data
