#!/usr/bin/env python
#-*- coding: utf8 -*-


###############################
#	dataset.py
###############################


#
#
#
#
#


###############################
# 	IMPORT
###############################


import bokeh.plotting as bkp
import bokeh.layouts as bkl
import os
import pandas as pd
from stockstats import StockDataFrame


##############################
# 	CLASS
###############################


class _DataSet(pd.DataFrame):
    """pandas Dataset : collection of data from an ohlc file"""

    def __init__(self, data_dict, filename, name, value, curency,	period, interval):

        pd.DataFrame.__init__(self, data_dict)
        self.filename = filename
        self.name = filename.replace(".csv", "")
        self.value = value
        self.curency = curency
        self.period = period
        self.interval = interval
        self.desc = "{} in {} for {} in {}".format(value, curency, period, interval)
        self.main_indicators = dict()
        self.other_indicators = dict()
        self.orders = list()
        self.result = (self["close"].iloc[-1] - self["close"].iloc[0])/self["close"].iloc[0] \
            if self["close"].iloc[-1] > self["close"].iloc[0] \
            else -(self["close"].iloc[0] - self["close"].iloc[-1])/self.close[0]

    def add_indicator(self, name, val, main=True):
        if main:
            self.main_indicators[name] = [val]
        else:
            self.other_indicators[name] = [val]

    def add_orders(self, buy, sell):
        self["buy"] = pd.Series(buy)
        self["sell"] = pd.Series(sell)
        self.orders = ["buy", "sell"]

    def add_ma(self, period, mode="s", base="close"):
        u""" add one or various standard/exponentiel moving average to self (df.DataFrame)

        positional args :
                period :    period to calulate ma
                                        type int for one ma or list of int for various ma

        optional args :
                mode :      standard, or exponential moving average (or both)
                                        type str "s" for std, "e" for exp, "b" for both

                base :      value based caluclation
                                        type str "open", "high", "low", "close", "middle"
                                        or "o", "h", "l", "c", "m"

        return :        none, add expected attribute(s) to self + update self.inidcators
        """

        stock = StockDataFrame.retype(self)

        # manage period argument
        if type(period) != list:
            period = [period]
        for p in period:
            if not (type(p) == int and 0 <= p <= 10000):
                raise ValueError("int expected")

        # manage mode argument
        if mode not in ["s", "e", "b", "std", "exp", "both"]:
            raise ValueError("s, e, b expected")
        mode = [mode]
        if mode[0] == ("b" or "both"):
            mode = ["e", "s"]

        # manage base argument
        base_dict = {"o": "open", "h": "high", "l": "low", "c": "close", "m": "middle"}
        if base not in (base_dict.keys() + base_dict.values()):
            raise ValueError("o, h, l, c, m expected")
        if base in base_dict.keys():
            base = base_dict[base]

        indicator_list = list()
        # add ma(s) regading given arguments
        for m in mode:
            for p in period:
                att = "{}_{}_{}".format(base, p, m+"ma")
                self[att] = stock.get(att).round(2)
                indicator_list.append(att)
        self.main_indicators["ma"] = indicator_list

    def add_bollingers(self):

        stock = StockDataFrame.retype(self)
        self["boll"] = stock['boll'].round(2)
        self.main_indicators["bollingers"] = ["boll_ub", "boll_lb"]

    def add_cross(self, indicator_1, indicator_2, option=""):

        stock = StockDataFrame.retype(self)
        att = indicator_1 + "_x" + option + "_" + indicator_2

        self[att] = stock.get(att)
        self.main_indicators["cross"] = [att]

    def add_macd(self, spec=""):
        u""" add MACD value, signal or Histogram to self (df.DataFrame)

        optional args :
                spec :      MACD's type
                                        type str or list of str: "v" for value, "s" for signal line, "h" for histogram
                                        default or "a"or "all": all
                                        spec = "" or spec = "v"

        return :        none, add expected attribute(s) to self + update self.indicators
        """

        stock = StockDataFrame.retype(self)
        indicator_list = list()

        self["macds"] = stock["macds"].round(2)
        self["macdh"] = stock["macdh"].round(2)

        indicator_list.append("macd")
        if spec:
            indicator_list.append("macd_" + spec)

        self.other_indicators["macd"] = indicator_list

    def add_rsi(self, period):
        u""" add RSI value,for one or various period

        positional
         args :
                period :    MACD's type
                                        type int or list of int

        return :        none, add expected attribute(s) to self + update self.other_indicators
        """

        stock = StockDataFrame.retype(self)
        indicator_list = list()

        if type(period) != list:
            period = [period]
        for p in period:
            att = "{}_{}".format("rsi", p)
            self[att] = stock.get(att).round(2)
            indicator_list.append(att)
        self.other_indicators["rsi"] = indicator_list

    def add_volatiliy():  #  MSTD: moving standard deviation or MVAR: moving variance
        pass

    def add_stochastic():  # RSV or KDJ
        pass

    def add_vvr():  # VR: Volatility Volume Ratio
        pass


###############################
# 	FUNCTIONS
###############################


def DataSet(filename, name="", value="", curency="", period="", interval=""):
    u""" add standard or exponentiel moving average to self.stock

    positional args :

            filename :	filename of your CVS file
                                    type str, exemple "google.csv",
                                    only CSV files suported for now

    optional args :
            name : 		arbitrary name of your dataset
                                    type str, default is filname without ".csv"

            value :     stock's name, or value/asset you work on
                                    type str, exemple "BTC", "Gold", "Google"

            currency : 	currency
                                    type str, exemple "$", "eur", "BTC"

            period : 	period you work on :
                                    type str, exemple "01/01/2016 -01/01/18"
                                    if "auto" : automatic calculation

            interval :	standard internationnal interval reference
                                    D for day H for hour, T for minute


    return :        an DataSet object, based on DataFrame but ehanced of various features"""

    # manage args
    if not os.path.isfile(filename):
        raise ValueError("file not found in {}".format(path))
    if not ".csv" in filename:
        raise ValueError("only CSV file suported for now")

    # call the _DataSet consturctor
    return _DataSet(	pd.read_csv(filename).to_dict(),
                     filename, name, value, curency,
                     period, interval)
