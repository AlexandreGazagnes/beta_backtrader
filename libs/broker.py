#!/usr/bin/env python
#-*- coding: utf8 -*-



###############################
###############################
#   broker
###############################
###############################


# broker is the python object représentation of a real web broker
# see full information in bellow docstring



#########################
#   CLASS
#########################


class Broker(object):
    u"""Broker is a object that simulate a real web broker
    usefull if you want to run a strategy on a dataset and explore how
    broker's conditions affect your results.
    TO DO for future versions : 
    -   be able to connect to the real broker's api
        and manage connection to your account, consults your porfolio, download your trade history
        and pass automatic/maunal orders
    -   be able to dowload exact parameters from updated real web borker.
        for instance brk = Broker.get_real("kraken")  
    """

    MIN = {"maker_fees": 0.0, "taker_fees": 0.001, "slipage": 0.002}
    MAX = {"maker_fees": 0.01, "taker_fees": 0.01, "slipage": 0.08}

    def __init__(self, name="ideal_broker", maker_fees=MIN["maker_fees"],
                 taker_fees=MIN["taker_fees"], slipage=MIN["slipage"]):
        u"""Initialization.

            positional arguments :

            name        :       the arbitray name given to your broker's instance
                                exemple : just "kraken" or bitfinex
                                type str

            maker_fees  :       maker_fees = fees for market order
                                type float in [0.0 : 0003]


            taker_fees  :       maker_fees = fees for limit order
                                type float in [0.0 : 0003]

            slipage      :      difference betwen the price you want/set order and the price your
                                broker pass the order
                                WARNING : subejctive and not definitive version but slipage is a diffrenet notion when
                                you pass a limit or a market order
                                    - when market order : difference between price at time t, and price your broker buy for you
                                    slightly bellow for sell, slightly above for buy

                                    - when limit order : difference between price at time t, and the order you put
                                    slightly above for sell, slightly bellow for buy
                                type float, in [0 : 0.01]

        """

        self.name = name

        # validation of maker fees arguments regarding default and athorised values
        try:
            maker_fees = float(maker_fees)
            assert self.MIN["maker_fees"] <= maker_fees < self.MAX["maker_fees"]
            self.maker_fees = maker_fees
        except:
            raise ValueError(
                "Broker.maker_fees : given {}, expected  float, min {}, max {}"
                .format(maker_fees, self.MIN["maker_fees"], self.MAX["maker_fees"]))

        # validation of taker fees arguments regarding default and athorised values
        try:
            taker_fees = float(taker_fees)
            assert self.MIN["taker_fees"] <= taker_fees < self.MAX["taker_fees"]
            self.taker_fees = taker_fees
        except:
            raise ValueError(
                "Broker.taker_fees : given {}, expected  float, min {}, max {}"
                .format(taker_fees, self.MIN["taker_fees"], self.MAX["taker_fees"]))

        # validation of slipage arguments regarding default and athorised values
        try:
            slipage = float(slipage)
            assert self.MIN["slipage"] <= slipage < self.MAX["slipage"]
            self.slipage = slipage
        except:
            raise ValueError(
                "Broker.slipage : given {}, expected float, min {}, max {}"
                .format(slipage, self.MIN["slipage"], self.MAX["slipage"]))



#########################
#   MAIN
#########################


# this section should be founded in test/test_broker.py (with pytest usage)

if __name__ == '__main__':

    # broker = Broker("mad_broker", 0.1, 0.005, 0.01)
    # print(broker.__dict__)
    broker = Broker()
    print(broker.__dict__)
    # broker = Broker("mad_broker", 0.1, 0.00, 0.0)
    # print(broker.__dict__)
