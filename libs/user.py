#!/usr/bin/env python 
#-*- coding: utf8 -*-



###############################
###############################
#   user
###############################
###############################



# user is the python object representation of a real user agent
# see full information in bellow docstring



#########################
#   CLASS
#########################


class User : 
    u"""User is a object that simulate and store important features of an user
	this feature is not drasticly usefull for now but will contain advanced
	and very dramatic features for future versions
	TO DO for futures version : 
	- 	manage "agressivity" of an user regarding money management strategy 
	- 	manage some king of "mood" or "market vision". is the user optimistic, 
		realistic pessimist, want kind of impact this feature will affect 
		its strategy choice, is it possible to train our agent to have a good
		"market vision" ? (...), for the same strategy what impact could or should
		have this "market vision" regarding final result? (...)

    """

	MIN = {"bank":100, "ruined_rate" : 0.1}
	MAX = {"bank":10000, "ruined_rate" : 0.99}

	def __init__(self, bank=MIN["bank"], ruined_rate=max["ruined_rate"]) : 
        
        u"""Initialization.

            positional arguments :

            bank        :       the arbitray sum your user have on his bank account
                                type int in [100, 10_000]

            ruined_rate  :      regarding a wrong strategy, the level your 
            					user will decide to stop the simulation and will
            					consider himself "ruined" 
            					type ploat in [0.0, 1.0]


        """

        # validation of bank arguments regarding default and authorised values
        try : 
        	bank = int(bank)
        	assert self.MAX["bank"] >= bank >= self.MIN["bank"]
        	self.bank = bank
        except:
            raise ValueError(
                "User.bank : given {}, expected int, min {}, max {}"
                .format(bank, self.MIN["bank"], self.MAX["bank"]))

        # validation of ruined rate arguments regarding default and authorised values
        try : 
        	ruined_rate = int(ruined_rate)
        	assert self.MAX["ruined_rate"] >= ruined_rate >= self.MIN["ruined_rate"]
        	self.ruined_rate = ruined_rate

        except:
            raise ValueError(
                "User.ruined_rate : given {}, expected float, min {}, max {}"
                .format(ruined_rate, self.MIN["ruined_rate"], self.MAX["ruined_rate"]))



#########################
#   MAIN
#########################


# this section should be founded in test/test_user.py (with pytest usage)

if __name__ == '__main__':
	user = User()
	print(user.__dict__)
