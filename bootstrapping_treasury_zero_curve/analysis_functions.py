# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 19:36:06 2020

@author: RUNHAO
"""

import pandas as pd

def bootstrap_slice(interpolatedDataSlice):
    cashflowStructure = {}
    
    for tenor in interpolatedDataSlice.index:
        
        #for each tenor bond, fill up the CF structure
        termStructure = []
        for time in range(5, int(tenor*10), 5):
            #note the range will naturally miss out the last interval
            termStructure.append(interpolatedDataSlice[tenor] / 2)
        termStructure.append(100 + interpolatedDataSlice[tenor] / 2)
        
        cashflowStructure[tenor] = termStructure
    
    spotRates = []
    
    #Using par-bond assumption, which states that at expiration value = par = 100
    #cashflow / 100 is the discount factor
    #we kick start the bootstrapping for the first value here:
    
    #note that the spot rates derived now are still in semi-annual decimal format
    #spotRates is a list in series by tenor
    
    spotRates.append(cashflowStructure[0.5][0] / 100 - 1)
    
    for tenor in interpolatedDataSlice.index[1:]:
        totalValue = 0
        finalPeriod = len(cashflowStructure[tenor])
        
        for period in range(0, finalPeriod - 1):
            discountFactor = (1 + spotRates[period]) ** (period + 1)
            totalValue += cashflowStructure[tenor][period] / discountFactor
        
        finalCashflow = 100 - totalValue
        discountFactorInverse = cashflowStructure[tenor][finalPeriod - 1] / finalCashflow
        spotRates.append(discountFactorInverse ** (1 / (finalPeriod)) - 1)
        
    forwardRates = []
    
    #Using forward parity, we can derive the forward curve as well
    
    for period in range(1, len(spotRates)):
        
        spotYield = (1 + spotRates[period]) ** period
        onePeriodBeforeYield = (1 + spotRates[period - 1]) ** (period - 1)
        forwardRates.append(spotYield/onePeriodBeforeYield - 1)
    
    #returns the raw dp in list format   
    return spotRates, forwardRates

def bootstrap_dataframe(interpolatedData):
    """
    loops down the time series to get our spot and forward curves
    """
    spotRatesData = pd.DataFrame(columns = interpolatedData.columns)
    forwardRatesData= pd.DataFrame(columns = interpolatedData.columns[1:])
    
    for date in interpolatedData.index:
        spot, forward = bootstrap_slice(interpolatedData.loc[date])
        
        spot = pd.Series(spot, index = interpolatedData.columns, name = date)
        forward = pd.Series(forward, index = interpolatedData.columns[1:], name = date)
        
        spotRatesData = spotRatesData.append(spot)
        forwardRatesData = forwardRatesData.append(forward)
    
    #tidy up
    spotRatesData = spotRatesData.applymap(lambda x: round(x * 100, 4))
    forwardRatesData = forwardRatesData.applymap(lambda x: round(x * 100, 4))
    
    return spotRatesData, forwardRatesData
