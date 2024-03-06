import pickle
import numpy as np
import xarray as xr
import math
import shapefile as shp
import geopandas as gp
import regionmask
from numpy import nan
from paths import countryfilepaths,contfilepaths,basinfilepaths,usafilepath

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

# From Isla's shapefile_utils, changed to take list of level 0 files
def masklev0(listl0,dat4mask,mtype):
    """ Generate a mask using information from a shapefile.  Mask will have 1's 
    within the desired region, nan's everywhere else
    Input: 
        listl0 = list of level 0 object names (e.g., country, continent)
        dat4mask = the data that you're planning to mask
    Output:
        mask = the mask
    """

    # setup of the grid for the mask from dat4mask
    maskcoords = xr.Dataset({'lat' : (['lat'],dat4mask['lat'].values)}, {'lon' : (['lon'],dat4mask['lon'].values)})

    mask = np.zeros([maskcoords.lat.size, maskcoords.lon.size])

    for i in range(0,len(listl0),1):
        if mtype=='country':
            shpfile=countryfilepaths(listl0[i],lev=0)
        elif mtype=='continent':
            shpfile=contfilepaths(retname(listl0[i]))
        elif mtype=='basincontinent':
            shpfile=basinfilepaths(listl0[i],lev=1)
        print("masking "+listl0[i]) 
        # read in shapefile
        lev0 = gp.read_file(shpfile)
        maskt = regionmask.mask_geopandas(lev0, maskcoords["lon"], maskcoords["lat"])
        maskt = np.where(np.isnan(maskt), 0, 1)
        mask[:,:] = mask[:,:] + maskt[:,:]

    # ensure unmasked region is set to 1, rest set to nan's
    mask = np.where(mask == 0, nan, 1)
    mask = xr.DataArray(mask, coords=maskcoords.coords)

    return mask

# From Isla's shapefile_utils
def masklev1(parentlev,dat4mask,relist,mtype):
    """ Generate a mask using information from a shapefile.  Mask will have 1's 
    within the desired region, nan's everywhere else
    Input: 
        parentlev = level 0 object name (e.g., country, continent)
        dat4mask = the data that you're planning to mask
        relist = list of subregions ('all' for all subregions)
        mtype= mask type, e.g. country, basins
    Output:
        mask = the mask
    """

    # setup of the grid for the mask from dat4mask
    maskcoords = xr.Dataset({'lat' : (['lat'],dat4mask['lat'].values)}, {'lon' : (['lon'],dat4mask['lon'].values)})

    mask = np.zeros([maskcoords.lat.size, maskcoords.lon.size])

    if mtype=='country':
        shpfile=gp.read_file(countryfilepaths(parentlev,lev=1))
    elif mtype=='basins':
        idname='HYBAS_ID'
        shpfile=gp.read_file(basinfilepaths(parentlev,lev=2))
    elif mtype=='state':
        idname='NAME_1'
        shpfile=gp.read_file(usafilepath())

    for i,re in enumerate(relist):
        print("masking "+str(re)) 
        # read in shapefile
        lev1 = shpfile[shpfile[idname]==re]
        maskt = regionmask.mask_geopandas(lev1, maskcoords["lon"], maskcoords["lat"])
        maskt = np.where(np.isnan(maskt), 0, 1)
        mask[:,:] = mask[:,:] + maskt[:,:]

    # ensure unmasked region is set to 1, rest set to nan's
    mask = np.where(mask == 0, nan, 1)
    mask = xr.DataArray(mask, coords=maskcoords.coords)

    return mask

def settype(relb):
    mtype={
            'af'        :'country',
            'ic'        :'country',
            'fc'        :'state',
            'cp'        :'state',
            'sa'        :'country',
            'se'        :'state',
            'us'        :'country',
            }
    return mtype[relb]

def regionsets(relb):
    lc={
            'af'        :['botswana','zambia','zimbabwe'],
            'ic'        :['cambodia','laos','vietnam'],
            'fc'        :['Utah','Colorado','New Mexico','Arizona'],
            'cp'        :['Kansas','Nebraska','Missouri','Iowa'],
            'sa'        :['bolivia','brazil','paraguay'],
            'se'        :['Tennessee','North Carolina',
                          'Mississippi','Alabama','Georgia',
                          'South Carolina','Florida'],
            'us'        :['usa'],
            }
    return lc[relb]

def retname(re):
    lc={
            'af'        :'Africa',
            'an'        :'Antarctica',
            'ar'        :'Arctic',
            'as'        :'Asia',
            'au'        :'Australia',
            'eu'        :'Europe',
            'ic'        :'Indochina',
            'gr'        :'Greenland',
            'na'        :'North America',
            'oc'        :'Oceania',
            'sa'        :'South America',
            'se'        :'Southeast US',
            'si'        :'Siberia',
            'fc'        :'Four Corners',
            'cp'        :'Central Plains',
            'us'        :'United States',
            }
    return lc[re]

def window(relb):
    lonlat={
            'af'        :[-25,55,-40,40],
            'ar'        :[-180,50,50,80],
            'as'        :[50,150,0,60],
            'au'        :[90,180,-50,15],
            'eu'        :[-25,75,10,80],
            'ic'        :[90,120,0,30],
            'gr'        :[-75,-10,55,85],
            'na'        :[-140,-50,5,60],
            'sa'        :[-90,-30,-60,20],
            'si'        :[60,180,45,80],
            }
    return lonlat[relb] 

def refigsize(relb):
    fs={
            'af'        :(8,9),
            'ic'        :(9,8),
            'sa'        :(8,9),
            }
    return fs[relb] 
