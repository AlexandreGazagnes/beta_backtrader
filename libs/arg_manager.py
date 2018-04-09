#!/usr/bin/env python 
#-*- coding: utf8 -*-



# basic arguments manager builded on argparse



# import 

import argparse



# functions

def arg_manager() : 
    u"""return args from args parser.
    positional args : 	-
    optional args : 	-
    return :		argparse object"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", 
			help="The OHLC file you want to study in ./datas, if none : PATH/FILE", 
			type=str)
    parser.add_argument("-F", "--folder", 
			help="The folder in wich tradator will load all valid OHLC files, if none : PATH/FILE",
			type=str)
    parser.add_argument("-g", "--graph", 
			help="show graph in web browser",
			action="store_true")

    return parser.parse_args()



# main 

if __name__ == '__main__':
    args = arg_manager()
    print args.__dict__