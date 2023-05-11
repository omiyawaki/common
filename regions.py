import pickle
import numpy as np

def pointlocs(re):
    if re=='swus':
        iloc=[135,200]
    elif re=='yuma':
        iloc=[130,198]
    elif re=='sahara':
        iloc=[120,10]
    elif re=='sea':
        iloc=[110,85]
    elif re=='amazon':
        iloc=[90,240]
    elif re=='zambia':
        iloc=[80,25]
    return iloc

def rbin(re):
    if re=='sea':
        mt,mq=np.mgrid[280:320:250j,1e-2:3e-2:250j]
    elif re=='swus':
        mt,mq=np.mgrid[280:320:250j,5e-4:1.5e-2:250j]
    return mt,mq

def rinfo(re):
    if re=='sea':
        [rloc,mgr]=pickle.load(open('/project/amp/miyawaki/plots/p004/hist_hotdays/cmip6/jja/fut-his/ssp245/mmm/defsea.t2m.95.ssp245.jja.pickle','rb'))
        # [rloc,mgr]=pickle.load(open('/home/miyawaki/defsea.t2m.95.ssp245.jja.pickle','rb'))
        rlat=mgr[0][:,0]
        rlon=mgr[1][0,:]
    elif re=='swus':
        [rloc,mgr]=pickle.load(open('/project/amp/miyawaki/plots/p004/hist_hotdays/era5/jja/q2m/defswus.q2m.05.jja.pickle','rb'))
        # [rloc,mgr]=pickle.load(open('/home/miyawaki/defswus.q2m.05.jja.pickle','rb'))
        rlat=mgr[0][:,0]
        rlon=mgr[1][0,:]
    return rloc,rlat,rlon

def rlev(re,pc):
    if pc=='':
        if re=='sea':
            levs=np.arange(0,250+5,5)
        elif re=='swus':
            levs=np.arange(0,100+1,5)
    else:
        if re=='sea':
            levs=np.arange(0,250+5,5)
        elif re=='swus':
            levs=np.arange(0,100+5,5)
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

def sellatlon(vn,gr,reg):
    if reg=='nh':
        sla=np.where(gr['lat']>0)[0]
        vn=vn[sla,:]
    elif reg=='sh':
        sla=np.where(gr['lat']<0)[0]
        vn=vn[sla,:]

    return vn
