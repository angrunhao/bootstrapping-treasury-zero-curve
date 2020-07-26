# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 18:07:59 2020

@author: RUNHAO
"""
import os
import pandas as pd

"""
HARDCODED VALUES
"""
#only used when testing
#parentPath = os.path.dirname(os.getcwd())
parentPath = os.getcwd()

def get_data(path = parentPath):
    """
    retrieves the static data for Treasury bills and bonds located in the 'data' folder,
    which is located in the parent folder.
    processes the data for further analysis
    """
    
    dataMerged = pd.DataFrame()
    billsData = pd.read_csv(path + "\\data\\treasuryBills.csv", index_col = 0)
    billsData = billsData.loc[:, ["26 WEEKS COUPON EQUIVALENT", "52 WEEKS COUPON EQUIVALENT"]]
    
    bondsData = pd.read_csv(path + "\\data\\treasuryBonds.csv", index_col = 0)
    bondsData = bondsData.loc[:, ["2 Yr", "3 Yr", "5 Yr", "7 Yr", "10 Yr"]]
    
    if (billsData.index != bondsData.index).any():
        commonIndex = billsData.index.intersection(bondsData.index)
        billsData = billsData[commonIndex]
        bondsData = bondsData[commonIndex]
    
    dataMerged = pd.concat([billsData, bondsData], axis = 1)
    dataMerged.columns = ["26W", "52W", "2Y", "3Y", "5Y", "7Y", "10Y"]
    
    return dataMerged

def tenor_converter(columnName):
    
    if columnName[-1] == "W":
        return round(int(columnName[:-1])/52,2)
    
    elif columnName[-1] == "M":
        return round(int(columnName[:-1])/12,2)
    
    else:
        return float(columnName[:-1])

def interpolate_data(data):
    
    #create the semi-annual tenors list
    availableTenors = [tenor_converter(x) for x in data.columns]
    data.columns = availableTenors
    fullTenors = [tenor/10 for tenor in range(5,101,5)]
    missingTenors = [tenor/10 for tenor in range(5,101,5) if tenor/10 not in availableTenors]
    
    #interpolate the missing semi-annual tenors
    for tenor in missingTenors:       
        low = None
        high = None
        
        while low == None and high == None:
            
            for availableTenorIndex in range(0, len(availableTenors)):
                
                if tenor > availableTenors[availableTenorIndex]:
                    low = availableTenors[availableTenorIndex]
                    high = availableTenors[availableTenorIndex + 1]
        
        data[tenor] = data[low] + ((data[high] - data[low]) / (high - low)) * (tenor - low)
    
    #tidy up to 2dp and in the tenor order
    data = data.applymap(lambda x: round(x, 4))
    data = data[fullTenors]
    
    return data
            
        
        
        
        
        
        
        
        
    
