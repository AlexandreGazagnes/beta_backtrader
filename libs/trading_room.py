#!/usr/bin/env python
#-*- coding: utf8 -*-



# TradingRoom is the market place simulator



# 	IMPORT

from __future__ import division

import pandas as pd
from stockstats import StockDataFrame
import numpy as np



# CLASS

class TradingRoom() : 

	def __init__(self, dataset, strategy, broker) :

		_dataset = pd.DataFrame({"close" : dataset["close"]})

		# add fieds 
		_dataset["orders"]= np.int8(0)
		_dataset["broker_price"] = np.float16(0.0)
		_dataset["quantity"] = np.float16(0.0)
		_dataset["fees"] = np.float16(0.0)
		_dataset["bank"] = np.float16(0.0)
		_dataset.loc[0, "bank"]=np.float16(100.0)
		_dataset.loc[1, "bank"]=np.float16(100.0)
		_dataset["portfolio"] = np.float16(100.0)


		self.last_order = -1


		# eval if buy or sell
		for i in _dataset.index : 
			if self.last_order == -1 and strat_says_buy(i) : 
					_dataset.loc[i, "orders"] =  self.last_order = 1
			elif self.last_order == 1 and strat_says_sell(i) : 
					_dataset.loc[i, "orders"] = self.last_order = -1
			else : 
				_dataset.loc[i, "orders"] = np.nan

		# set broker price
		for i in _dataset.index	: 
			if _dataset.loc[i, "orders"] == 1 : 
				_dataset.loc[i, "broker_price"] = _dataset.loc[i, "close"] * (1+broker.slipage)
			elif _dataset.loc[i, "orders"] == -1 : 
				_dataset.loc[i, "broker_price"] = _dataset.loc[i, "close"] * (1-broker.slipage)
			else :
				_dataset.loc[i, "broker_price"] = np.nan

		# eval orders consequences 
		for i in _dataset.index :

			if not i : continue 
			
			_dataset.loc[i, "bank"] = _dataset.loc[i-1, "bank"]
			_dataset.loc[i, "quantity"] = _dataset.loc[i-1, "quantity"]

			
			if (_dataset.loc[i, "portfolio"] < 1.0) and (broker.stop_ruined) :
				raise ValueError("You are ruined at run n* {}!!!!".format(i))
				print("ruined!") 
				break 
			
			if _dataset.loc[i, "orders"] == 1 : 
				_dataset.loc[i, "fees"] = _dataset.loc[i, "bank"] * broker.fees
				_dataset.loc[i, "bank"] -= _dataset.loc[i, "fees"]
				_dataset.loc[i, "quantity"] = _dataset.loc[i, "bank"] / _dataset.loc[i, "broker_price"]
				_dataset.loc[i, "bank"] = 0
				_dataset.loc[i, "portfolio"] = _dataset.loc[i, "quantity"] * _dataset.loc[i, "close"] + _dataset.loc[i, "bank"]
			elif _dataset.loc[i, "orders"] == -1 : 
				_dataset.loc[i, "fees"] = _dataset.loc[i, "quantity"] * _dataset.loc[i, "close"] * broker.fees
				cash = _dataset.loc[i, "quantity"] * _dataset.loc[i, "broker_price"]
				cash -= _dataset.loc[i, "fees"]
				_dataset.loc[i, "bank"] = cash
				_dataset.loc[i, "portfolio"], _dataset.loc[i, "quantity"] = _dataset.loc[i, "bank"], 0
			else :
				_dataset.loc[i, "fees"] == np.nan
				_dataset.loc[i, "portfolio"] = _dataset.loc[i, "quantity"] * _dataset.loc[i, "close"] +  _dataset.loc[i, "bank"]



		dataset["orders"] = _dataset.loc[:,"orders"]
		dataset["broker_price"] = _dataset.loc[:,"broker_price"]
		dataset["quantity"] = _dataset.loc[:,"quantity"]
		dataset["fees"] = _dataset.loc[:,"fees"]
		dataset["bank"] = _dataset.loc[:,"bank"]
		dataset["bank"] = _dataset.loc[:,"bank"]
		dataset["bank"] = _dataset.loc[:,"bank"]
		dataset["portfolio"] = _dataset.loc[:,"portfolio"]

def strat_says_sell(i) : 
	if not i % 11  : 
		return True
	else : 
		return False

def strat_says_buy(i) : 
	if i > 3 : 
		return True
	else :
		return False