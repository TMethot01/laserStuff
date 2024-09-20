import h5py
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from curveFitting import exponentialFit, fourierFit, gaussian


f = h5py.File("NoiseMeasurement_sweep_00000 (1).h5", 'r') # if you have a different file name or path change it here

#print(list(f.keys()))
#dset = f['004']
#print(dset)
#print(dset.name)


def printname(name):
    print(name)

#f.visit(printname)

#dsetx = list(f['006']['dev2467']['demods']['4']['sample']['y'])
#dsety = list(f['006']['dev2467']['demods']['4']['sample']['tc'])

#plt.plot(dsetx, dsety)
#plt.show()

for trial in list(f.keys()):
    sampleGroup = f[trial]['dev2467']['demods']['4']['sample']
    
    # Add any variables you want here. Follow the same syntax and just add whatever dataset you want in the last [''].
    dsetx = list(sampleGroup['x'])
    dsety = list(sampleGroup['y'])
    dsettc = list(sampleGroup['tc'])
    dsetfreq = list(sampleGroup['frequency'])
    dsetxstddev = list(sampleGroup['xstddev'])

    #xfit = fourierFit(dsettc, dsetx, n=18)  # this is the fourier fit that also doesn't really seem to work.


    # Here is the setup for the gaussian fit. It looks like a straight line on the graph, not sure why.
    initial_guess = [np.max(dsetx), dsettc[np.argmax(dsetx)], 1.0, np.min(dsetx)]
    poptx, pcovx = curve_fit(gaussian, dsettc, dsetx, p0=initial_guess)
    A_fit, x0_fit, sigma_fit, baseline_fit = poptx
    gaussian_x_fit = gaussian(dsettc, A_fit, x0_fit, sigma_fit, baseline_fit)


    # Here is the setup for the polynomial fit. It never goes high enough to identify any peaks.
    tcxfit = np.polyfit(dsettc, dsetx, deg=6)
    tcp = np.linspace(dsettc[0], dsettc[-1], 150)
    p = np.poly1d(tcxfit)
    

    #print({"x": dsettc, "y": dsetx})
    plt.plot(dsettc, dsetx, label="X")  # regular tc vs x
    plt.plot(tcp, p(tcp))   # polynomial fit
    plt.plot(dsettc, gaussian_x_fit, label="gaussian")   # gaussian fit
    #plt.plot(dsettc, xfit, '--')   # fourier fit
    plt.plot(dsettc, dsety, label="Y")   # tc vs y
    plt.title("Trial #" + trial + ": TC vs X, and TC vs Y")
    plt.xlabel("TC")
    plt.ylabel("X & Y")
    plt.legend()
    plt.show()

    plt.plot(dsetfreq, dsetx)  # freq vs x
    plt.title("Trial #" + trial + ": Frequency vs X")
    plt.xlabel("Frequency")
    plt.ylabel("X")
    plt.show()