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
    cov=np.nansum((a-ma)*(b-mb),axis=dim,keepdims=True)
    vara=np.nansum((a-ma)**2,axis=dim,keepdims=True)
    varb=np.nansum((b-mb)**2,axis=dim,keepdims=True)
    return np.squeeze(cov/(np.sqrt(vara*varb)))

def corr2d(a,b,gr,dim,**kwargs): # area-weighted correlation
    # computes correlation coefficient between arrays
    # a and b along axis dim
    lm=kwargs.get('lm',np.ones([a.shape[-2],a.shape[-1]]))
    w=np.cos(np.deg2rad(gr['lat']))
    denom=np.nansum(lm*np.transpose(np.tile(w,(a.shape[-1],1)),[1,0]))
    try:
        w=np.transpose(np.tile(w,(a.shape[-1],1)),[1,0])
    except:
        w=np.transpose(np.tile(w,(a.shape[-1],a.shape[0],a.shape[1],a.shape[2],1)),[1,2,3,4,0])
    ma=np.nansum(w*a,axis=dim,keepdims=True)/denom
    mb=np.nansum(w*b,axis=dim,keepdims=True)/denom
    cov=np.nansum(w*(a-ma)*(b-mb),axis=dim,keepdims=True)/denom
    vara=np.nansum(w*(a-ma)**2,axis=dim,keepdims=True)/denom
    varb=np.nansum(w*(b-mb)**2,axis=dim,keepdims=True)/denom
    return np.squeeze(cov/np.sqrt((vara*varb)))

