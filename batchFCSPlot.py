#!/usr/bin/env python

import sys
import os
import errno
import optparse
import fcsparser
import numpy as np
import plotly.graph_objs as go
import numpy as np
import copy
from plotly.offline import download_plotlyjs, plot
from pathlib import Path
import asyncio
from pyppeteer import launch

"""
Batch scatterplot generation from FCS files
"""

def main():
    plotter = BatchFCSPlot()
    plotter.parseArguments()
    plotter.run()

class BatchFCSPlot(object):

    baseMarker = {
        'color' : 'rgb(178, 190, 181)',
        'size' : 4,
        'symbol' : 'circle',
        'line' : {
            'color' : 'rgb(178, 190, 181)',
            'width' : 1
        },
        'opacity' : 0.1
    }

    highlightMarker = copy.deepcopy(baseMarker)
    highlightMarker['color'] = 'rgb(229, 43, 80)'
    highlightMarker['line']['color'] = 'rgb(229, 43, 80)'
    highlightMarker['opacity'] = 1

    def __init__(self, inputDir=None, outputDir=None, fcsInputExtension="fcs", fcsInputFiles=[], fcsTitles=[], fcsColumns=[], baseMarker=baseMarker, highlightMarker=highlightMarker, log10Transform=True, gateX=3.55, gateY=3.2, gateZ=3.02, xRangeMin=0, xRangeMax=6, yRangeMin=0, yRangeMax=6, zRangeMin=0, zRangeMax=6):
        self.inputDir = inputDir
        self.outputDir = outputDir
        self.fcsInputExtension = fcsInputExtension
        self.fcsInputFiles = fcsInputFiles
        self.fcsTitles = fcsTitles
        self.fcsColumns = fcsColumns
        self.baseMarker = baseMarker
        self.highlightMarker = highlightMarker
        self.log10Transform = log10Transform
        self.gateX = gateX
        self.gateY = gateY
        self.gateZ = gateZ
        self.xRangeMin = xRangeMin
        self.xRangeMax = xRangeMax
        self.yRangeMin = yRangeMin
        self.yRangeMax = yRangeMax
        self.zRangeMin = zRangeMin
        self.zRangeMax = zRangeMax

    def run(self):
        for fcsInputFileIdx, fcsInputFile in enumerate(self.fcsInputFiles):
            fcsTitle = self.fcsTitles[fcsInputFileIdx]
            fcsHTMLOutputDir = os.path.join(self.outputDir, fcsTitle)
            if not os.path.exists(fcsHTMLOutputDir):
                os.makedirs(fcsHTMLOutputDir)
            self.processInputFile(fcsInputFile, fcsHTMLOutputDir, fcsTitle, self.log10Transform)

    def processInputFile(self, inputFn, outputDir, title, log10Transform):
        meta, data = fcsparser.parse(inputFn, meta_data_only=False, reformat_meta=True)
        subset = data[self.fcsColumns]
        if log10Transform:
            subset = subset.apply(np.log10)
        xCol, yCol, zCol = subset.iloc[:, 0], subset.iloc[:, 1], subset.iloc[:, 2]
        x, y, z = np.array(xCol), np.array(yCol), np.array(zCol)
        xRange, yRange, zRange = [self.xRangeMin, self.xRangeMax], [self.yRangeMin, self.yRangeMax], [self.zRangeMin, self.zRangeMax]
        
        figData = []
        
        xSub, ySub, zSub = x[x < self.gateX], y[y < self.gateY], z[z < self.gateZ] 
        figData.append(self.xyzPlot(xSub, ySub, zSub, name="tripNegative", marker=self.highlightMarker))

        xSub, ySub, zSub = x[x >= self.gateX], y[y >= self.gateY], z[z >= self.gateZ] 
        figData.append(self.xyzPlot(xSub, ySub, zSub, name="tripPositive", marker=self.baseMarker))

        xSub, ySub, zSub = x[x < self.gateX], y[y >= self.gateY], z[z >= self.gateZ] 
        figData.append(self.xyzPlot(xSub, ySub, zSub, name="lag3Tim3Pos", marker=self.baseMarker))

        xSub, ySub, zSub = x[x >= self.gateX], y[y < self.gateY], z[z >= self.gateZ] 
        figData.append(self.xyzPlot(xSub, ySub, zSub, name="lag3Pd1Pos", marker=self.baseMarker))

        xSub, ySub, zSub = x[x >= self.gateX], y[y >= self.gateY], z[z < self.gateZ] 
        figData.append(self.xyzPlot(xSub, ySub, zSub, name="pd1Tim3Pos", marker=self.baseMarker))

        xSub, ySub, zSub = x[x >= self.gateX], y[y < self.gateY], z[z < self.gateZ] 
        figData.append(self.xyzPlot(xSub, ySub, zSub, name="pd1Pos", marker=self.baseMarker))

        xSub, ySub, zSub = x[x < self.gateX], y[y >= self.gateY], z[z < self.gateZ] 
        figData.append(self.xyzPlot(xSub, ySub, zSub, name="tim3Pos", marker=self.baseMarker))

        figLayout = go.Layout(
            title=title,
            width=2048,
            height=2048,
            font=dict(
                family='".SFNSDisplay-Regular", -apple-system, BlinkMacSystemFont, "Helvetica Neue", "Helvetica", "Calibri", Arial, sans-serif', 
                size=32, 
                color='#000'),
            scene = dict(
                camera=dict(
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=-1.25, y=-1.15, z=1.8)
                ),
                xaxis = dict(
                    title=xCol.name, 
                    range=xRange,
                    tickfont=dict(size=22)),
                yaxis = dict(
                    title=yCol.name, 
                    range=yRange,
                    tickfont=dict(size=22)),
                zaxis = dict(
                    title=zCol.name, 
                    range=zRange,
                    tickfont=dict(size=22)),
                aspectmode = 'cube')
        )

        fig = go.Figure(data=figData, layout=figLayout)

        htmlOutputFn = os.path.join(outputDir, 'index.html')
        pngOutputFn = os.path.join(outputDir, 'figure.png')
        sys.stderr.write("Debug: Writing [%s] and [%s]...\n" % (htmlOutputFn, pngOutputFn))
        plot(fig, image=None, filename=htmlOutputFn, image_width=2560, image_height=2560, auto_open=False)
        asyncio.get_event_loop().run_until_complete(self.imageViaPyppeteer("file://" + htmlOutputFn, pngOutputFn))

    async def imageViaPyppeteer(self, htmlUrl, pngPath):
        browser = await launch({
            'headless': False,
            'width': '2560px', 
            'height': '2560px', 
            'deviceScaleFactor': 1})
        page = await browser.newPage()
        await page.goto(htmlUrl)
        await page.screenshot({'path': pngPath, 'fullPage': True, 'omitBackground': True})
        await browser.close()

    def xyzPlot(self, x, y, z, name=None, marker=baseMarker, mode='markers', opacity=1):
        plot = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode=mode,
            marker=dict(
                color=marker['color'],
                size=marker['size'],
                symbol=marker['symbol'],
                line=marker['line'],
                opacity=marker['opacity']
            ),
            opacity=opacity,
            name=name
        )
        return plot

    def parseArguments(self):
        parser = optparse.OptionParser()
        parser.add_option("-i", "--inputDir", type="string", action="store", dest="inputDir", default=None)
        parser.add_option("-o", "--outputDir", type="string", action="store", dest="outputDir", default=None)
        parser.add_option("-c", "--fcsColumns", type="string", action="store", dest="fcsColumns", default=None)
        parser.add_option("-x", "--gateX", type="string", action="store", dest="gateX", default=None)
        parser.add_option("-y", "--gateY", type="string", action="store", dest="gateY", default=None)
        parser.add_option("-z", "--gateZ", type="string", action="store", dest="gateZ", default=None)
        parser.add_option("-1", "--xRangeMin", type="string", action="store", dest="xRangeMin", default=None)
        parser.add_option("-2", "--xRangeMax", type="string", action="store", dest="xRangeMax", default=None)
        parser.add_option("-3", "--yRangeMin", type="string", action="store", dest="yRangeMin", default=None)
        parser.add_option("-4", "--yRangeMax", type="string", action="store", dest="yRangeMax", default=None)
        parser.add_option("-5", "--zRangeMin", type="string", action="store", dest="zRangeMin", default=None)
        parser.add_option("-6", "--zRangeMax", type="string", action="store", dest="zRangeMax", default=None)
        (options, args) = parser.parse_args()

        # input directory
        if not options.inputDir:
            sys.stderr.write("Error: Must specify input directory\n")
            sys.exit(errno.EINVAL)
        self.inputDir = options.inputDir
        try:
            for fn in os.listdir(self.inputDir):
                if fn.endswith(".%s" % (self.fcsInputExtension)):
                    self.fcsInputFiles.append(os.path.abspath(os.path.join(self.inputDir, fn)))
                    self.fcsTitles.append(Path(fn).stem)
            if len(self.fcsInputFiles) == 0:
                raise FileNotFoundError("Error: FCS files not found in specified directory")
        except FileNotFoundError as err:
            sys.stderr.write("%s\n" % (err))
            sys.exit(errno.ENOENT)

        # output directory
        if not options.outputDir:
            sys.stderr.write("Error: Must specify output directory\n")
            sys.exit(errno.EINVAL)
        self.outputDir = os.path.abspath(options.outputDir)    
        if os.path.exists(self.outputDir):
            sys.stderr.write("Error: Output directory must not already exist\n")
            sys.exit(errno.EINVAL)
        os.makedirs(self.outputDir)

        # FCS columns
        if not options.fcsColumns:
            sys.stderr.write("Error: Must specify FSC columns\n")
            sys.exit(errno.EINVAL)
        cols = options.fcsColumns.split(',')
        if len(cols) != 3:
            sys.stderr.write("Error: Must specify three FSC column names\n")
            sys.exit(errno.EINVAL)
        self.fcsColumns = cols

        # gates
        if options.gateX:
            self.gateX = float(options.gateX)
        if options.gateY:
            self.gateY = float(options.gateY)
        if options.gateZ:
            self.gateZ = float(options.gateZ)

        # layout range bounds
        if options.xRangeMin:
            self.xRangeMin = float(options.xRangeMin)
        if options.xRangeMax:
            self.xRangeMax = float(options.xRangeMax)
        if options.yRangeMin:
            self.yRangeMin = float(options.yRangeMin)
        if options.yRangeMax:
            self.yRangeMax = float(options.yRangeMax)
        if options.zRangeMin:
            self.zRangeMin = float(options.zRangeMin)
        if options.zRangeMax:
            self.zRangeMax = float(options.zRangeMax)

    @property
    def inputDir(self):
        return self.__inputDir

    @inputDir.setter
    def inputDir(self, inputDir):
        self.__inputDir = inputDir

    @property
    def outputDir(self):
        return self.__outputDir

    @outputDir.setter
    def outputDir(self, outputDir):
        self.__outputDir = outputDir

    @property
    def fcsInputExtension(self):
        return self.__fcsInputExtension

    @fcsInputExtension.setter
    def fcsInputExtension(self, fcsInputExtension):
        self.__fcsInputExtension = fcsInputExtension

    @property
    def fcsInputFiles(self):
        return self.__fcsInputFiles

    @fcsInputFiles.setter
    def fcsInputFiles(self, fcsInputFiles):
        self.__fcsInputFiles = fcsInputFiles

    @property
    def fcsTitles(self):
        return self.__fcsTitles

    @fcsTitles.setter
    def fcsTitles(self, fcsTitles):
        self.__fcsTitles = fcsTitles

    @property
    def fcsColumns(self):
        return self.__fcsColumns

    @fcsColumns.setter
    def fcsColumns(self, fcsColumns):
        self.__fcsColumns = fcsColumns

    @property
    def baseMarker(self):
        return self.__baseMarker

    @baseMarker.setter
    def baseMarker(self, baseMarker):
        self.__baseMarker = baseMarker

    @property
    def highlightMarker(self):
        return self.__highlightMarker

    @highlightMarker.setter
    def highlightMarker(self, highlightMarker):
        self.__highlightMarker = highlightMarker

    @property
    def log10Transform(self):
        return self.__log10Transform

    @log10Transform.setter
    def log10Transform(self, log10Transform):
        self.__log10Transform = log10Transform

    @property
    def gateX(self):
        return self.__gateX

    @gateX.setter
    def gateX(self, gateX):
        self.__gateX = gateX

    @property
    def gateY(self):
        return self.__gateY

    @gateY.setter
    def gateY(self, gateY):
        self.__gateY = gateY

    @property
    def gateZ(self):
        return self.__gateZ

    @gateZ.setter
    def gateZ(self, gateZ):
        self.__gateZ = gateZ

    @property
    def xRangeMin(self):
        return self.__xRangeMin

    @xRangeMin.setter
    def xRangeMin(self, xRangeMin):
        self.__xRangeMin = xRangeMin

    @property
    def xRangeMax(self):
        return self.__xRangeMax

    @xRangeMax.setter
    def xRangeMax(self, xRangeMax):
        self.__xRangeMax = xRangeMax

    @property
    def yRangeMin(self):
        return self.__yRangeMin

    @yRangeMin.setter
    def yRangeMin(self, yRangeMin):
        self.__yRangeMin = yRangeMin

    @property
    def yRangeMax(self):
        return self.__yRangeMax

    @yRangeMax.setter
    def yRangeMax(self, yRangeMax):
        self.__yRangeMax = yRangeMax

    @property
    def zRangeMin(self):
        return self.__zRangeMin

    @zRangeMin.setter
    def zRangeMin(self, zRangeMin):
        self.__zRangeMin = zRangeMin

    @property
    def zRangeMax(self):
        return self.__zRangeMax

    @zRangeMax.setter
    def zRangeMax(self, zRangeMax):
        self.__zRangeMax = zRangeMax

if __name__ == "__main__":
    main()