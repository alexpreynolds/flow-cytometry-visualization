# flow-cytometry-visualization

This project demonstrates visualizing flow cytometry datasets, using Jupyter, Plotly, and `fcsparser`. 

A command-line script is included called `batchFCSPlot.py` that does batch conversion of FCS files to PNG-formatted scatterplots. This script makes uses of Google Puppeteer and Chromium, in addition to Plotly and `fcsparser`.

## Jupyter notebook

To run this quickly, you may view the Jupyter notebook in *nbviewer*:

https://nbviewer.jupyter.org/github/alexpreynolds/flow-cytometry-visualization/blob/master/FlowCytometryVisualization.ipynb

It can be useful to run this locally, to make tweaks and see how things work.

First, install required Python libraries:

```
$ pip install fcsparser
$ pip install jupyter
$ pip install plotly
$ pip install numpy
```

Installing these libraries could take a few minutes, depending on what is already installed.

The `fcsparser` library is used to open and process FCS files. The other libraries are used for processing and visualizing the data.

Open the notebook file `FlowCytometryVisualization.ipynb`:

```
$ jupyter notebook FlowCytometryVisualization.ipynb
```

This will open the notebook in your default web browser.

----
Note: If you run into `IOPub` errors, adjust `jupyter` settings when loading the notebook:

```
$ jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e10 FlowCytometryVisualization.ipynb
```
----

Make a couple adjustments, as needed, to load local data and select desired datasets:

 1. Adjust the value of the `fcsBaseFn` variable to point to a locally-saved copy of your FCS file. The desired FCS file could be put into the `data` subdirectory in this notebook's directory.
 2. Adjust the desired column names in the `colsOfInterest`; these are used to render the three axes of the scatterplot.

After making adjustments, re-run the Jupyter notebook. To do this, pull down the `Kernel` menu and select `Restart & Run All`.

The scatterplot is available at the bottom of the notebook and can be interacted with click-and-drag and scrollwheel actions, which rotate and zoom the plot. 

A PNG file of the scatterplot can be exported by clicking on the camera icon in the top-right corner of the scatterplot window.

## Batch plot generation

### Prerequisites

Batch generation requires the additional installation of the `pyppeteer` Python library, which will in turn install Chromium, a version of Google Chrome that is used here to generate and export PNG files:

```
$ pip install pyppeteer
```

### Usage

```
$ ./batchFCSPlot.py --inputDir <directory-of-FCS-files> --outputDir <directory-for-image-files> --fcsColumns <list-of-column-headers> [ --gateX <float> --gateY <float> --gateZ <float>] [ --xRangeMin <float> --xRangeMax <float> --yRangeMin <float> --yRangeMax <float> --zRangeMin <float> --zRangeMax <float> ]
```

The first time the `batchFCSPlot.py` script is run, you may be prompted to grant permissions for Chromium to access your screen display. Just click on the "Allow" button for the script to proceed. You should only need to do this once; afterwards, the browser will make screenshots in the background.

Gate values `--gateX`, `--gateY`, and `--gateZ` are optional and are set initially to defaults of `3.55`, `3.2`, and `3.02`, respectively.

Each pair of `--xRangeMin`, `--xRangeMax`, `--yRangeMin`, `--yRangeMax`, `--zRangeMin`, and `--zRangeMax` is set to a default minimum of `0` and a maximum of `6`, respectively.

### Example

When run from within this project directory:

```
$ ./batchFCSPlot.py --inputDir data --outputDir /tmp/fcsImages --fcsColumns "APC-H,PB450-H,ECD-H"
Debug: Writing [/tmp/fcsImages/01-TripDay5-E2-Untreated/index.html] and [/tmp/fcsImages/01-TripDay5-E2-Untreated/figure.png]...
Debug: Writing [/tmp/fcsImages/01-TripDay5-B1-PD1/index.html] and [/tmp/fcsImages/01-TripDay5-B1-PD1/figure.png]...
Debug: Writing [/tmp/fcsImages/01-TripDay5-C1-TIM3/index.html] and [/tmp/fcsImages/01-TripDay5-C1-TIM3/figure.png]...
Debug: Writing [/tmp/fcsImages/01-TripDay5-E1-Untreated/index.html] and [/tmp/fcsImages/01-TripDay5-E1-Untreated/figure.png]...
Debug: Writing [/tmp/fcsImages/01-TripDay5-B2-PD1/index.html] and [/tmp/fcsImages/01-TripDay5-B2-PD1/figure.png]...
Debug: Writing [/tmp/fcsImages/01-TripDay5-A3-unstained/index.html] and [/tmp/fcsImages/01-TripDay5-A3-unstained/figure.png]...
Debug: Writing [/tmp/fcsImages/01-TripDay5-D2-LAG3/index.html] and [/tmp/fcsImages/01-TripDay5-D2-LAG3/figure.png]...
Debug: Writing [/tmp/fcsImages/01-TripDay5-A2-multiplex/index.html] and [/tmp/fcsImages/01-TripDay5-A2-multiplex/figure.png]...
Debug: Writing [/tmp/fcsImages/01-TripDay5-C2-TIM3/index.html] and [/tmp/fcsImages/01-TripDay5-C2-TIM3/figure.png]...
Debug: Writing [/tmp/fcsImages/01-TripDay5-A1/index.html] and [/tmp/fcsImages/01-TripDay5-A1/figure.png]...
Debug: Writing [/tmp/fcsImages/01-TripDay5-D1-LAG3/index.html] and [/tmp/fcsImages/01-TripDay5-D1-LAG3/figure.png]...
```

In this example, each of the subfolders `/tmp/fcsImages/<FCS-dataset>` contain `index.html` and `figure.png`.

The following, for instance, will open the PNG file in your default image viewer:

```
$ open /tmp/fcsImages/01-TripDay5-B1-PD1/figure.png
```