def varnlb(vn):
    lbs={
            'tas':          'T',
            'ta850':        'T_{850}',
            'twas':         'T_w',
            'hurs':         'RH',
            'sfcWind':      'U',
            'pr':           'P',
            'gflx':         'G',
            'huss':         'q',
            'hurs':         'RH',
            'fsm':          'F_{snowmelt}',
            'snc':          '\mathrm{Snow\,Concentration}',
            'rsfc':         'R_{SFC}',
            'lwsfc':        'LW',
            'swsfc':        'SW',
            'lh2ce':        'L_v \\rho U (q^*-q)',
            'lhflx':        'LH',
            'qsum':         'LH_{\mathrm{soil+vegE+vegT}}',
            'qsoil':        'LH_{\mathrm{soil}}',
            'qvege':        'LH_{\mathrm{vegE}}',
            'qvegt':        'LH_{\mathrm{vegT}}',
            'hfls':         'LH',
            'hfss':         'SH',
            'mrsos':        'SM',
            'td_mrsos':     'SM_{\mathrm{30\,d}}',
            'ti_pr':        'P_{\mathrm{30\,d}}',
            'ti_ev':        '-E_{\mathrm{30\,d}}',
            'ti_ro':        '-R_{\mathrm{30\,d}}',
            'csm':          'SM_\mathrm{crit}',
            'ef':           'EF',#'LH/R_{SFC}',
            'ef2':          'LH/(LH+SH)',
            'ef3':          'LH/(SW_{net}+LW_\downarrow)',
            'blh':          'LH_{\mathrm{bulk}}',
            'plh':          'LH_{BC}',
            'plh_fixbc':    'LH_{BChist}',
            'ooef':         'LH/R_{SFC}',
            'ooef2':        'LH/(LH+SH)',
            'ooef3':        'LH/(SW_{net}+LW_\downarrow)',
            'oosf':         'SH/R_{SFC}',
            'oosf2':        'SH/(LH+SH)',
            'oopef':        'EF',
            'oopef2':       'LH/(LH+SH)_{BC}',
            'oopef3':       'LH/(SW_{net}+LW_\downarrow)',
            'oopef_fixbc':  'EF_{BChist}',
            'oopef3_fixbc': 'LH/(SW_{net}+LW_\downarrow)_{BChist}',
            'ooblh':        'LH_{\mathrm{bulk}}',
            'ooplh':        'LH_{BC}',
            'ooplh10':      'LH_{BC10}',
            'ooplh100':     'LH_{BC100}',
            'ooplh200':     'LH_{BC200}',
            'ooplh300':     'LH_{BC300}',
            'ooplh400':     'LH_{BC400}',
            'ooplh500':     'LH_{BC500}',
            'ooplh600':     'LH_{BC600}',
            'ooplh700':     'LH_{BC700}',
            'ooplh800':     'LH_{BC800}',
            'ooplh10.qvegt': 'LH_{BC10,qvegt}',
            'ooplh100.qvegt':'LH_{BC100,qvegt}',
            'ooplh200.qvegt':'LH_{BC200,qvegt}',
            'ooplh300.qvegt':'LH_{BC300,qvegt}',
            'ooplh_orig':   'LH_{BC}',
            'ooplh_msm':    'LH_{\Delta\delta\,SM=0}',
            'ooplh_fixmsm': 'LH_{\Delta\delta\,SM=0}',
            'ooplh_fixasm': 'LH_{\Delta\delta\,SM=0}',
            'ooplh_mmmbc':  'LH_{MMM\,BC}',
            'ooplh_mmmsm':  'LH_{MMM\,SM}',
            'ooplh_fixbc':  'LH_{BChist}',
            'ooplh_fixbc10': 'LH_{BChist10}',
            'ooplh_fixbc100':'LH_{BChist100}',
            'ooplh_fixbc200':'LH_{BChist200}',
            'ooplh_fixbc300':'LH_{BChist300}',
            'ooplh_rbcsm':  'LH',
            'ooplh_rddsm':  'LH_{\Delta\delta\,SM}',
            'ooplh_dbc':    'LH_{SMhist}',
            'ooplh_mtr':    'LH_{\partial_{SM}LH}',
            'oopef_msm':    'EF_{\Delta\delta\,SM=0}',
            'oopef_fixmsm': 'EF_{\Delta\delta\,SM=0}',
            'oopef_fixasm': 'EF_{\Delta\delta\,SM=0}',
            'oopef_mmmbc':  'EF_{MMM\,BC}',
            'oopef_mmmsm':  'EF_{MMM\,SM}',
            'oopef_fixbc':  'EF_{BChist}',
            'oopef_rbcsm':  'EF',
            'oopef_rddsm':  'EF',
            'oopef_dbc':    'EF_{SMhist}',
            'oopef_mtr':    'EF_{\partial_{SM}EF}',
            'ooai':         '0.8R_{sfc}/L_vP',
            'annai':        '0.8R_{sfc}/L_vP',
            'rfa':          r'(-\langle\nabla\cdot F_a\rangle)',
            'pblh':         r'\mathrm{PBLH}',
            'wap850':       r'\omega_{850}',
            'wapt850':      r'(\omega T)_{850}',
            'fa850':        r'(-\nabla\cdot F_{a,\,850})',
            'fat850':       r'(-\nabla\cdot (vc_pT)_{850})',
            'advt850_wm2':  r'\rho z_{850}(-uc_p\partial_xT-vc_p\partial_yT)_{850}',
            'advt850':      r'(-uc_p\partial_xT-vc_p\partial_yT)_{850}',
            'advtx850':     r'(-uc_p\partial_xT)_{850}',
            'advty850':     r'(-vc_p\partial_yT)_{850}',
            'advm850':      r'(-u\partial_xm-v\partial_ym)_{850}',
            'advmx850':     r'(-u\partial_xm)_{850}',
            'advmy850':     r'(-v\partial_ym)_{850}',
            }
    return lbs[vn]

