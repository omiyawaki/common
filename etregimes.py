# Based on Qin Kong's modified ET regime script
# use Hsu's method: scipy.optimize.curve_fit
# doing segmented linear regression on slhf against swvl1 with the aim to classify the data to dry, wet and transitional regime
# fit different segmented model to the data and find which one has lowest AIC/BIC
# extract the critical thresholds that separate transitional regime
# which is then used for calculating sensitivity index within this transitional regime

# try to deal with x0<x1 issue

import os
import sys
import numpy as np
import xarray as xr
from scipy import optimize
from scipy import stats
from tqdm import tqdm

def piecewise3sg_linear(x, x0, x1, y0, k1,k2,k3):
    condlist = [x < x0, (x >= x0) & (x < x1), x >= x1]
    funclist = [lambda x: k1*(x-x0)+y0, lambda x:k2*(x-x0) + y0, lambda x:k3*(x-x1) + k2*(x1-x0) + y0]
    return np.piecewise(x, condlist, funclist)

def fit1110(data):
    SM=data[0]
    LH=data[1]
    n=len(SM)
    param_num=6
    p0=[SM.min()+(SM.max()-SM.min())/3,
        SM.max()-(SM.max()-SM.min())/3,  
        LH.min()+(LH.max()-LH.min())/3,
        0,
        50,
        0]
    bounds=([np.min(np.array(SM)),np.min(np.array(SM)),np.min(np.array(LH)),-0.0010,0,-0.0010],
            [np.max(np.array(SM)),np.max(np.array(SM)),np.max(np.array(LH)),0.0010,np.inf,0.0010])
    res= optimize.curve_fit(piecewise3sg_linear, np.array(SM), np.array(LH),p0=p0,bounds=bounds,full_output=True,maxfev=1e10)
    X=np.r_[SM.min(),res[0][0],res[0][1],SM.max()]
    Y=np.r_[res[0][3]*(SM.min()-res[0][0])+res[0][2],
           res[0][2],
           res[0][4]*(res[0][1]-res[0][0])+res[0][2],
           res[0][5]*(SM.max()-res[0][1])+res[0][4]*(res[0][1]-res[0][0])+res[0][2]]
    Xnew = np.take_along_axis(X, X.argsort(axis=0),axis=0)
    Ynew = np.take_along_axis(Y, X.argsort(axis=0),axis=0)
    Y2=np.interp(SM, Xnew, Ynew)
    MRSS=np.mean((LH - Y2)**2)
    AIC = n * np.log(MRSS) + 2*param_num
    BIC = n * np.log(MRSS) + param_num * np.log(n)
    if "is satisfied" in res[3] or "are satisfied" in res[3]:
        flag=1
    else:
        flag=0
    xc=res[0][1] # critical soil moisture
    mt=res[0][4] # transition regime slope
    return {'type':'1110','flag1':res[4],'flag2':flag,'p':res[0],'AIC':AIC,'BIC':BIC,'line':[Xnew,Ynew],'xc':xc,'yp':Y2,'mt':mt}

def piecewise2sg_linear_LHSflat(x, x0, y0, k1,k2):
    condlist = [x < x0, x >= x0]
    funclist = [lambda x: k1*(x-x0)+y0, lambda x:k2*(x-x0) + y0]
    return np.piecewise(x, condlist, funclist)

def fit1100(data):
    SM=data[0]
    LH=data[1]
    n=len(SM)
    param_num=4
    p0=[SM.min()+(SM.max()-SM.min())/3,
        LH.min()+(LH.max()-LH.min())/3,
        0,
        50]
    bounds=([np.min(np.array(SM)),np.min(np.array(LH)),-0.0010,0],
            [np.max(np.array(SM)),np.max(np.array(LH)),0.0010,np.inf])
    res= optimize.curve_fit(piecewise2sg_linear_LHSflat, np.array(SM), np.array(LH),p0=p0,bounds=bounds,full_output=True,maxfev=1e10)
    X=np.r_[SM.min(),res[0][0],SM.max()]
    Y=np.r_[res[0][1]+(SM.min()-res[0][0])*res[0][2],res[0][1],res[0][1]+res[0][3]*(SM.max()-res[0][0])]
    Y2=np.interp(SM, X, Y)
    MRSS=np.mean((LH - Y2)**2)
    AIC = n * np.log(MRSS) + 2*param_num
    BIC = n * np.log(MRSS) + param_num * np.log(n)
    if "is satisfied" in res[3] or "are satisfied" in res[3]:
        flag=1
    else:
        flag=0
    xc=np.inf
    mt=res[0][3]
    return {'type':'1100','flag1':res[4],'flag2':flag,'p':res[0],'AIC':AIC,'BIC':BIC,'line':[X,Y],'xc':xc,'yp':Y2,'mt':mt}

