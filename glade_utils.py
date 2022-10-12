def mctr(md):
    # DESCRIPTION
    # Returns the model center name applicable for the model

    # INPUT
    # md    : STRING describing the model (e.g., ACCESS-CM1)
    
    # OUTPUT 
    # ctr   : STRING of model center name

    if md in ['ACCESS-CM2']:
        ctr='CSIRO-ACCSSR'
    elif md in ['CESM2','CESM2-WACCM']:
        ctr='NCAR'
    elif md in ['CNRM-CM6-1','CNRM-CM6-1-HR','CNRM-ESM2-1']:
        ctr='CNRM-CERFACS'
    elif md in ['CanESM5','CanESM5-CanOE']:
        ctr='CCCma'
    elif md in ['MIROC-ES2L']:
        ctr='MIROC'
    elif md in ['NorESM2-LM','NorESM2-MM']:
        ctr='NCC'

    return ctr

def adte(fo,cl,md):
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

def grid(fo,cl,md):
    # DESCRIPTION
    # Returns the grid name applicable for the type of run, model

    # INPUT
    # fo    : STRING describing the forcing (e.g., ssp245)
    # cl    : STRING describing the climatology (fut=future, his=historical)
    # md    : STRING describing the model (e.g., ACCESS-CM1)
    
    # OUTPUT 
    # grid   : STRING of grid name
    
    if md in ['ACCESS-CM2','ACCESS-ESM1-5','BCC-CSM2-MR','CanESM5','CESM2-WACCM','HadGEM3-GC31-LL','MIROC-ES2L','MPI-ESM1-2-LR','MRI-ESM2-0','NorESM2-LM','UKESM1-0-LL']:
        grd='gn'
    elif md in ['CNRM-CM6-1','CNRM-ESM2-1','KACE-1-0-G']:
        grd='gr'

    return grd

