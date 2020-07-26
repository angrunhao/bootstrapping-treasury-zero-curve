# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 18:26:46 2020

@author: RUNHAO
"""
import os
from bootstrapping_treasury_zero_curve import data_functions
from bootstrapping_treasury_zero_curve import analysis_functions


"""
HARDCODED VARIABLES
"""
currentPath = os.getcwd()

data = data_functions.get_data(path = currentPath)
interpolatedData = data_functions.interpolate_data(data = data)

spotData, forwardData = analysis_functions.bootstrap_dataframe(interpolatedData)

ymax = max([max(spotData.max()),max(forwardData.max())])
ymin = min([min(spotData.min()),min(forwardData.min())])