def piecewise2sg_linear_RHSflat(x, x0, y0, k1,k2):
    condlist = [x < x0, x >= x0]
    funclist = [lambda x: y0+k1*(x-x0), lambda x:k2*(x-x0)+y0]
    return np.piecewise(x, condlist, funclist)

def fit0110(data):
    SM=data[0]
    LH=data[1]
    n=len(SM)
    param_num=4
    p0=[SM.max()-(SM.max()-SM.min())/3,
        LH.max()-(LH.max()-LH.min())/3,
        50,
        0]
    bounds=([np.min(np.array(SM)),np.min(np.array(LH)),0,-0.0010],
            [np.max(np.array(SM)),np.max(np.array(LH)),np.inf,0.0010])
    res= optimize.curve_fit(piecewise2sg_linear_RHSflat, np.array(SM), np.array(LH),p0=p0,bounds=bounds,full_output=True,maxfev=1e10)
    X=np.r_[SM.min(),res[0][0],SM.max()]
    Y=np.r_[res[0][1]-res[0][2]*(res[0][0]-SM.min()),res[0][1],res[0][3]*(SM.max()-res[0][0])+res[0][1]]
    Y2=np.interp(SM, X, Y)
    MRSS=np.mean((LH - Y2)**2)
    AIC = n * np.log(MRSS) + 2*param_num
    BIC = n * np.log(MRSS) + param_num * np.log(n)
    if "is satisfied" in res[3] or "are satisfied" in res[3]:
        flag=1
    else:
        flag=0
    xc=res[0][0]
    mt=res[0][2]
    return {'type':'1100','flag1':res[4],'flag2':flag,'p':res[0],'AIC':AIC,'BIC':BIC,'line':[X,Y],'xc':xc,'yp':Y2,'mt':mt}

def noflat(x,y0,k):
    return k*x+y0

def fit0100(data):
    SM=data[0]
    LH=data[1]
    n=len(SM)
    param_num=2
    p0=[np.median(LH),
        50]
    bounds=([np.min(np.array(LH)),0],
            [np.max(np.array(LH)),np.inf])
    res= optimize.curve_fit(noflat, np.array(SM), np.array(LH),p0=p0,bounds=bounds,full_output=True,maxfev=1e10)
    X=np.r_[SM.min(),SM.max()]
    Y=np.r_[res[0][1]*SM.min()+res[0][0],res[0][1]*SM.max()+res[0][0]]
    Y2=np.interp(SM, X, Y)
    MRSS=np.mean((LH - Y2)**2)
    AIC = n * np.log(MRSS) + 2*param_num
    BIC = n * np.log(MRSS) + param_num * np.log(n)
    if "is satisfied" in res[3] or "are satisfied" in res[3]:
        flag=1
    else:
        flag=0
    xc=np.inf
    mt=res[0][1]
    return {'type':'0100','flag1':res[4],'flag2':flag,'p':res[0],'AIC':AIC,'BIC':BIC,'line':[X,Y],'xc':xc,'yp':Y2,'mt':mt}

def allflat(x,y0):
    return y0

def fit0010(data):
    SM=data[0]
    LH=data[1]
    n=len(SM)
    param_num=1
    p0=np.median(LH)
    bounds=(LH.min(),LH.max())
    res= optimize.curve_fit(allflat, np.array(SM), np.array(LH),p0=p0,bounds=bounds,full_output=True,maxfev=1e10)
    X=np.r_[SM.min(),SM.max()]
    Y=np.r_[res[0][0],res[0][0]]
    Y2=np.interp(SM, X, Y)
    MRSS=np.mean((LH - Y2)**2)
    AIC = n * np.log(MRSS) + 2*param_num
    BIC = n * np.log(MRSS) + param_num * np.log(n)
    if "is satisfied" in res[3] or "are satisfied" in res[3]:
        flag=1
    else:
        flag=0
    xc=np.nan
    mt=np.nan
    return {'type':'0010','flag1':res[4],'flag2':flag,'p':res[0],'AIC':AIC,'BIC':BIC,'line':[X,Y],'xc':xc,'yp':Y2,'mt':mt}


def piecewise2sg_linear_LHSflat_negative_slope(x, x0, y0, k1,k2):
    condlist = [x < x0, x >= x0]
    funclist = [lambda x: k1*(x-x0)+y0, lambda x:k2*(x-x0) + y0]
    return np.piecewise(x, condlist, funclist)

