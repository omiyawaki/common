# from metpy.units import units

# GAS CONSTANTS (from AMS Glossary)
Rs	= 8.3144621 # [J mol**-1 K**-1]	universal gas constant
Rd	= 287 		# [J K**-1 kg**-1] 	dry gas constant 
Rv	= 461       # [J K**-1 kg**-1] 	vapor gas constant
ep	= Rd/Rv 	# [unitless] 		dry to vapor gas constant ratio

# SPECIFIC HEAT CAPACITY (from AMS Glossary)
cpd	= 1005.7   	# [J K**-1 kg**-1] 	isobaric (constant pressure) specific heat capacity of dry air
cvd	= 719 		# [J K**-1 kg**-1] 	isochoric (constant volume) specific heat capacity of dry air

# LATENT HEAT CONSTANTS (from AMS Glossary)
Lv	= 2.501e6   # [J kg**-1]		latent heat of vaporization
Lf	= 3.337e5	# [J kg**-1]		latent heat of fusion
Ls	= 2.834e6	# [J kg**-1]		latent heat of sublimation

# RADIATION
si  = 5.67e-8   # [W m**-2 K**-4]   Stefan-Boltzmann constant

# PLANETARY CONSTANTS for EARTH (from NASA Earth Fact Sheet)
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
g	= 9.798     # [m s**-2]		    gravitational acceleration
a	= 6371e3    # [m]			    volumetric mean radius of Earth
obl	= 23.44		# [deg]			    orbit obliquity
ecc	= 0.0167	# [unitless]	    orbit eccentricity
ps	= 1014e2	# [Pa]			    surface pressure
rhs	= 1.217		# [kg m**-3]	    surface density
Hs	= 8.5e3		# [m]			    scale height
Ma	= 5.1e18	# [kg]			    mass of atmosphere
Mh	= 1.4e21	# [kg]			    mass of hydrosphere
Tav	= 288		# [K]			    average temperature
mav	= 28.97e-3	# [kg mol**-1]		mean molecular weight
pn2	= 0.7808	# [unitless]		volumetric N2 concentration
po2	= 0.2095	# [unitless]		volumetric O2 concentration
par	= 9340e-6	# [unitless]		volumetric Ar concentration
pco2= 415e-6	# [unitless]		volumetric CO2 concentration
pne	= 18.18e-6	# [unitless]		volumetric Ne concentration
phe	= 5.24e-6	# [unitless]		volumetric He concentration
pch4= 1.7e-6	# [unitless]		volumetric CH4 concentration
pkr	= 1.14e-6	# [unitless]		volumetric Kr concentration
ph2	= 0.55e-6	# [unitless]		volumetric H2 concentration

rhow= 1e3       # [kg m**-3]        density of water
