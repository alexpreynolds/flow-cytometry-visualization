# flow-cytometry-visualization

Flow cytometry dataset visualization demo, using Jupyter, Plotly, and `fcsparser`.

To run this locally, install required Python libraries:

```
$ pip install fcsparser
$ pip install jupyter
$ pip install plotly
$ pip install numpy
```

Installing these libraries could take a few minutes.

The `fcsparser` library is used to open and process FCS files. The other libraries are used for processing and visualizing the data.

Open the notebook file `FlowCytometryVisualization.ipynb`:

```
$ jupyter notebook FlowCytometryVisualization.ipynb
```

This will open the notebook in your default web browser.

Make a couple adjustments, as needed, to load local data and select desired datasets:

 1. Adjust the value of the `path` variable to point to a locally-saved copy of your FCS file. The desired FCS file could be put into the same directory as this notebook.
 2. Adjust the desired column names in the `colsOfInterest`; these are used to render the three axes of the scatterplot.

After making adjustments, re-run the Jupyter notebook. To do this, pull down the `Kernel` menu and select `Restart & Run All`.

The scatterplot is available at the bottom of the notebook and can be interacted with click-and-drag and scrollwheel actions, which rotate and zoom the plot. 

A PNG file of the scatterplot can be exported by clicking on the camera icon in the top-right corner of the scatterplot window.
