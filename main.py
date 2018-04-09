#!/usr/bin/env python
#-*- coding: utf8 -*-

from __future__ import absolute_import, division


##############################
##############################

#	beta_backtrader v1.0.0

##############################
##############################



##############################
#   IMPORT
##############################

import os

from pprint import pprint
from collections import OrderedDict

from libs.dataset import *
from libs.graph import *
from libs.results import *
from libs.indicators import *
from libs.arg_manager import *
from libs.broker import *
from libs.trading_room import *



##############################
#		CONSTANTS
##############################


DEFAULT_FILE = "datas/test.csv"



##############################
#		FUNCTIONS
##############################


def return_filelist(args): # should use specific package import file or IO
	u""" build a list with default, specific file(s) regarding user input
	positional args :   arg container from arg_manager (argparse)
	optional args :     - 
	return :            list with one or more filenames to work on
	"""

	if args.folder :
		if args.folder[-1] != "/": args.folder += "/"
		file_list = [i for i in os.listdir(args.folder) if ".csv" in i]
		return [str(args.folder+i) for i in file_list]
	elif args.filename :
		return [args.filename]
	else :
		return [DEFAULT_FILE]


def add_indicators():
		# add various indicators
		# ds.add_ma([30, 60], mode="e", base="close")
		# ds.add_macd()
	ds.add_bollingers()
	ds.add_rsi(period=[10, 12, 18])
	# ds.add_cross("close_30_ema", "close_60_ema")


def control_prints(ds):
	u"""put in there your controls prints
	positional args :   - 
	optional args :     - 
	return :            - but print in cli resquested outputs
	"""
	
	print(ds.head(10))
	print(ds.tail(10))


def graph_if_needed(args,ds):
	u"""build and print graph if need regarding user input
	poitional agrs :    arg container from args_manager (argparse)
	optional args :     - 
	return  :           - but open a web browser tab with requetested graph
	"""

	if args.graph: build_graph(ds=ds, option="line")


def main():

	# manage args
	args = arg_manager()
	file_list = return_filelist(args)

	# initaite Result Manager
	rslt = Result()

	for filename in file_list:

		# initiate all parameters
		ds = DataSet(filename, value="", curency="", period="",
					 interval="")


		brk = Broker( name="kraken", order_ref="close", 
					  order_type="market",
					  fees=0.002, slipage=0.002)

		
		stg = Strategy(	name="my_first_strategy", 
						family= "indicator_cross", 
						dataset=ds,
						conditions={"buy" : "close_10_sma_xu_close_30_sma", 
									"sell": None, 
									"stop_loss" : 0.01, 
									"stop_profit" : 0.04, 
									"waiter": 0})


		# trading simulation, adding datas to stg and ds
		tdg = TradingRoom( dataset=ds, strategy=stg, 
						   broker=brk, stop_ruined=True)
		

		# display prints, rslt and graph
		control_prints(ds)
		"""
		rslt.save()
		rslt.show()
		"""
		graph_if_needed(args, ds)
		



##############################
#		MAIN
##############################


if __name__ == '__main__':
	main()
