# Rantt

[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)

A small class to generate a Gantt chart (and in some future maybe a roadmap) using python and csv files.  

### Why the distinction between Gantt chart and roadmap

Roadmap and Gantt chart may look similar, but differ at their core. While a Gantt chart is typically a rather _static_ plan with an aggregation of broken down tasks (_Activities_) directly depending on each other, a roadmap is an _agile_ approach to define chunks of work and their rough timeframe.  

So while a Gantt Chart may be very detailed from the start, a roadmap orbits around self-organization and adaptive planning.

### Current Status

Currently, this code can generate Gantt charts from csv files, implementing optional dependencies of the tasks (marked as arrows).  
For a roadmap, systems providing more interaction, such as [bqplot](https://github.com/bloomberg/bqplot), may be implemented, so that an interactive roadmap can be created.  
Here are two examples of the resulting gantt charts (all matplotlib colorschemes are applicable):  
![example figure](https://github.com/Japhiolite/Rantt/blob/master/imgs/gantt_chart.png)
Different colorschemes:
![example viridis](https://github.com/Japhiolite/Rantt/blob/master/imgs/gantt_viridis.png)

Parts of this code are inspired by [gantt](https://github.com/stefanSchinkel/gantt) by stefanSchinkel.
