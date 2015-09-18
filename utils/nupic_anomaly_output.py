# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
"""
Provides two classes with the same signature for writing data out of NuPIC
models.
(This is a component of the One Hot Gym Anomaly Tutorial.)
"""
import csv
from collections import deque
from abc import ABCMeta, abstractmethod
# Try to import matplotlib, but we don't have to.
try:
  import matplotlib
  matplotlib.use('TKAgg')
  import matplotlib.pyplot as plt
  import matplotlib.gridspec as gridspec
  from matplotlib.dates import date2num, DateFormatter
except ImportError:
  pass

WINDOW = 300
HIGHLIGHT_ALPHA = 0.3
ANOMALY_HIGHLIGHT_COLOR = 'red'
WEEKEND_HIGHLIGHT_COLOR = 'yellow'
ANOMALY_THRESHOLD = 0.9


class NuPICOutput(object):

  __metaclass__ = ABCMeta


  def __init__(self, name):
    self.name = name


  @abstractmethod
  def write(self, xData, anomalyScore):
    pass


  @abstractmethod
  def close(self):
    pass



class NuPICPlotOutput(NuPICOutput):


  def __init__(self, *args, **kwargs):
    super(NuPICPlotOutput, self).__init__(*args, **kwargs)
    # Turn matplotlib interactive mode on.
    plt.ion()
    self.xVals = []
    self.anomalyScore = []
    self.anomalyScoreLine = None
    self.linesInitialized = False


    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(2, 1, height_ratios=[3,  1])

    self._anomalyGraph = fig.add_subplot(gs[0])

    plt.ylabel('Percentage')
    plt.xlabel('Record Index')

    # Maximizes window
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    plt.tight_layout()



  def initializeLines(self, xData):
    print "initializing %s" % self.name
    anomalyRange = (0.0, 1.0)
    self.xVals = deque([xData] * WINDOW, maxlen=WINDOW)
    self.anomalyScore = deque([0.0] * WINDOW, maxlen=WINDOW)


    anomalyScorePlot, = self._anomalyGraph.plot(
      self.xVals, self.anomalyScore, 'm'
    )
    anomalyScorePlot.axes.set_ylim(anomalyRange)

    self.anomalyScoreLine = anomalyScorePlot

    self._anomalyGraph.legend(
      tuple(['anomaly score']), loc=3
    )
    
    self.linesInitialized = True


  def write(self, xData, anomalyScore):

    if not self.linesInitialized:
      self.initializeLines(xData)


    self.xVals.append(xData)
    self.anomalyScore.append(anomalyScore)

    # Update anomaly chart data
    self.anomalyScoreLine.set_xdata(self.xVals)
    self.anomalyScoreLine.set_ydata(self.anomalyScore)

    self._anomalyGraph.relim()
    self._anomalyGraph.autoscale_view(True, True, True)

    plt.draw()



  def close(self):
    plt.ioff()
    plt.show()


NuPICOutput.register(NuPICPlotOutput)