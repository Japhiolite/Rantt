"""
This module helps to generate interactive gantt charts / roadmaps from
csv files. Used in Jupyter Notebooks with bqplot, charts are interactive
and can changed in the plot frame.
The changes are then stored back in the dataframe / csv.
Some of this code is inspired by https://github.com/stefanSchinkel/gantt
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlib
# import bqplot as bp


class Gantt_chart(object):
    """
    Class to load render and plot a Gantt chart or roadmap
    """

    def __init__(self, dataFile):
        """
        Initialization of a new Gantt instance using a provided
        data file in csv form.

        Keyword arguments:
        dataFile -- provided csv data
        """
        self.dataFile = dataFile

        self._loadData()
        self._processData()

    def _loadData(self):
        """
        Load data from a csv file. Mandatory columns are
        'activity', 'start date', 'end date'. Optional columns are
        'Workstream', 'Milestone', 'Deliverable'
        """

        fid = pd.read_csv(self.dataFile)

        fid.columns = map(str.lower, fid.columns)

        self.fid = fid
        self._check_columns()

    def _processData(self):
        """
        Prepare the loaded csv file for plotting in a Gantt chart
        """
        try:
            self.workstream = self.fid['workstream'].unique()
            self.fid['workstream'] = self.fid['workstream'].astype('category')
        except AttributeError:
            print("No workstreams defined")
            pass

        self.nActivities = len(self.fid.index)
        self.activity = self.fid['activity']
        self.startDate = pd.to_datetime(self.fid['start date'],
                                        yearfirst=True)
        self.endDate = pd.to_datetime(self.fid['end date'],
                                      yearfirst=True)

        self.duration = self.endDate - self.startDate
        self.yPosition = np.arange(self.nActivities, 0, -1)

        self._setWScolors()

    def _check_columns(self):
        mandatory_cols = ['activity', 'start date', 'end date']

        check_cols = [i.lower() in mandatory_cols for i in self.fid.columns]

        if sum(check_cols) != 3:
            print("Mandatory column names {} are not given in the csv file."
                  .format(*mandatory_cols))
        else:
            pass

    def _setWScolors(self):
        """
        set colors unique to a workstream
        """
        self.colors = {}
        colormap = plt.get_cmap('tab10', len(self.workstream))
        for i in range(len(self.workstream)):
            self.colors[self.workstream[i]] = colormap(i)
        # colors = [colormap(i) for i in self.workstream]

    def get(self, name):
        return super().__getattribute__(name)

    def formatPlot(self):
        """
        format the plot environment, e.g. labels, colors, ticks, etc.
        """
        plt.xlim(np.min(self.startDate), np.max(self.endDate))
        plt.ylim(0.5, self.nActivities + .5)

        plt.yticks(self.yPosition, self.activity)
        plt.xticks(rotation=35)

    def preparePlot(self):
        """
        prepare the plot environment
        """
        self.fig = plt.figure(figsize=[20, 10])
        self.ax = self.fig.add_subplot(111)
        self.numDuration = (mlib.dates.date2num(self.endDate) -
                            mlib.dates.date2num(self.startDate))
        self.numStart = mlib.dates.date2num(self.startDate)
        colorsarray = [self.colors.get(i) for i in self.fid['workstream']]
        self.bars = plt.barh(self.yPosition, self.numDuration,
                             left=self.numStart,
                             align='center',
                             height=.5,
                             alpha=.8,
                             color=colorsarray)
        self.formatter = mlib.dates.DateFormatter("%d-%b '%y")
        self.ax.xaxis.set_major_formatter(self.formatter)

        self.formatPlot()

    def showCSV(self):
        """
        Show the dataframe.
        """
        return self.fid.head()

    @staticmethod
    def showGantt():
        """
        Show plot
        """
        plt.show()
