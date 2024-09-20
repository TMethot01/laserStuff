# HDF5 File viewer

This is a project that is made to view HDF5 files and visualize them using pyplot.

## usage

There are a few tools you can use in this project which are separated into a few different files.

### main.py

This is the main function I was coding and it is kind of a mess, but if ran it will output the graphs of each trial for **tc vs x**, **tc vs y**, and **frequency vs x**. Taking a look a the syntax I used in the program it should be easy to plot any two datasets against eachother along with any fitting functions that you might want. I didn't get the fitting functions to work.

### h5Tools.py

This is a rather small library that holds a function that extracts the file hierarchy from the HDF5 file so that you can see what datasets it contains. The file structure is generated in a new textfile that will appear in the same directory as the program.

### gui.py

***My baby, my baby***. This is a program that works very similarly to main.py, but instead of launching all the plots at you, it opens a gui to select which trial and which files you would like to plot against each other and formats them a bit. This program also has a gaussian fitting applied to it, but it doesn't seem to work too well on the plots that I tried out.

### curveFitting.py

This is my greatest dissapointment. It has a bunch of cool fitting functions in it including exponential, gaussian, and fourier fits, but they all seem to fall **flat** on the data contained in the .h5 file. Feel free to add in any fitting function and import it into main.py and gui.py!

## Acknowledgements

ChatGPT o1-preview wrote a decent amount of this code so I urge you to direct any complaints in its direction. Thank you.
