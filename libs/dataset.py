#!/usr/bin/env python
#-*- coding: utf8 -*-



###############################
###############################
#   dataset
###############################
###############################



# hhuiefuiaefzueofea
# fazilfauefaozffazf
# jfizafziafuafziaofa
# fzailflizeoafa
# fhaiufiozfeafoa"""



#########################
#   IMPORTS 
#########################


import pandas as pd
from stockstats import StockDataFrame



#########################
#   CLASS 
#########################


class DataSet(): 

    def __init__(self, filename, name=None, value=None, 
                 curency=None, period=None, interval=None) : 
        u""" aDataset 

        positional args :

            filename :  filename of your CVS file
                        type str, exemple "google.csv",
                        only CSV files suported for now

        optional args :
            name :      arbitrary name of your dataset
                        type str, default is filname without ".csv"

            value :     stock's name, or value/asset you work on
                        type str, exemple "BTC", "Gold", "Google"

            currency :  currency
                        type str, exemple "$", "eur", "BTC"

            period :    period you work on :
                        type str, exemple "01/01/2016 -01/01/18"
                        if "auto" : automatic calculation

            interval :  standard internationnal interval reference
                        D for day H for hour, T for minute


    return :        an DataSet object, based on DataFrame but ehanced of various features"""


        if not name : 
            self.name = filename.replace(".csv")
        else : 
            self.name=name

        if not value : 
            pass # self.value = try_to_get_value(filename)
        else : 
            self.value=value
        
        if not curency : 
            pass # self.curency = try_to_get_curency(filename)
        else : 
            self.curency = curency

        self.data = StockDataFrame.retype(pd.read_csv(filename))

        if not period : 
            pass # self.period = try_to_get_period(filename)
        else :
            self.period = period

        if not interval : 
            pass # self.interval = try_to_get_interval(filename)
        else : 
            self.interval = interval



#########################
#   MAIN
#########################


if __name__ == '__main__':

    ds = DataSet("/home/alex/Bureau/beta_backtrader/datas/accord.csv",
                name="accord_eur_2017_1D", value="accord",
                curency="eur", period="2017", interval="1D")

    print(ds.__dict__.keys())
    print(ds.data.head())
    print(ds.data.shape)
    print(ds.data.columns)
    print(len(ds.data))