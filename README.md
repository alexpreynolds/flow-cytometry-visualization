# flow-cytometry-visualization

This project demonstrates visualizing flow cytometry datasets, using Jupyter, Plotly, and `fcsparser`. 

A command-line script is included called `batchFCSPlot.py` that does batch conversion of FCS files to PNG-formatted scatterplots. This script makes uses of Google Puppeteer and Chromium, in addition to Plotly and `fcsparser`.

----

## Setup

### Virtual environment

The easiest way to run this is to install Anaconda. Then run the `setupFCSPlotlyEnvironment.sh` script to set up a virtual environment called `fcsPlotly`, which contains the required Python libraries (as well as the specific versions of libraries required for interoperability):

```
$ ./setupFCSPlotlyEnvironment.sh
...
```

This step can take a few minutes, but you only need to do this step once. Afterwards, you can skip this step and go directly to the next.

### Opening the notebook

Any time that you open the notebook, you will want to do so from within the environment you just made, by activating it:

```
$ conda activate fcsPlotly
(fcsPlotly) $
```

Then run the `jupyter lab` command to open the notebook:

```
(fcsPlotly) $ jupyter lab
...
```

When finished, run `conda deactivate` to close the environment and return to the base shell:

```
(fcsPlotly) $ conda deactivate
$
```

Or just close the Terminal window.

----

## Notebook

It may be necessary to re-run the Jupyter notebook, after opening it. 

To do this, pull down the `Kernel` menu and select `Restart & Run All`. This recalculates variables and objects used for rendering the scatterplot.

To load local data and select desired datasets, make some adjustments to variables in the notebook:

 1. Adjust the value of the `fcsBaseFn` variable to point to a locally-saved copy of your FCS file. The desired FCS file could be put into the `data` subdirectory in this notebook's directory.
 2. Adjust the desired column names in the `colsOfInterest`; these are used to render the three axes of the scatterplot.

After making adjustments, re-run the Jupyter notebook. To do this, pull down the `Kernel` menu and select `Restart & Run All`.

The scatterplot is available at the bottom of the notebook and can be interacted with click-and-drag and scrollwheel actions, which rotate and zoom the plot. 

A PNG file of the scatterplot can be exported by clicking on the camera icon in the top-right corner of the scatterplot window.

----

## Batch plot generation

### Prerequisites

Batch generation requires the installation of the `pyppeteer` Python library, which will in turn install Chromium, a version of Google Chrome that is used here to generate and export PNG files. This is installed with the `fcsPlotly` virtual environment. See the *Setup* section at the top of this page to make sure you have installed the environment and that you have activated it.

**Note**: I am investigating use of `plotly.io` to write PDF and PNG files directly from the notebook, instead of using Chromium as an intermediate. At this time, there appear to be bugs. This approach sidesteps `plotly.io` by mimicking interaction with the scatterplot through a "headless" web browser.

### Usage

```
(fcsPlotly) $ ./batchFCSPlot.py --inputDir <directory-of-FCS-files> --outputDir <directory-for-image-files> --fcsColumns <list-of-column-headers> [ --gateX <float> --gateY <float> --gateZ <float>] [ --xRangeMin <float> --xRangeMax <float> --yRangeMin <float> --yRangeMax <float> --zRangeMin <float> --zRangeMax <float> ]
```

The first time the `batchFCSPlot.py` script is run, you may be prompted to grant permissions for Chromium to access your screen display. Just click on the "Allow" button for the script to proceed. You should only need to do this once; afterwards, the browser will make screenshots in the background.

Gate values `--gateX`, `--gateY`, and `--gateZ` are optional and are set initially to defaults of `3.55`, `3.2`, and `3.02`, respectively.

Each pair of `--xRangeMin`, `--xRangeMax`, `--yRangeMin`, `--yRangeMax`, `--zRangeMin`, and `--zRangeMax` is set to a default minimum of `0` and a maximum of `6`, respectively.

### Example

When run from within this project directory:

```
(fcsPlotly) $ ./batchFCSPlot.py --inputDir data --outputDir /tmp/fcsImages --fcsColumns "APC-H,PB450-H,ECD-H"
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

The following, for instance, will open a PNG file in your default image viewer:

```
$ open /tmp/fcsImages/01-TripDay5-B1-PD1/figure.png
```
