import numpy as np
from symfit import parameters, variables, sin, cos, Fit



def exponentialFit(x, a, b, c):
    return a * np.exp(-b * x) + c



def sinFit(x, a, b, c, d, e):
    return np.sin(x)



def fourierSeries(x, f, n=0):
    a0, *cos_a = parameters(','.join(['a{}'.format(i) for i in range(0, n + 1)]))
    sin_b = parameters(','.join(['b{}'.format(i) for i in range(1, n + 1)]))

    series = a0 + sum(ai * cos(i * f * x) + bi * sin(i * f * x)
                    for i, (ai, bi) in enumerate(zip(cos_a, sin_b), start=1))
    return series

def fourierFit(xdata, ydata, n=2):
        
    x, y = variables('x, y')
    w, = parameters('w')

    xdata = np.asarray(xdata, dtype=float)
    ydata = np.asarray(ydata, dtype=float)

    model_dict = {y: fourierSeries(x, f=w, n=n)}
    print(model_dict)

    fit = Fit(model_dict, x=xdata, y=ydata)
    fit_result = fit.execute()
    print(fit_result.params)
    print(fit_result.params['a0']+fit_result.params['a0']*np.cos(fit_result.params['w']*xdata)+fit_result.params['b1']*np.sin(fit_result.params['w']*xdata))
    evaluated_model = fit.model(x=xdata, **fit_result.params).y
    y_fit = evaluated_model
    return y_fit



def gaussian(x, A, x0, sigma, baseline):
    return baseline + A * np.exp(-((x-x0) ** 2) / (2 * sigma ** 2))