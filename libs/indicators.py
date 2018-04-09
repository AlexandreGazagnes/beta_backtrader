#!/usr/bin/env python 
#-*- coding: utf8 -*-



class Indicator() : 

	def __init__(self) : 
		pass

	def add_family(self, family) : 
		self.family = dict()

	def add_val(self, family, label, val) : 
		self.family[label] = val