#!/usr/bin/env python
#-*- coding: utf8 -*-



###############################
###############################
#	tradingroom
###############################
###############################



# hhuiefuiaefzueofea
# fazilfauefaozffazf
# jfizafziafuafziaofa
# fzailflizeoafa
# fhaiufiozfeafoa"""



#########################
#	IMPORTS 
#########################


from __future__ import division

import pandas as pd
from stockstats import StockDataFrame
import numpy as np



#########################
#	CLASS
#########################


class TradingRoom() : 


	def __init__(self, dataset, strategy, broker, user, 
				 stop_ruined=True, close_pos_last_round=False) :
		
		# import dataset
		self.df = dataset.data

		# import strategy
		self.price = strategy.price
		if strategy.order_type == "limit" : self.fees = broker.maker_fees 
		else : self.fees = broker.taker_fees
		self.stg_says_buy = strategy.says_buy
		self.stg_says_sell = strategy.says_sell

		# import broker
		self.slipage = broker.slipage

		# import user 
		self.bank = user.bank
		self.ruined_rate = user.ruined_rate

		# import bool values 
		self.close_pos_last_round = close_pos_last_round
		self.stop_ruined = stop_ruined

		# main 
		self.prepare_for_trading()
		self.run_trading_session()
		self.add_session_results()


	def prepare_for_trading(self) : 
		self.df["orders"]= np.int8(0)
		self.df["abs_result"] = np.float16(0.0)
		self.df["real_result"] = np.float16(0.0)
		self.df["broker_price"] = np.float16(0.0)
		self.df["quantity"] = np.float16(0.0)
		self.df["fees"] = np.float16(0.0)
		self.df["bank"] = np.float16(0.0)
		self.df["portfolio"] = np.float16(0.0)
		self.df["total"] = np.float16(0.0)
		self.df["order_signal"] = "None"

		self.df.loc[0, "bank"]=self.df.loc[0, "total"] = np.float16(self.bank)

		self.last_order_type = -1
		self.last_order_round = -1

		self.ruined=False
		self.ruined_round = None 
		self.limit_ruined = self.bank - (self.bank * self.ruined_rate)


	def run_trading_session(self) : 
		end = len(self.df)
		if self.stop_ruined : 
			for i  in xrange(1, end) : 
				self.run_trading_round(i)
				if self.df.loc[i, "total"] < self.limit_ruined : 
					self.ruined_round = i 
					self.ruined = True
					break
		else :  
			for i  in xrange(1, end) : 
				self.run_trading_round(i)


	def run_trading_round(self, i) : 
		has_to_buy, reason = self.stg_says_buy(i)
		self.df.loc[i, "order_signal"] = reason
		if self.last_order_type == -1 and has_to_buy: 
			self.buy(i)
		elif self.last_order_type == 1 : 
			self.define_broker_price_buy(i)
			results = self.estimate_trade_results(i)
			has_to_sell, reason = self.stg_says_sell(i, results)
			self.df.loc[i, "order_signal"] = reason
			if has_to_sell : 
				self.sell(i)
			else : 
				self.do_nothing(i)
		else : 
			self.do_nothing(i)


	def buy(self, i) :
		self.define_broker_price_buy(i)
		self.exchange_buy(i)
		self.update_orders_buy(i)
		self.update_portfolio(i)
		self.update_total(i)


	def sell(self, i) : 
		self.exchange_sell(i)
		self.update_orders_sell(i)
		self.update_portfolio(i)
		self.update_total(i)

	def update_orders_buy(self,i) :  
		self.df.loc[i,"orders"] =  self.last_order_type = 1
		self.last_order_round = i

		
	def define_broker_price_buy(self,i) : 
		self.df.loc[i, "broker_price"] =   self.df.loc[i, self.price] \
										 * (1+self.slipage)


	def update_orders_sell(self, i) : 
		self.df.loc[i,"orders"] = self.last_order_type = -1
		self.last_order_round = i


	def define_broker_price_sell(self, i) : 
		self.df.loc[i, "broker_price"] = 	 self.df.loc[i, self.price] \
										  * (1-self.slipage)


	def exchange_buy(self, i) : 
		self.df.loc[i, "bank"] = self.df.loc[i-1, "bank"]

		self.df.loc[i, "fees"] = self.df.loc[i, "bank"] * self.fees
		self.df.loc[i, "bank"] -= self.df.loc[i, "fees"]
		self.df.loc[i, "quantity"] = 	self.df.loc[i, "bank"] \
									  / self.df.loc[i, "broker_price"]
		self.df.loc[i, "bank"] = 0


	def exchange_sell(self, i) : 
		self.df.loc[i, "quantity"] = self.df.loc[i-1, "quantity"]
		self.df.loc[i, "fees"] = 	self.df.loc[i, "quantity"] \
								  * self.df.loc[i, self.price] \
								  * self.fees
		cash = self.df.loc[i, "quantity"] * self.df.loc[i, "broker_price"]
		cash -= self.df.loc[i, "fees"]
		self.df.loc[i, "bank"] = cash
		self.df.loc[i, "quantity"] = 0


	def estimate_trade_results(self, i, ) : 
		open_price = self.df.loc[self.last_order_round, self.price]
		close_price = self.df.loc[i, self.price]
		if close_price > open_price : 
			self.df.loc[i, "abs_result" ] = round(	(close_price - open_price)\
												   / open_price, 4)
		else :
			self.df.loc[i, "abs_result" ] = round( -(open_price - close_price)\
												   / open_price, 4)

		open_total = self.df.loc[self.last_order_round, "total"]
		close_total = self.df.loc[i-1, "quantity"] \
					* self.df.loc[i, "broker_price"] \
					* (1 - self.slipage) \
					* (1 - self.fees)

		if close_total > open_total : 
			self.df.loc[i, "real_result" ] = round(	(close_total - open_total)\
												   / open_total, 4)
		else :
			self.df.loc[i, "real_result" ] = round( -(open_total - close_total)\
												   / open_total, 4)

		return self.df.loc[i, "abs_result" ], self.df.loc[i, "real_result" ]



	def update_portfolio(self, i) : 
		self.df.loc[i, "portfolio"] =	self.df.loc[i, "quantity"] \
									  * self.df.loc[i, self.price]


	def update_total(self, i) :
		self.df.loc[i, "total"] = 	self.df.loc[i, "portfolio"]\
								  + self.df.loc[i, "bank"]


	def do_nothing(self, i) : 
		self.df.loc[i, "bank"] = self.df.loc[i-1, "bank"]
		self.df.loc[i, "quantity"] = self.df.loc[i-1, "quantity"]
		self.update_portfolio(i)
		self.update_total(i)


	def add_session_results(self) : 
		self.results = dict()

		first = self.df.loc[0, self.price]
		last = self.df.loc[self.df.shape[0]-1, self.price]
		if last > first : 
			self.results["market"] = round((last - first) / first,4)
		else : 
			self.results["market"] = round(-(first - last) / first,4)

		first = self.df.loc[0, "total"]
		last = self.df.loc[self.df.shape[0]-1, "total"]
		if last > first : 
			self.results["strat"] = round((last - first) / first,4)
		else : 
			self.results["strat"] = round(-(first - last) / first,4)

		self.results["strat_vs_market"] = "not implemented"
		self.results["cum_fees"] = round(self.df.fees.sum(),2)
		self.results["nb_pos_trades"] = self.df.shape[0]/2
		self.results["nb_tot_trades"] = len(self.df.loc[self.df.orders !=0]) / 2

		ser = self.df.abs_result[self.df.orders == -1]
		self.results["win_abs_trades"] = len(ser[ser>0])
		
		ser = self.df.real_result[self.df.orders == -1]
		self.results["win_real_trades"] = len(ser[ser>0])

		self.results["ruined"] = self.ruined
		self.results["ruined_round"] = self.ruined_round

		cat = str()
		cat += "+" if (self.results["strat"] > self.results["market"]) else "-"
		cat += "+" if (self.results["strat"] > 0) else "-"
		cat += "+" if (self.results["market"] > 0) else "-"
		self.results["category"] = cat


	def print_results(self) : 
		tsr = self.results
		ordered_results = [("Global"," "), 
							("category", tsr["category"]), 
							("strat",tsr["strat"]),
							("market",tsr["market"]),
							("strat_vs_market",tsr["strat_vs_market"]),
							("\nTrades detail"," "),
							("win_abs_trades",tsr["win_abs_trades"]),
							("win_real_trades",tsr["win_real_trades"]),
							("nb_tot_trades",tsr["nb_tot_trades"]),
							("nb_pos_trades",tsr["nb_pos_trades"]),
							("cum_fees",tsr["cum_fees"]),
							("\nRuined info"," "),
							("ruined",tsr["ruined"]),
							("ruined_round",tsr["ruined_round"])]
					
		for k,v in ordered_results : 
			print("{} : {}".format(k,v))


	def __repr__(self) : 
		txt = str()
		for k,v in self.__dict__.items() : 
			txt +=("{} : {}\n".format(k, str(v)[:400]))
		return txt



