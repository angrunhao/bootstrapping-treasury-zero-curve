import os
from . import data_functions
from . import analysis_functions


"""
HARDCODED VARIABLES
"""
currentPath = os.getcwd()

def run_functions():
    data = data_functions.get_data()
    interpolatedData = data_functions.interpolate_data(data = data)

    spotData, forwardData = analysis_functions.bootstrap_dataframe(interpolatedData)

    ymax = max([max(spotData.max()),max(forwardData.max())])
    ymin = min([min(spotData.min()),min(forwardData.min())])

    return spotData, forwardData, ymax, ymin