def fit0011(data):
    SM=data[0]
    LH=data[1]
    n=len(SM)
    param_num=4
    p0=[SM.min()+(SM.max()-SM.min())/3,
        LH.min()+(LH.max()-LH.min())/3,
        0,
    -50]
    bounds=([np.min(np.array(SM)),np.min(np.array(LH)),-0.0010,-np.inf],
            [np.max(np.array(SM)),np.max(np.array(LH)),0.0010,0])
    res= optimize.curve_fit(piecewise2sg_linear_LHSflat_negative_slope, np.array(SM), np.array(LH),p0=p0,bounds=bounds,full_output=True,maxfev=1e10)
    X=np.r_[SM.min(),res[0][0],SM.max()]
    Y=np.r_[res[0][1]+(SM.min()-res[0][0])*res[0][2],res[0][1],res[0][1]+res[0][3]*(SM.max()-res[0][0])]
    Y2=np.interp(SM, X, Y)
    MRSS=np.mean((LH - Y2)**2)
    AIC = n * np.log(MRSS) + 2*param_num
    BIC = n * np.log(MRSS) + param_num * np.log(n)
    if "is satisfied" in res[3] or "are satisfied" in res[3]:
        flag=1
    else:
        flag=0
    xc=-np.inf
    mt=np.nan
    return {'type':'0011','flag1':res[4],'flag2':flag,'p':res[0],'AIC':AIC,'BIC':BIC,'line':[X,Y],'xc':xc,'yp':Y2,'mt':mt}

def noflat_negative_slope(x,y0,k):
    return k*x+y0

def fit0001(data):
    SM=data[0]
    LH=data[1]
    n=len(SM)
    param_num=2
    p0=[np.median(LH),
        -50]
    bounds=([np.min(np.array(LH)),-np.inf],
            [np.max(np.array(LH)),0])
    res= optimize.curve_fit(noflat_negative_slope, np.array(SM), np.array(LH),p0=p0,bounds=bounds,full_output=True,maxfev=1e10)
    X=np.r_[SM.min(),SM.max()]
    Y=np.r_[res[0][1]*SM.min()+res[0][0],res[0][1]*SM.max()+res[0][0]]
    Y2=np.interp(SM, X, Y)
    MRSS=np.mean((LH - Y2)**2)
    AIC = n * np.log(MRSS) + 2*param_num
    BIC = n * np.log(MRSS) + param_num * np.log(n)
    if "is satisfied" in res[3] or "are satisfied" in res[3]:
        flag=1
    else:
        flag=0
    xc=-np.inf
    mt=np.nan
    return {'type':'0001','flag1':res[4],'flag2':flag,'p':res[0],'AIC':AIC,'BIC':BIC,'line':[X,Y],'xc':xc,'yp':Y2,'mt':mt}

###
# new fits
def fit0101(data):
    SM=data[0]
    LH=data[1]
    n=len(SM)
    param_num=4
    p0=[SM.min()+(SM.max()-SM.min())/3,
        LH.min()+(LH.max()-LH.min())/3,
        50,
        -50]
    bounds=([np.min(np.array(SM)),np.min(np.array(LH)),0,-np.inf],
            [np.max(np.array(SM)),np.max(np.array(LH)),np.inf,0])
    res= optimize.curve_fit(piecewise2sg_linear_LHSflat_negative_slope, np.array(SM), np.array(LH),p0=p0,bounds=bounds,full_output=True,maxfev=1e10)
    X=np.r_[SM.min(),res[0][0],SM.max()]
    Y=np.r_[res[0][1]+(SM.min()-res[0][0])*res[0][2],res[0][1],res[0][1]+res[0][3]*(SM.max()-res[0][0])]
    Y2=np.interp(SM, X, Y)
    MRSS=np.mean((LH - Y2)**2)
    AIC = n * np.log(MRSS) + 2*param_num
    BIC = n * np.log(MRSS) + param_num * np.log(n)
    if "is satisfied" in res[3] or "are satisfied" in res[3]:
        flag=1
    else:
        flag=0
    xc=res[0][0]
    mt=res[0][2]
    return {'type':'0101','flag1':res[4],'flag2':flag,'p':res[0],'AIC':AIC,'BIC':BIC,'line':[X,Y],'xc':xc,'yp':Y2,'mt':mt}

