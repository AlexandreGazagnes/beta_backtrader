#!/usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import absolute_import
import os



class Result(object) : 

    def __init__(self) : 

        # count how many "result_x.csv" file in "./results" and initiate counter if needed
        if ".result_count.p" not in os.listdir("./results/") : 
            result_counter = 0
        else : 
            with open("./results/.result_count.p", "r") as f:
                result_counter = int(f.read())
        result_filename = "result_"+str(result_counter)+".csv"
        result_counter+=1
        with open("./results/.result_count.p", "w") as f : 
            f.write(str(result_counter))

        # first 2 arguments of result class

        self.resut_path = "./results/"
        self.result_filename = result_filename
        
        self.headers  =  "strategy_name,strategy_family,file,param1,param2,param3,param4,data_result,abs_strat_result,rel_strat_result\n"
        

        # write headers
        with open(self.resut_path+self.result_filename, "w") as f : 
            f.write(self.headers) 

    def save(self,  strategy_name, strategy_family, 
             file, param1, param2, param3, param4, 
             data_result, abs_strat_result, rel_strat_result):
        u"""Save strategy results.csv in a file.

        Positional arguments:
        REWRIITE IT
        """

        with open(self.resut_path+self.result_filename, "a") as f:
            f.write(    "{},{},{},{},{},{},{},{},{},{}\n".format(   strategy_name, strategy_family, 
                                                        file, param1, param2, param3, param4, 
                                                        data_result, abs_strat_result, rel_strat_result))
            


def main() : 

    r1 = Result(    "Dumb_0.1_0.1_0", "dumb",
                    {"stop_loss":0.1, "stop_profit": 0.1, "waiter":0},
                    ["crisis_OK.csv", "euphoria_OK.csv"],
                    {"crisis_OK.csv":-33.12, "euphoria_OK.csv":+125 },
                    {"crisis_OK.csv":-45.12, "euphoria_OK.csv":+45 },
                    {"crisis_OK.csv":-15, "euphoria_OK.csv":-67 })

    print(r1.__dict__)


if __name__ == '__main__':
    main()