#########################
#	MAIN
#########################


if __name__ == '__main__':



	#########################
	#	IMPORTS 
	#########################


	from user import User
	from broker import Broker
	from dataset2 import DataSet



	#########################
	#	CLASS
	#########################


	# just build a pseudo and dumb Strategy 
	class Strategy : 
		def __init__(self, order_type, price) : 
			self.order_type = order_type
			self.price = price

		def says_buy(self, i) : 
			if  not i%3:
				return True, "signal"
			else :
				return False, "None"

		def says_sell(self, i, results) : 
			if not i%13 : 	 
				return True, "signal"
			else : 
				return False, "None"


	#########################
	#	FUNCTIONS 
	#########################


	# just for a easy readable text
	def print_label(label) : 
		print("\n\n############################################")
		print("\t{}".format(label))
		print("############################################\n")

	

	#########################
	#	MAIN 
	#########################


	# initiate objects
	###################


	ds = DataSet("/home/alex/Bureau/beta_backtrader/datas/accord.csv", 
				name="accord_eur_2017_1D", value="accord", 
				curency="eur", period="2017", interval="1D") 


	brk = Broker(name="test_broker", 
				  maker_fees=0.002, taker_fees=0.004,
				  slipage=0.005)


	stg = Strategy(order_type="market", price="close")


	usr = User(bank=100, ruined_rate=0.99)



	# launch trading session
	#########################


	trading_session = TradingRoom(dataset=ds, 
								  strategy=stg,
								  broker=brk, 
								  user=usr)

	#_ = raw_input("Go for control prints?\n")

	
	# control prints
	###################


	# dataset info 
	print_label("Dataset info")
	print(ds.data.iloc[:10, :])
	print(ds.data.iloc[-3:, :])

	
	# trading session info 
	print_label("trading session info")
	print(trading_session)


	# trading session results
	print_label("trading session results")
	trading_session.print_results()




	# trading session orders
	print_label("trading session orders")
	mask = ds.data.loc[:, "orders"] != 0
	print(ds.data.loc[mask, ["close", "orders", "abs_result", "real_result"]])