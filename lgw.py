import h5py
import numpy as np
from pycbc.types.timeseries import TimeSeries

def lensed_strain_fd(newparam=0.0, **kwds):
    hp, hc = get_fd_waveform(approximant="IMRPhenomD", **kwds)

def lensed_strain_td(**kwds):
    return None