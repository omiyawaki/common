def realm(vn):
    d={ 
        'lhflx':    'atm',
        'vq':       'atm',
        'vt':       'atm',
        'vz':       'atm',
        'fsntoa':   'atm',
        'fsns':     'atm',
        'flnt':     'atm',
        'flns':     'atm',
        'ra':       'atm',
        'pblh':     'atm',
        'pblp':     'atm',
        'qsoil':    'lnd',
        'qvege':    'lnd',
        'qvegt':    'lnd',
        'qsum':     'lnd',
        'fsm':      'lnd',
        'fsno':     'lnd',
        }
    return d[vn]

def history(vn):
    d={ 
        'lhflx':    'cam.h1',
        'fsntoa':   'cam.h1',
        'fsns':     'cam.h1',
        'flnt':     'cam.h1',
        'flns':     'cam.h1',
        'ra':       'cam.h1',
        'solin':    'cam.h1',
        'pblh':     'cam.h1',
        'pblp':     'cam.h1',
        'qsoil':    'clm2.h5',
        'qvege':    'clm2.h5',
        'qvegt':    'clm2.h5',
        'qsum':     'clm2.h5',
        'fsm':      'clm2.h5',
        'fsno':     'clm2.h5',
        }
    return d[vn]
