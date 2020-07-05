## Bootstrapping Treasury Zero Curve

"bootstrapping-treasury-zero-curve" is an algorithm that calculates the spot/zero curves and by extension the implied forward rate curves from the treasury yield curve"

### How to use
Running the main.py in the root folder will output the corresponding curves

### Working Features

### CurrentWIP
Data import and handling
```python
data_functions.get_data()
data_functions.interpolate_data()
```

Bootstrapping
```python
analysis_functions.bootstrap()
```