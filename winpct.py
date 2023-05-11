# Brian Medeiros' windowed quantile calculator
# https://github.com/brianpm/TemperatureExtremes/blob/master/notebooks/Save_Quantile_Dataset.ipynb

import numpy as np

def get_window_indices(thing, current, look_back, look_ahead):
    """Given an iterable, thing, return the values of thing in circular slice. Go back look_back steps and
       go ahead look_ahead steps.
    """
    N = len(thing)-1
    window_inds = np.arange(-1*(look_back), look_ahead+1)
    result = []
    for w in window_inds:
        result.append(thing[(current + w) % N])
    return np.array(result)  # these are the values of thing

def get_our_pct(data,pcts):
    return np.nanpercentile(data, pcts, axis=0, overwrite_input=False, interpolation='linear', keepdims=False)