def fit0111(data):
    SM=data[0]
    LH=data[1]
    n=len(SM)
    param_num=6
    p0=[SM.min()+(SM.max()-SM.min())/3,
        SM.max()-(SM.max()-SM.min())/3,  
        LH.min()+(LH.max()-LH.min())/3,
        50,
        0,
        -50]
    bounds=([np.min(np.array(SM)),np.min(np.array(SM)),np.min(np.array(LH)),0,-0.0010,-np.inf],
            [np.max(np.array(SM)),np.max(np.array(SM)),np.max(np.array(LH)),np.inf,0.0010,0])
    res= optimize.curve_fit(piecewise3sg_linear, np.array(SM), np.array(LH),p0=p0,bounds=bounds,full_output=True,maxfev=1e10)
    X=np.r_[SM.min(),res[0][0],res[0][1],SM.max()]
    Y=np.r_[res[0][3]*(SM.min()-res[0][0])+res[0][2],
           res[0][2],
           res[0][4]*(res[0][1]-res[0][0])+res[0][2],
           res[0][5]*(SM.max()-res[0][1])+res[0][4]*(res[0][1]-res[0][0])+res[0][2]]
    Xnew = np.take_along_axis(X, X.argsort(axis=0),axis=0)
    Ynew = np.take_along_axis(Y, X.argsort(axis=0),axis=0)
    Y2=np.interp(SM, Xnew, Ynew)
    MRSS=np.mean((LH - Y2)**2)
    AIC = n * np.log(MRSS) + 2*param_num
    BIC = n * np.log(MRSS) + param_num * np.log(n)
    if "is satisfied" in res[3] or "are satisfied" in res[3]:
        flag=1
    else:
        flag=0
    xc=res[0][0]
    mt=res[0][3]
    return {'type':'0111','flag1':res[4],'flag2':flag,'p':res[0],'AIC':AIC,'BIC':BIC,'line':[Xnew,Ynew],'xc':xc,'yp':Y2,'mt':mt}

def fit1101(data):
    SM=data[0]
    LH=data[1]
    n=len(SM)
    param_num=6
    p0=[SM.min()+(SM.max()-SM.min())/3,
        SM.max()-(SM.max()-SM.min())/3,  
        LH.min()+(LH.max()-LH.min())/3,
        0,
        50,
        -50]
    bounds=([np.min(np.array(SM)),np.min(np.array(SM)),np.min(np.array(LH)),-0.0010,0,-np.inf],
            [np.max(np.array(SM)),np.max(np.array(SM)),np.max(np.array(LH)),0.0010,np.inf,0])
    res= optimize.curve_fit(piecewise3sg_linear, np.array(SM), np.array(LH),p0=p0,bounds=bounds,full_output=True,maxfev=1e10)
    X=np.r_[SM.min(),res[0][0],res[0][1],SM.max()]
    Y=np.r_[res[0][3]*(SM.min()-res[0][0])+res[0][2],
           res[0][2],
           res[0][4]*(res[0][1]-res[0][0])+res[0][2],
           res[0][5]*(SM.max()-res[0][1])+res[0][4]*(res[0][1]-res[0][0])+res[0][2]]
    Xnew = np.take_along_axis(X, X.argsort(axis=0),axis=0)
    Ynew = np.take_along_axis(Y, X.argsort(axis=0),axis=0)
    Y2=np.interp(SM, Xnew, Ynew)
    MRSS=np.mean((LH - Y2)**2)
    AIC = n * np.log(MRSS) + 2*param_num
    BIC = n * np.log(MRSS) + param_num * np.log(n)
    if "is satisfied" in res[3] or "are satisfied" in res[3]:
        flag=1
    else:
        flag=0
    xc=res[0][1]
    mt=res[0][4]
    return {'type':'1101','flag1':res[4],'flag2':flag,'p':res[0],'AIC':AIC,'BIC':BIC,'line':[Xnew,Ynew],'xc':xc,'yp':Y2,'mt':mt}

def piecewise4sg_linear(x,x0,x1,x2,y0,k1,k2,k3,k4):
    condlist = [x < x0, (x >= x0) & (x < x1), (x>=x1)&(x<x2), x >= x2]
    funclist = [lambda x: k1*(x-x0)+y0, lambda x:k2*(x-x0) + y0, lambda x:k3*(x-x1) + k2*(x1-x0) + y0, lambda x:k4*(x-x2)+k3*(x2-x1)+k2*(x1-x0)+y0]
    return np.piecewise(x, condlist, funclist)

