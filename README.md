## Bootstrapping Treasury Zero Curve

"bootstrapping-treasury-zero-curve" is an algorithm that calculates the spot/zero curves and by extension the implied forward rate curves from the treasury yield curve". The project also adds a Dash-enabled visualisation to observe the evolution of the spot / forward curves through time, both playing in real time and selectable modes

### Data
Data is taken from public sources (Yahoo! Finance). It comprises the YTMs of various Treasury maturities throughout the year 2019.

### How to use
There are two ways of exploring this project

1. Running wsgi.py in the root folder will start up the Dash Application for data visualisation.

2. Running the main.py in the root folder will output the corresponding curves

### Content of functions
Data import and handling
```python
data_functions.get_data()
data_functions.interpolate_data()
```

Bootstrapping
```python
analysis_functions.bootstrap()
```