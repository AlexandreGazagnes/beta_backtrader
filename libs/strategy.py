#!/usr/bin/env python 
#-*- coding: utf8 -*-




###############################
#	strategy.py
###############################

stg = Strategy(	name="my_first_strategy", 
				family= "indicator_cross", 
				dataset=df,
				conditions={"buy" : "close_10_sma_xu_close_30_sma", 
							"sell": None, 
							"stop_loss" : 0.01, 
							"stop_profit" : 0.04, 
							"waiter": 0})

class Strategy : 

		def __init__(self, name, family, dataset, **conditions)

		# strat ID
		self.name 	= name
		self.family = family

		# manage conditions
		try : self.buy = conditions["buy"]
		except : raise ValueError("error conditions strategy, not good Buy so Goodbye")
		
		if (not ("sell" or "stop_profit")) in conditions.keys() : 
			raise : ValueError("error conditions strategy, not good Sell")
		else : 
			try : self.sell = conditions["sell"]
			except: self.sell = None
			try  : self.stop_profit = conditions["stop_profit"]

		try : self.stop_loss = conditions["stop_loss"]
		except: self.stop_loss = -1.1
		
		try : self.waiter = conditions["waiter"]
		except : self.waiter = 0

		# add an indicator for curent trade --> stop loss and stop profit
		self.last_buy = 0
		self.curent_price = 0
		self.curent_trade = 0
		

		# try to add technicals indicators
		if self.buy : 
			try : dataset[self.buy]
			except : raise ValueError("error conditions strategy, not good Buy so Goodbye")

		if self.sell : 
			try : dataset[self.sell]
			except : raise : ValueError("error conditions strategy, not good Sell")
			


	def eval_curent_trade() : 
		self.curent_price = dataset.loc[i, "close"]
		if self.curent_price > self.last_buy : 
			self.curent_trade = (self.curent_price - self.last_buy) / self.last_buy
		elif  self.curent_price > self.last_buy : 
			self.curent_trade = - (self.last_buy - self.curent_price ) / self.last_buy
		else : 
			self.curent_trade = 0



	def strat_say_buy(i) : 
		if dataset.loc[i, self.buy] : 
			self.last_buy = dataset.loc[i, "close"]
			return True
		else : return False 


	def start_say_sell(i) : 
		eval_curent_trade()
		if self.curent_trade > self.stop_profit : return True
		elif (-self.curent_trade) > self.stop_loss : return True
		elif dataset.loc[i, self.sell] : return True
		else : return False 




