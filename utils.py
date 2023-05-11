import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def rainmap(nbin):
    cmap_name = 'rainmap'
    colors = ['white',[92/255,146/255,176/255],[111/255,182/255,86/255],[234/255,228/255,112/255],[134/255,35/255,32/255]]
    return LinearSegmentedColormap.from_list(cmap_name, colors, N=nbin)

def monname(m):
    monlist={
            0:'January',
            1:'February',
            2:'March',
            3:'April',
            4:'May',
            5:'June',
            6:'July',
            7:'August',
            8:'September',
            9:'October',
            10:'November',
            11:'December',
            }
    return monlist[m]

def corr(a,b,dim):
    # computes correlation coefficient between arrays
    # a and b along axis dim
    ma=np.nanmean(a,axis=dim,keepdims=True)
    mb=np.nanmean(b,axis=dim,keepdims=True)
    cov=np.nanmean((a-ma)*(b-mb),axis=dim,keepdims=True)
    sa=np.nanstd(a,axis=dim,keepdims=True)
    sb=np.nanstd(b,axis=dim,keepdims=True)
    return np.squeeze(cov/(sa*sb))

def corr2d(a,b,gr,dim,**kwargs): # area-weighted correlation
    # computes correlation coefficient between arrays
    # a and b along axis dim
    lm=kwargs.get('lm',np.ones([a.shape[-2],a.shape[-1]]))
    w=np.cos(np.deg2rad(gr['lat']))
    denom=np.nansum(lm*np.transpose(np.tile(w,(a.shape[-1],1)),[1,0]))
    w=np.transpose(np.tile(w,(a.shape[-1],a.shape[0],a.shape[1],a.shape[2],1)),[1,2,3,4,0])
    ma=np.nansum(w*a,axis=dim,keepdims=True)/denom
    mb=np.nansum(w*b,axis=dim,keepdims=True)/denom
    cov=np.nansum(w*(a-ma)*(b-mb),axis=dim,keepdims=True)/denom
    vara=np.nansum(w*(a-ma)**2,axis=dim,keepdims=True)/denom
    varb=np.nansum(w*(b-mb)**2,axis=dim,keepdims=True)/denom
    return np.squeeze(cov/np.sqrt((vara*varb)))
