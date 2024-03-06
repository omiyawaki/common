import numpy as np
import constants as c

def esat(T): # for T [K] compute esat [Pa]
    return 611.2*np.exp(17.67*(T-273.15)/(T-29.65)) # Bolton (1980)

def desat(T): # desat/dT
    return esat(T)*17.67*(273.15-29.65)/(T-29.65)**2
