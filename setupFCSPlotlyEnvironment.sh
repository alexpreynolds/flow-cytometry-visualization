#!/bin/bash

conda create -n fcsPlotly python=3.6
conda activate fcsPlotly
pip install plotly==3.4.0
pip install plotly-orca==1.1.1
pip install psutil==5.4.8
pip install "notebook>=5.3" "ipywidgets>=7.2"
pip install jupyterlab==0.35
pip install fcsparser
pip install numpy
pip install pyppeteer
conda install -c conda-forge poppler -y
export NODE_OPTIONS=--max-old-space-size=4096
jupyter labextension install @jupyter-widgets/jupyterlab-manager@0.38 --no-build
jupyter labextension install plotlywidget@0.5.0  --no-build
jupyter labextension install @jupyterlab/plotly-extension@0.18  --no-build
jupyter lab build
conda deactivate fcsPlotly