def fit1111(data):
    SM=data[0]
    LH=data[1]
    n=len(SM)
    param_num=8
    p0=[SM.min()+(SM.max()-SM.min())/4,
        SM.min()+(SM.max()-SM.min())/2,  
        SM.max()-(SM.max()-SM.min())/4,  
        LH.min()+(LH.max()-LH.min())/3,
        0,
        50,
        0,
        -50]
    bounds=([np.min(np.array(SM)),np.min(np.array(SM)),np.min(np.array(SM)),np.min(np.array(LH)),-0.0010,0,-0.0010,-np.inf],
            [np.max(np.array(SM)),np.max(np.array(SM)),np.max(np.array(SM)),np.max(np.array(LH)),0.0010,np.inf,0.0010,0])
    res= optimize.curve_fit(piecewise4sg_linear, np.array(SM), np.array(LH),p0=p0,bounds=bounds,full_output=True,maxfev=1e10)
    X=np.r_[SM.min(),res[0][0],res[0][1],res[0][2],SM.max()]
    Y=np.r_[res[0][4]*(SM.min()-res[0][0])+res[0][3],
           res[0][3],
           res[0][5]*(res[0][1]-res[0][0])+res[0][3],
           res[0][6]*(SM.max()-res[0][1])+res[0][5]*(res[0][1]-res[0][0])+res[0][3],
           res[0][7]*(SM.max()-res[0][2])+res[0][6]*(res[0][2]-res[0][1])+res[0][5]*(res[0][1]-res[0][0])+res[0][3] ]
    Xnew = np.take_along_axis(X, X.argsort(axis=0),axis=0)
    Ynew = np.take_along_axis(Y, X.argsort(axis=0),axis=0)
    Y2=np.interp(SM, Xnew, Ynew)
    MRSS=np.mean((LH - Y2)**2)
    AIC = n * np.log(MRSS) + 2*param_num
    BIC = n * np.log(MRSS) + param_num * np.log(n)
    if "is satisfied" in res[3] or "are satisfied" in res[3]:
        flag=1
    else:
        flag=0
    xc=res[0][1]
    mt=res[0][5]
    return {'type':'1111','flag1':res[4],'flag2':flag,'p':res[0],'AIC':AIC,'BIC':BIC,'line':[Xnew,Ynew],'xc':xc,'yp':Y2,'mt':mt}

#
###

def remove_outlier(SM,LH):
    LH_copy=np.sort(LH)
    thre=0
    for k in range(50):
        tmp0=LH_copy[-1-k]
        tmp1=LH_copy[-1-(k+1)]
        if tmp0-tmp1<50:
            continue
        else:
            thre=tmp0
    if thre>0:
        SMnew=SM[np.where(LH<thre)]
        LHnew=LH[np.where(LH<thre)]
    else:
        SMnew=SM
        LHnew=LH
    SMnew2=SMnew[np.where(~np.isnan(SMnew))]
    LHnew2=LHnew[np.where(~np.isnan(SMnew))]
    return [SMnew2,LHnew2]

def runfit(sm,lf,fitfunc):
    # remove outliers
    # sm,lf=remove_outlier(sm,lf)

    return fitfunc([sm,lf])

def bestfit(sm,lf):
    #################################
    # fit various segment models
    #################################
    fmodels=[fit1111,fit0111,fit1110,fit1100,fit0110,fit0100,fit0010,fit0011,fit0001]
    # fmodels=[fit1111,fit0111,fit0101,fit1101,fit1110,fit1100,fit0110,fit0100,fit0010,fit0011,fit0001]
    lfits=[runfit(sm,lf,fitfunc) for fitfunc in fmodels]

    lcrit1=[fit['AIC'] for fit in lfits]
    lcrit2=[fit['BIC'] for fit in lfits]

    # best fit determined by min[AIC,BIC]
    bfits=[ lfits[lcrit1.index(min(lcrit1))],
            lfits[lcrit2.index(min(lcrit2))]] 

    return bfits

def bestfit_ef(sm,lf):
    #################################
    # fit various segment models
    #################################
    fmodels=[fit1110,fit0110,fit1100,fit0010]
    lfits=[runfit(sm,lf,fitfunc) for fitfunc in fmodels]

    lcrit1=[fit['AIC'] for fit in lfits]
    lcrit2=[fit['BIC'] for fit in lfits]

    # best fit determined by min[AIC,BIC]
    bfits=[ lfits[lcrit1.index(min(lcrit1))],
            lfits[lcrit2.index(min(lcrit2))]] 

    return bfits

def bestfit_hd22(sm,lf):
    #################################
    # fit various segment models
    #################################
    fmodels=[fit1110,fit1100,fit0110,fit0100,fit0010]
    lfits=[runfit(sm,lf,fitfunc) for fitfunc in fmodels]

    lcrit1=[fit['AIC'] for fit in lfits]
    lcrit2=[fit['BIC'] for fit in lfits]

    # best fit determined by min[AIC,BIC]
    bfits=[ lfits[lcrit1.index(min(lcrit1))],
            lfits[lcrit2.index(min(lcrit2))]] 

    return bfits
