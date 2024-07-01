# Python program for Fernando de Noronha data

# import
import netCDF4
import numpy as np
import pandas as pd
import pathlib as plib
from datetime import datetime
from datetime import timedelta

#----- dataset directory
current_dir = plib.Path.cwd()  #default directory
dataset_dir = current_dir / 'FN_20210703'  #folder with the data

#----- reading IASI data

# file read
iasi_file = dataset_dir / 'W_XX-EUMETSAT-Darmstadt,HYPERSPECT+SOUNDING,METOPA+IASI_C_EUMP_20210703210257_76308_eps_o_l2.nc'
nc = netCDF4.Dataset(iasi_file)

# variables
iasi_lat = nc['lat'][:]
iasi_lon = nc['lon'][:]

iasi_time = nc['record_start_time'][:]
since = datetime.strptime('2000-01-01 0:0:0', '%Y-%m-%d %H:%M:%S')

#----- reading sonde data

# file read
col = list(range(11))
sonde_filename = dataset_dir / 'FN_202107032100.csv'
sonde_data = pd.read_csv(sonde_filename,usecols=col,header=None,
                   names=["PRES", "HGHT", "TEMP", "DWPT", "RELH", "MIXR", "DRCT", "SKNT", "THTA", "THTE", "THTV"],sep=',')

# variables
sonde_location = [-3.85, -32.41]
sonde_datei = datetime.strptime('03-07-2021 21:00:00', '%d-%m-%Y %H:%M:%S')

#----- spatial limit
print('sonde coordinates: {}, {}'.format(sonde_location[0], sonde_location[1]))

lat = sonde_location[0] * np.ones(iasi_lat.shape)
lon = sonde_location[1] * np.ones(iasi_lon.shape)

# calculating the distance
dist = np.sqrt(np.power((iasi_lat - lat), 2) + np.power((iasi_lon - lon), 2))
dist = dist * 110  #convert dgr to km
print('the shortest distance is: {:.2f} km'.format(np.nanmin(dist)))

i, j = np.asarray(dist == np.nanmin(dist)).nonzero()
print(i,j)
print('Lat/Lon from the nearest point is: {:.2f}, {:.2f} degrees'.format(iasi_lat[i[0], j[0]], iasi_lon[i[0], j[0]]))

# minimum distance limit
limit_spatial = 25.
if (np.nanmin(dist) <= limit_spatial):
    print('The datas are close enough spatially')
else:
    print('The datas are NOT close enough spatially')
print(40*'-')
print('')

#----- time limit
iasi_datei = iasi_time[i]  #index i is the closest point between the data
iasi_datei = iasi_datei.item()  #convert numpy.int32 to int
iasi_datef = since + timedelta(seconds=iasi_datei)

print('radiosonde date: ', sonde_datei)
print('iasi date: ', iasi_datef)

l = datetime.strptime('0:30:0', '%H:%M:%S')
limit_time = timedelta(hours=l.hour, minutes=l.minute, seconds=l.second)  #convert datetime to timedelta

if sonde_datei > iasi_datef:
    ddate = sonde_datei - iasi_datef
    if ddate <= limit_time:
        print('the data is within the time limit, the time difference is:', ddate)
    else:
        print('the time difference is bigger than 30min', ddate)
elif iasi_datef > sonde_datei:
    ddate = iasi_datef - sonde_datei
    if ddate <= limit_time:
        print('the data is within the time limit, the time difference is:', ddate)
    else:
        print('the time difference is bigger than 30min', ddate)
print(40*'-')
