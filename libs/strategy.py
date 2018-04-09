#!/usr/bin/env python 
#-*- coding: utf8 -*-



###############################
###############################
#	strategy
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



#########################
#	CLASS
#########################


class Strategy : 

	def __init__(self, name="my_first_strategy", family= "indicator_cross",
					order_type="market", price="close",
					dataset="dataset",
					conditions={"buy": "close_10_sma_xu_close_30_sma", 
								"sell": None, 
								"stop_loss_profit_base": "real",
								"stop_loss": 0.01, "trailing_stop_loss": None,
								"stop_profit":0.04,"trailing_stop_profit":None,
								"universal_waiter": 0, "loss_waiter": None, 
								"profit_waiter": None}) : 


		# strat ID
		self.name 	= name
		self.family = family
		self.order_type = order_type
		self.price = price
		self.df = dataset.data
		# add an indicator for curent trade --> stop loss and stop profit
		
		self.last_buy = 0
		self.curent_price = 0
		self.curent_trade = 0
		
		self.buy_condition = conditions["buy"]
		# if (not conditions["sell"]) or (not isinstance(conditions["sell"], str)) : 
		# 	conditions["sell"] = str(conditions["sell"])
		self.sell_condition = conditions["sell"]

		self.stop_loss_profit_base = conditions["stop_loss_profit_base"]

		self.stop_loss = conditions["stop_loss"]
		self.stop_profit = conditions["stop_profit"]
		self.trailing_stop_loss = conditions["trailing_stop_loss"]
		self.trailing_stop_profit = conditions["trailing_stop_profit"]

		self.universal_waiter = conditions["universal_waiter"]
		self.loss_waiter = conditions["loss_waiter" ]
		self.profit_waiter = conditions["profit_waiter"]

		self.add_needed_indicators()
		#		print(self.df.head())


	def add_needed_indicators(self) : 

		for indicator in [self.buy_condition, self.sell_condition] : 
			if indicator : 
				try : 
					self.df.get(indicator)
				except : 
					self.df["None"] = False
					self.sell_condition = "None"
			else : 
				self.df["None"] = False
				self.sell_condition = "None"




	def says_buy(self, i) : 
		if self.df.loc[i, self.buy_condition] : 
			self.curent_trade = 0.0
			return True, str(self.buy_condition)
		self.curent_trade = 0.0
		return False, None 


	def says_sell(self, i, k) : 
		sell, reason = self.automatic_sell(i,k)
		if sell : 
			return True, reason 
		if self.df.loc[i, self.sell_condition] : 
			return True, str(self.sell_condition)
		return False, None


	def automatic_sell(self, i, k):
		self.curent_trade = k[1] if self.stop_loss_profit_base=="real" else k[0]
		if (self.curent_trade > self.stop_profit) : 
			return True, "stop profit"
		if (-self.curent_trade) > self.stop_loss : 
			return True, "stop loss"
		return False, None
	


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
	from trading_room2 import TradingRoom



	#########################
	#	FUNCTIONS 
	#########################


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


	brk = Broker( name="test_broker", 
				  maker_fees=0.002, 
				  taker_fees=0.004,
				  slipage=0.005)


	stg = Strategy(	name="my_first_strategy", family= "indicator_cross",
					order_type="market", price="close",
					dataset=ds,
					conditions={"buy": "close_10_sma_xu_close_50_sma", 
								"sell": None, 
								"stop_loss_profit_base": "real",
								"stop_loss": 0.5, "trailing_stop_loss": None,
								"stop_profit":0.1,"trailing_stop_profit":None,
								"universal_waiter": None, "loss_waiter": None, 
								"profit_waiter": None})



	usr = User(bank=100, ruined_rate=0.99)


	# launch trading session
	##########################


	trading_session = TradingRoom(dataset=ds, 
								  strategy=stg,
								  broker=brk, 
								  user=usr)

	# _ = raw_input("Go for control prints?\n")


	# control prints
	###################


	# dataset info 
	print_label("Dataset info")
	print(ds.data.iloc[:3, :])
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
	print(ds.data.loc[mask, ["close", "orders", "abs_result", "real_result", "order_signal"]])