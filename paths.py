def countryfilepaths(country,lev):
    rootpath='/project/amp/miyawaki/data/share/shapefiles/countries'
    filepaths={
            'antarctica':   'gadm41_ATA',
            'argentina':    'gadm41_ARG',
            'bolivia':      'gadm41_BOL',
            'botswana':     'gadm41_BWA',
            'brazil':       'gadm41_BRA',
            'cambodia':     'gadm41_KHM',
            'chile':        'gadm41_CHL',
            'colombia':     'gadm41_COL',
            'ecuador':      'gadm41_ECU',
            'greenland':    'gadm41_GRL',
            'guyana':       'gadm41_GUY',
            'guyane':       'gadm41_GUF',
            'laos':         'gadm41_LAO',
            'paraguay':     'gadm41_PRY',
            'peru':         'gadm41_PER',
            'suriname':     'gadm41_SUR',
            'uruguay':      'gadm41_URY',
            'usa':          'gadm41_USA',
            'venezuela':    'gadm41_VEN',
            'vietnam':      'gadm36_VNM',
            'zambia':       'gadm41_ZMB',
            'zimbabwe':     'gadm41_ZWE'
            }
    return '%s/%s/%s_%g.shp'%(rootpath,country,filepaths[country],lev)

def contfilepaths(cont):
    rootpath='/project/amp/miyawaki/data/share/shapefiles/continents'
    filepath='%s.shp'%(cont)
    return '%s/%s'%(rootpath,filepath)

def basinfilepaths(basin,lev):
    rootpath='/project/amp/miyawaki/data/share/shapefiles/basins'
    filepath='hybas_%s_lev0%g_v1c.shp'%(basin,lev)
    return '%s/%s/%s'%(rootpath,basin,filepath)

def usafilepath():
    return '/project/cas/islas/shapefiles/usa/gadm36_USA_1.shp'
