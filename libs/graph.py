#!/usr/bin/env python 
#-*- coding: utf8 -*-


from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
from random import choice
from collections import OrderedDict


class Graph :

	def __init__(self, name, *items) :
		# output to static HTML file
		output_file(name + ".html")
		self.items = [i.figure for i in items]

	def show(self):
		# show
		show(column(self.items))


class Item :

	MAIN_SIZE = [1200, 400]
	OTHER_SIZE = [1200, 200]


	def __init__(self, title="", main=False) : 
		self.color_line = iter(	["black", "red", "orange", "gold", "yellow", "blue", "green",
								"black", "red", "orange", "gold", "yellow", "blue", "green"])
		self.color_points = iter(["orange", "blue", "green"])

		if main : 
			width, height = self.MAIN_SIZE
		else :
			width, height = self.OTHER_SIZE


		# create a new plot with a title and axis labels
		self.figure = figure(title=title, x_axis_label='day', y_axis_label='val',
							plot_width=width, plot_height=height)

	def add_candles(self):
		pass 

	def add_line(self, x, y, l="") : 
		color = next(self.color_line)
		self.figure.line(x, y, legend=l, line_width=2, line_color=color)

	def add_lines(self, x, l_y):
		for l, y in l_y :
			color = next(self.color_line)
			self.figure.line(x, y, legend=l, line_width=2, line_color=color)


	def add_points(self, x_y, l) : 
		x,y =x_y
		self.figure.circle(x,y, legend=l, size=10, color=self.color_points, alpha=0.5)

	def add_orders(self, buy_x_y, sell_x_y ): 
		x, y = [i[0] for  i in buy_x_y], [i[1] for  i in buy_x_y]
		self.figure.circle(x,y, legend="buy", size=10, color="green", alpha=0.5)

		x, y = [i[0] for  i in sell_x_y], [i[1] for  i in sell_x_y]
		self.figure.circle(x,y, legend="sell", size=10, color="red", alpha=0.5)



def build_graph(ds=None, option="line") : 

	# CONSTANTS

	MAIN_SIZE = [1200, 400]
	OTHER_SIZE = [1200, 200]
	COLOR_LINES = ["black", "red", "orange", "gold", "yellow", "blue", "green"]
	COLOR_POINTS = ["black", "grey", "purple", "blue", "green"]


	# FUNCTIONS

	def initiate_output() : 
		output_file(ds.name + ".html")


	def intiate_color(lines) :
		COLOR = COLOR_LINES if lines else COLOR_POINTS
		return COLOR


	def initiate_figure(title_fig, main_item) : 
		size = MAIN_SIZE if main_item else OTHER_SIZE
		return figure(	title=title_fig, x_axis_label='day', y_axis_label='val',
						plot_width=size[0],  plot_height=size[1])


	def draw_main_item() : 

		main_item = initiate_figure(ds.desc, True) 	
		color_panel = iter(intiate_color(lines=True))

		if option == "line" : 		# add close 		
			x, y = list(ds.index), list(ds.close)
			main_item.line(x, y, legend="close", line_width=2, line_color=next(color_panel))
		else : 
			print("not implemented")

		if "ma" in ds.main_indicators.keys() : 		# add various ma
			for name in ds.main_indicators["ma"] :
				x, y = list(ds.index), list(ds[name])
				main_item.line(x, y, legend=name, line_width=2, line_color=next(color_panel))

		if "bollingers" in ds.main_indicators.keys() : 		# add bollingers 
			for name in ds.main_indicators["bollingers"] : 
				x, y = list(ds.index), list(ds[name])
				main_item.line(x, y, line_dash ="dashed",
								 line_width=2, line_color="grey")
				main_item.line(	[0], [ds.close[0]], legend="bollingers", 
								line_dash="dashed", color = "grey" )

		color_panel = iter(intiate_color(lines=False))
	
		if "cross" in ds.main_indicators.keys() : 		# add cross 
			for name in ds.main_indicators["cross"] : 
				x = list(ds[ds[name] == True].index) # [i for (i, j) in enumerate(ds[name]) if j == True ]
				y = [ds.close[i] for i in x]
				main_item.circle(x, y, legend=name, size=10, color=next(color_panel), alpha=0.5)

		if ds.orders : 		# add orders 
			for name in ds.orders : 
				color = "green" if name == "buy" else "red"
				x = list(ds[ds[name] == True].index)
				y = [ds.close[i] for i in x]
				main_item.circle(x, y, legend=name, size=10, color=color, alpha=0.5)

		return main_item


	def draw_other_items() : 
		items = list()
		for family, indicators  in ds.other_indicators.items() : 
		
			color_panel = iter(intiate_color(lines=True))

			other_item = initiate_figure(family, False) 
			for name in indicators : 
				x, y = list(ds.index), list(ds[name])
				other_item.line(x, y, legend=name, line_width=2, line_color=next(color_panel))
			items.append(other_item)

		return items


	# MAIN 

	initiate_output()  

	main_item = draw_main_item()
	other_items = draw_other_items()
	items = [main_item] + other_items
	show(column(items))