def unitlb(vn):
    lbs={
            'tas':          'K',
            'ta850':        'K',
            'twas':         'K',
            'hurs':         '%',
            'huss':         'kg kg${-1}$',
            'ooai':         'unitless',
            'annai':        'unitless',
            'sfcWind':      'm s$^{-1}$',
            'pr':           'mm d$^{-1}$',
            'gflx':         'W m$^{-2}$',
            'fsm':          'W m$^{-2}$',
            'rsfc':         'W m$^{-2}$',
            'lwsfc':        'W m$^{-2}$',
            'swsfc':        'W m$^{-2}$',
            'lhflx':        'W m$^{-2}$',
            'qsum':         'W m$^{-2}$',
            'qsoil':        'W m$^{-2}$',
            'qvege':        'W m$^{-2}$',
            'qvegt':        'W m$^{-2}$',
            'hfls':         'W m$^{-2}$',
            'hfss':         'W m$^{-2}$',
            'lh2ce':        'W m$^{-2}$',
            'mrsos':        'kg m$^{-2}$',
            'td_mrsos':     'kg m$^{-2}$',
            'ti_pr':        'kg m$^{-2}$',
            'ti_ev':        'kg m$^{-2}$',
            'ti_ro':        'kg m$^{-2}$',
            'csm':          'kg m$^{-2}$',
            'snc':          'unitless',
            'ef':           'unitless',
            'ef2':          'unitless',
            'ef3':          'unitless',
            'blh':          'W m$^{-2}$',
            'plh':          'W m$^{-2}$',
            'plh_fixbc':    'W m$^{-2}$',
            'ooef':         'unitless',
            'ooef2':        'unitless',
            'ooef3':        'unitless',
            'oosf':         'unitless',
            'oosf2':        'unitless',
            'oopef':        'unitless',
            'oopef2':       'unitless',
            'oopef3':       'unitless',
            'oopef_fixbc':  'unitless',
            'oopef3_fixbc': 'unitless',
            'ooblh':        'W m$^{-2}$',
            'ooplh':        'W m$^{-2}$',
            'ooplh10':      'W m$^{-2}$',
            'ooplh100':     'W m$^{-2}$',
            'ooplh200':     'W m$^{-2}$',
            'ooplh300':     'W m$^{-2}$',
            'ooplh400':     'W m$^{-2}$',
            'ooplh500':     'W m$^{-2}$',
            'ooplh600':     'W m$^{-2}$',
            'ooplh700':     'W m$^{-2}$',
            'ooplh800':     'W m$^{-2}$',
            'ooplh10.qvegt': 'W m$^{-2}$',
            'ooplh100.qvegt':'W m$^{-2}$',
            'ooplh200.qvegt':'W m$^{-2}$',
            'ooplh300.qvegt':'W m$^{-2}$',
            'ooplh_msm':    'W m$^{-2}$',
            'ooplh_fixmsm': 'W m$^{-2}$',
            'ooplh_fixasm': 'W m$^{-2}$',
            'ooplh_orig':   'W m$^{-2}$',
            'ooplh_mmmbc':  'W m$^{-2}$',
            'ooplh_mmmsm':  'W m$^{-2}$',
            'ooplh_fixbc':  'W m$^{-2}$',
            'ooplh_fixbc10': 'W m$^{-2}$',
            'ooplh_fixbc100':'W m$^{-2}$',
            'ooplh_fixbc200':'W m$^{-2}$',
            'ooplh_fixbc300':'W m$^{-2}$',
            'ooplh_rbcsm':  'W m$^{-2}$',
            'ooplh_rddsm':  'W m$^{-2}$',
            'ooplh_dbc':    'W m$^{-2}$',
            'ooplh_mtr':    'W m$^{-2}$',
            'oopef_msm':    'unitless',
            'oopef_fixmsm': 'unitless',
            'oopef_fixasm': 'unitless',
            'oopef_orig':   'unitless',
            'oopef_mmmbc':  'unitless',
            'oopef_mmmsm':  'unitless',
            'oopef_fixbc':  'unitless',
            'oopef_rbcsm':  'unitless',
            'oopef_rddsm':  'unitless',
            'oopef_dbc':    'unitless',
            'oopef_mtr':    'unitless',
            'rfa':          'W m$^{-2}$',
            'pblh':         'm',
            'wap850':       'hPa d$^{-1}$',
            'wapt850':      'K hPa d$^{-1}$',
            'fa850':        'W kg$^{-1}$',
            'fat850':       'W kg$^{-1}$',
            'advt850_wm2':  'W m$^{-2}$',
            'advt850':      'W kg$^{-1}$',
            'advtx850':     'W kg$^{-1}$',
            'advty850':     'W kg$^{-1}$',
            'advm850':      'W kg$^{-1}$',
            'advmx850':     'W kg$^{-1}$',
            'advmy850':     'W kg$^{-1}$',
            }
    return lbs[vn]

def filllongap(din,lon,axis):
    # repeat 0 deg lon info to 360 deg to prevent a blank line in contour
    lon=np.append(lon.data,360)
    dout=np.append(din,din[...,0][...,None],axis=axis)
    return dout,lon

