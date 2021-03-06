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
from datetime import datetime
import matplotlib as mlib
# import bqplot as bp


class Gantt_chart(object):
    """
    Class to load render and plot a Gantt chart or roadmap
    """

    def __init__(self, dataFile, colorstyle='tab10'):
        """
        Initialization of a new Gantt instance using a provided
        data file in csv form.

        Keyword arguments:
        dataFile -- provided csv data
        """
        self.dataFile = dataFile

        self._loadData()
        self._processData(colorstyle)

    def _loadData(self):
        """
        Load data from a csv file. Mandatory columns are
        'activity', 'start date', 'end date'. Optional columns are
        'Workstream', 'Milestone', 'Deliverable'
        """

        fid = pd.read_csv(self.dataFile).dropna(how='all')
        fid.columns = map(str.lower, fid.columns)

        self.fid = fid
        self._check_columns()

    def _processData(self, colorstyle):
        """
        Prepare the loaded csv file for plotting in a Gantt chart
        """
        try:
            self.workstream = self.fid['workstream'].unique()
            self.fid['workstream'] = self.fid['workstream'].astype('category')
        except KeyError:
            print("No workstreams defined")
            pass
        try:
            self.milestone = pd.to_datetime(self.fid['milestone'],
                                            yearfirst=True)
        except KeyError:
            print("No milestones defined.")
            pass
        try:
            self.deliverable = pd.to_datetime(self.fid['deliverable'],
                                              yearfirst=True)
        except KeyError:
            print("No deliverables defined.")
            pass
        try:
            self.dependency = self.fid['dependency']

        except KeyError:
            print("No dependencies defined.")
            pass

        self.nActivities = len(self.fid.index)
        self.activity = self.fid['activity']
        self.startDate = pd.to_datetime(self.fid['start date'],
                                        yearfirst=True)
        self.endDate = pd.to_datetime(self.fid['end date'],
                                      yearfirst=True)
        self.duration = self.endDate - self.startDate
        self.yPosition = np.arange(self.nActivities, 0, -1)

        self._setWScolors(colorstyle)

    def _check_columns(self):
        mandatory_cols = ['activity', 'start date', 'end date']

        check_cols = [i.lower() in mandatory_cols for i in self.fid.columns]

        if sum(check_cols) != 3:
            print("Mandatory column names {} are not given in the csv file."
                  .format(*mandatory_cols))
        else:
            pass

    def _setWScolors(self, colorstyle):
        """
        set colors unique to a workstream
        """
        self.colors = {}
        colormap = plt.get_cmap(colorstyle, len(self.workstream))
        for i in range(len(self.workstream)):
            self.colors[self.workstream[i]] = colormap(i)

    def _formatPlot(self):
        """
        format the plot environment, e.g. labels, colors, ticks, etc.
        """

        plt.xlim(np.min(self.startDate), np.max(self.endDate))
        plt.ylim(0.5, self.nActivities + .5)

        plt.yticks(self.yPosition, self.activity)
        plt.xticks(rotation=35)

    def _get_date(self):
        """
        get current date in strftime
        """
        return datetime.today().strftime("%Y-%m-%d")

    def addMilestone(self):
        """
        add Milestones as diamonds to the gantt chart.
        """
        x = self.milestone[self.milestone.notnull()]
        y = self.yPosition[x.index]
        plt.plot_date(x, y, marker='D', markersize=12., color='orange',
                      markeredgecolor='gray', zorder=4)

    def addDeliverable(self):
        """
        add Deliverables as squares to the gantt chart.
        """
        x = self.deliverable[self.deliverable.notnull()]
        y = self.yPosition[x.index]
        plt.plot_date(x, y, marker='s', markersize=17, color='#db0f0f',
                      markeredgecolor='black', zorder=3)

    def addLegend(self):
        """
        add a legend explaining WS colors, milestones and deliverables
        """
        legend_elements = []
        try:
            self.milestone
            legend_elements.append(mlib.lines.Line2D([], [],
                                   marker='D', color='orange',
                                   markersize=12, markeredgecolor='gray',
                                   label='Milestone'))
        except AttributeError:
            pass
        try:
            self.deliverable
            legend_elements.append(mlib.lines.Line2D([], [],
                                   marker='s', color='#db0f0f',
                                   markersize=12, markeredgecolor='black',
                                   label='Deliverable'))
        except AttributeError:
            pass

        plt.legend(handles=legend_elements, fontsize='xx-large',
                   markerscale=1.6, fancybox=False, labelspacing=1.3)

    def addDependencies(self):
        """
        add dependency-arrows if tasks depend on other ones
        """
        try:
            self.dependency
            xtail = self.dependency[self.dependency.notnull()]
            ytail = self.yPosition[xtail.index]
            indices = [self.activity.loc[self.activity == i]
                       for i in xtail.values]
            idx = np.array([indices[i].index.values[0]
                            for i in range(len(indices))])
            xhead = self.activity[idx]
            yhead = self.yPosition[idx]
            csstyle = "angle,angleA=-90,angleB=180,rad=5"
            for i in range(len(xtail.index)):
                plt.plot([self.startDate[xtail.index[i]],
                          self.endDate[xhead.index[i]]],
                         [ytail[i], yhead[i]], ".", color=".2",
                         zorder=0, alpha=.1)
                plt.annotate("",
                             xy=(self.endDate[xhead.index[i]], yhead[i]),
                             xycoords='data',
                             xytext=(self.startDate[xtail.index[i]], ytail[i]),
                             textcoords='data',
                             arrowprops=dict(arrowstyle="->",
                                             linewidth=3,
                                             color="0.3",
                                             shrinkA=5, shrinkB=5,
                                             patchA=None,
                                             patchB=None,
                                             connectionstyle=csstyle))
        except AttributeError:
            pass

    def preparePlot(self, style='default', current_date=True,
                    add_dependencies=True):
        """
        prepare the plot environment

        Keyword arguments:
        style -- string, pyplot style defined
        font_size -- int, defining font size
        """
        plt.style.use(style)

        self.fig = plt.figure(figsize=[20, 10])
        self.ax = self.fig.add_subplot(111)
        colorsarray = [self.colors.get(i) for i in self.fid['workstream']]
        self.bars = plt.hlines(self.yPosition,
                               self.endDate.values,
                               self.startDate.values,
                               linewidth=40,
                               alpha=.8,
                               color=colorsarray,
                               zorder=2)

        if current_date is True:
            self.date_line = plt.vlines(self._get_date(), min(self.yPosition),
                                        max(self.yPosition), colors='red',
                                        linestyles='dashdot', alpha=.7,
                                        linewidth=3, zorder=1)
        elif type(current_date) == str:
            curdat = pd.to_datetime(current_date, yearfirst=True)
            self.date_line = plt.vlines(curdat, min(self.yPosition),
                                        max(self.yPosition), colors='red',
                                        linestyles='dashdot', alpha=.7,
                                        linewidth=3, zorder=1)
        try:
            self.addMilestone()
        except AttributeError:
            pass
        try:
            self.addDeliverable()
        except AttributeError:
            pass
        if add_dependencies is True:
            self.addDependencies()
        self.addLegend()
        self.weeks = mlib.dates.DayLocator(bymonthday=(1, 15))
        self.formatter = mlib.dates.DateFormatter("%d-%b '%y")

        self.ax.xaxis.set_major_formatter(self.formatter)
        self.ax.xaxis.set_major_locator(self.weeks)
        self.ax.xaxis.tick_top()
        self.ax.grid(which='major', axis='x')

        self._formatPlot()
        self.ax.tick_params(labelsize='x-large')

    def get(self, name):
        return super().__getattribute__(name)

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

    @staticmethod
    def save(savePath='gantt_chart.png'):
        """
        Save the gantt-plot to a png file.

        Keyword arguments:
        savePath -- string, defining path to save file.
        """
        plt.savefig(savePath, dpi=400, bbox_inches='tight')
