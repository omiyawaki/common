import pickle
import numpy as np

def rbin(re):
    if re=='sea':
        mt,mq=np.mgrid[285:310:250j,1.25e-2:2.25e-2:250j]
    elif re=='swus':
        mt,mq=np.mgrid[285:310:250j,5e-4:1.5e-2:250j]
    return mt,mq

def rinfo(re):
    if re=='sea':
        [rloc,mgr]=pickle.load(open('/project/amp/miyawaki/plots/p004/hist_hotdays/cmip6/jja/fut-his/ssp245/mmm/defsea.t2m.95.ssp245.jja.pickle','rb'))
        rlat=mgr[0][:,0]
        rlon=mgr[1][0,:]
    elif re=='swus':
        [rloc,mgr]=pickle.load(open('/project/amp/miyawaki/plots/p004/hist_hotdays/era5/jja/q2m/defswus.q2m.05.jja.pickle','rb'))
        rlat=mgr[0][:,0]
        rlon=mgr[1][0,:]
    return rloc,rlat,rlon

def rlev(re,pc):
    if pc=='':
        if re=='sea':
            levs=np.arange(0,100+10,10)
        elif re=='swus':
            levs=np.arange(0,10+1,1)
    else:
        if re=='sea':
            levs=np.arange(0,250+25,25)
        elif re=='swus':
            levs=np.arange(0,50+5,5)
    return levs

def rtlm(re,pc):
    if pc=='':
        if re=='sea':
            tlim=[285,310]
        elif re=='swus':
            tlim=[285,315]
    else:
        if re=='sea':
            tlim=[300,310]
        elif re=='swus':
            tlim=[300,315]
    return tlim
