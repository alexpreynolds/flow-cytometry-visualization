# flow-cytometry-visualization
Flow cytometry visualization demo using Jupyter, Plotly, and fcsparser

To run this locally, install required Python libraries:

```
$ pip install fcsparser
$ pip install jupyter
$ pip install plotly
```

This can take a few minutes.

Open the notebook `FlowCytometryVisualization.ipynb`:

```
$ jupyter notebook FlowCytometryVisualization.ipynb
```

Make a couple adjustments, as needed, to load local data and select desired datasets:

 1. Adjust the value of the `path` variable to point to a locally-saved copy of your FCS file. 
 2. Adjust the desired column names in the `colsOfInterest`; these are used to render the three axes of the scatterplot

Run the Jupyter notebook. The scatterplot is at the bottom of the notebook and can be interacted with via mouse click-and-drag, and scrollwheel. 

A PNG file can be exported of the scatterplot by clicking on the camera icon in the top-right corner of the scatterplot window.
