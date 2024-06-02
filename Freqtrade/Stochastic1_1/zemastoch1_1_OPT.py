# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union
from functools import reduce


from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IntParameter, IStrategy, merge_informative_pair)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib


class zemastoch1_1(IStrategy):
   
    INTERFACE_VERSION = 3

    
    timeframe = '5m'

    minimal_roi = {
        "0":0.02 #0.5  5 %
    }
    
    buy_params={
        "fastd_period":5,
        "fastk_period":3,
        "stoch_period":14,
        "ema_long_period":50,
        "ema_fast_period":20
     }
   


    stoploss = -0.04 #1  ta 10% 
    trailing_stop = False   

    use_exit_signal = False
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    ema_fast_period = IntParameter(5, 50, default= 20,space ='buy') 
    ema_long_period = IntParameter(10, 100, default=50,space ='buy')
    fastk_period = IntParameter(2, 7, default=int(buy_params['fastk_period']),space="buy")
    fastd_period =IntParameter(2, 5,default=int(buy_params['fastd_period']),space="buy" )
    lenght_period = IntParameter(7, 25, default= int(buy_params['stoch_period']),space="buy" )
    
   

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        for val in self.ema_fast_period.range:
            dataframe[f"ema_fast_{val}"] = ta.EMA(dataframe, timeperiod=val)

        for val in self.ema_long_period.range:
            dataframe[f"ema_long_{val}"] = ta.EMA(dataframe, timeperiod=val)
#------------------------------------------------------------------------------------------
        for val in self.lenght_period.range:    
            for val_1 in self.fastk_period.range:
                for val_2 in self.fastd_period.range:
                    dataframe[f'fastk_{val}_{val_1}_{val_2}'] = ta.STOCHRSI(dataframe,timeperiod = val,fastk_period=val_1,
                    fastd_period=val_2, fastd_matype=0)['fastk']

                    dataframe[f'fastd_{val}_{val_1}_{val_2}'] = ta.STOCHRSI(dataframe,timeperiod = val,fastk_period=val_1,
                    fastd_period=val_2, fastd_matype=0)['fastd'] 
        return dataframe



    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
# enter Long
        conditions_long = []
        conditions_short = []

        conditions_long.append(qtpylib.crossed_below(
                dataframe[f'ema_fast_{self.ema_fast_period.value}'],
                dataframe[f'ema_long_{self.ema_long_period.value}'],
            ))

            
        conditions_long.append(
             dataframe[f'fastd_{self.lenght_period.value}_{self.fastk_period.value}_{self.fastd_period.value}'] 
             < dataframe[f'fastk_{self.lenght_period.value}_{self.fastk_period.value}_{self.fastd_period.value}']
        )
        


# enter Short
        conditions_short.append(qtpylib.crossed_above(
                dataframe[f'ema_fast_{self.ema_fast_period.value}'],
                dataframe[f'ema_long_{self.ema_long_period.value}'],
            ))

        conditions_short.append(
           dataframe[f'fastd_{self.lenght_period.value}_{self.fastk_period.value}_{self.fastd_period.value}'] 
             > dataframe[f'fastk_{self.lenght_period.value}_{self.fastk_period.value}_{self.fastd_period.value}']
        )


        dataframe.loc[
            reduce(lambda x, y: x & y, conditions_long),
            "enter_long",
        ] = 1

        dataframe.loc[
            reduce(lambda x, y: x & y, conditions_short),
            "enter_short",
        ] = 1

        return dataframe
        
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            
                (
                    #(qtpylib.crossed_below(dataframe['close'],dataframe['ema50']))
                    #(qtpylib.crossed_above(dataframe['ema20'],dataframe['ema50']))


                ),
                'exit_long'] = 1
       
        
        dataframe.loc[
              
                (
                    #(qtpylib.crossed_above(dataframe['close'],dataframe['ema50']))
                    #(qtpylib.crossed_below(dataframe['ema20'],dataframe['ema50']))
                    
                ),
                ['exit_short']] = 1
        
        return dataframe
                
      
        

        
        