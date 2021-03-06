<img src='http://galenscovell.github.io/css/pics/parser.png' width=500px />

# Transcriptome Data Parser

This repository is dedicated to the design and construction of a data parser for the Tublitz Neuroscience lab at the University of Oregon. All of the actual data is kept private.

Utilizes:
* <b>Pandas</b> and <b>Xlrd</b> module for handling csv, xls, and xlsx data
* <b>tkinter</b> for GUI creation
* <b>Matplotlib</b> for statistical representations

Features:
* Works with all csv/xls/xlsx data files containing column headers
* Search across column rows by keyword or numerical range, including rows containing semi-colon separated lists
* Refine data through additional searches
* Pie-chart and Histogram output for visualization of data composition
* Output final data as csv spreadsheet in auto-dated folders with user save names
* Simple, elegant GUI with user input through listbox and text entry, as well as color-coded output console, mouse-hover information and pop-up messageboxes

The end goal is an efficient, multifaceted interface for combing through very large sets of data.
