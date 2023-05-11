import numpy as np

def mctr(md):
    # DESCRIPTION
    # Returns the model center name applicable for the model

    # INPUT
    # md    : STRING describing the model (e.g., ACCESS-CM1)
    
    # OUTPUT 
    # ctr   : STRING of model center name

    if md in ['CanESM5','CanESM5-CanOE']:
        ctr='CCCma'
    elif md in ['CNRM-CM6-1','CNRM-CM6-1-HR','CNRM-ESM2-1']:
        ctr='CNRM-CERFACS'
    elif md in ['ACCESS-CM2']:
        ctr='CSIRO-ACCSSR'
    elif md in ['MIROC-ES2L']:
        ctr='MIROC'
    elif md in ['CESM2','CESM2-WACCM']:
        ctr='NCAR'
    elif md in ['NorESM2-LM','NorESM2-MM']:
        ctr='NCC'
    elif md in ['KACE-1-0-G','UKESM1-0-LL']:
        ctr='NIMS-KA'
    elif md in ['GFDL-CM4','GFDL-ESM4']:
        ctr='NOAA-GFDL'
    elif md in ['NESM3']:
        ctr='NUIST'
    elif md in ['CIESM']:
        ctr='THU'
    elif md in ['MCM-UA-1-0']:
        ctr='UA'

    return ctr

def adte(md):
    # DESCRIPTION
    # Returns the access date applicable for the model (for glade CMIP storage)

    # INPUT
    # md    : STRING describing the model (e.g., ACCESS-CM1)
    
    # OUTPUT 
    # ctr   : STRING of model center name

    if md in ['ACCESS-CM2','NorESM2-L']:
        ctr='v20191108'
    elif md in ['CanESM5']:
        ctr='v20190429'
    elif md in ['CESM2-WACCM']:
        ctr='v20190815'
    elif md in ['CNRM-CM6-1']:
        ctr='v20190219'
    elif md in ['MIROC-ES2L']:
        ctr='v20200318'

    return ctr

def grid(md):
    # DESCRIPTION
    # Returns the grid name applicable for the type of run, model

    # INPUT
    # fo    : STRING describing the forcing (e.g., ssp245)
    # md    : STRING describing the model (e.g., ACCESS-CM1)
    
    # OUTPUT 
    # grid   : STRING of grid name
    
    if md in ['ACCESS-CM2','ACCESS-ESM1-5','AWI-ESM-1-1-LR','AWI-CM-1-1-MR','BCC-CSM2-MR','BCC-ESM1','CanESM5','CESM2','CESM2-WACCM','CMCC-CM2-SR5','CMCC-ESM2','FGOALS-g3','HadGEM3-GC31-LL','IITM-ESM','MIROC-ES2L','MIROC6','MPI-ESM-1-2-HAM','MPI-ESM1-2-HR','MPI-ESM1-2-LR','MRI-ESM2-0','NorESM2-LM','NorESM2-MM','TaiESM1','UKESM1-0-LL']:
        grd='gn'
    elif md in ['CNRM-CM6-1','CNRM-ESM2-1','EC-Earth3','EC-Earth3-AerChem','EC-Earth3-Veg','EC-Earth3-Veg-LR','KACE-1-0-G','IPSL-CM5A2-INCA','IPSL-CM6A-LR']:
        grd='gr'
    elif md in ['GFDL-CM4']:
        grd='gr2'
    elif md in ['GFDL-ESM4','INM-CM4-8','INM-CM5-0']:
        grd='gr1'

    return grd

def smile(md,fo,varn):
    if fo=='historical':
        if md=='ACCESS-CM2':
            le=[f'r{i}i1p1f1' for i in range(1,41)]
        elif md=='CanESM5':
            le=[f'r{i}i1p1f1' for i in range(1,26)]
            le=le+([f'r{i}i1p1f1' for i in range(1,26)])
        elif md=='CanESM5-1':
            le=[f'r{i}i1p1f1' for i in range(1,11)]
            le=le+([f'r{i}i1p1f1' for i in range(1,11)])
        elif md=='EC-Earth3':
            le=[f'r{i}i1p1f1' for i in [1,4,5,6,9,11,13,15]]
            if not varn=='mrsos':
                le=le+[f'r{i}i1p1f1' for i in range(101,151)]
        elif md=='MIROC6':
            if varn=='mrsos':
                le=[f'r{i}i1p1f1' for i in range(1,4)]
            else:
                le=[f'r{i}i1p1f1' for i in range(1,51)]
        elif md=='MPI-ESM1-2-LR':
            le=[f'r{i}i1p1f1' for i in range(1,31)]
        elif md=='UKESM1-0-LL':
            le=[f'r{i}i1p1f1' for i in range(1,19)]

    elif fo=='ssp370':
        if md=='ACCESS-CM2':
            le=[f'r{i}i1p1f1' for i in range(1,41)]
        elif md=='CanESM5':
            le=[f'r{i}i1p1f1' for i in range(1,26)]
            le=le+([f'r{i}i1p1f1' for i in range(1,26)])
        elif md=='CanESM5-1':
            le=[f'r{i}i1p1f1' for i in range(1,11)]
            le=le+([f'r{i}i1p1f1' for i in range(1,11)])
        elif md=='EC-Earth3':
            le=[f'r{i}i1p1f1' for i in [1,4,5,6,9,11,13,15]]
            if not varn=='mrsos':
                le=le+[f'r{i}i1p1f1' for i in range(101,151)]
        elif md=='MIROC6':
            if varn=='mrsos':
                le=[f'r{i}i1p1f1' for i in range(1,4)]
            else:
                le=[f'r{i}i1p1f1' for i in range(1,51)]
        elif md=='MPI-ESM1-2-LR':
            le=[f'r{i}i1p1f1' for i in range(1,31)]
        elif md=='UKESM1-0-LL':
            le=[f'r{i}i1p1f1' for i in range(1,19)]

    return le

def inctype(md):
    # Outputs type of history file increments
    if md in ['EC-Earth3','EC-Earth3-Veg']:
        return 1
    elif md in ['MPI-ESM1-2-HR']:
        return 5

def listyr(md,byr,ygwl=None):
    n=inctype(md)
    if ygwl is not None:
        yrs=np.arange(np.floor((ygwl-11)/n)*n,np.ceil((ygwl[1]+11)/n)*n,n)
    else:
        yrs=np.arange(np.floor((byr[0]-1)/n)*n,np.ceil((byr[1]+1)/n)*n,n)
    lyr=['%i0101-%i1231'%(yr,yr+n-1) for yr in yrs]

    # edge cases
    if n==5:
        if byr[1]==2100:
            lyr[-1]='21000101-21001231'

    return lyr

def ishr(md):
    # Outputs whether model is high resolution
    if md in ['EC-Earth3','EC-Earth3-Veg','MPI-ESM1-2-HR']:
        return True
    else:
        return False
