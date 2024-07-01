# Python program for PIRATA data

# import
import netCDF4
import numpy as np
import pandas as pd
import pathlib as plib
from datetime import datetime
from datetime import timedelta

#----- dataset directory
current_dir = plib.Path.cwd()  #default directory
dataset_dir = current_dir / '20181105'  #folder with the data

#----- reading IASI data

# file read
iasi_file = dataset_dir / 'W_XX-EUMETSAT-Darmstadt,HYPERSPECT+SOUNDING,METOPB+IASI_C_EUMP_20181105220554_31827_eps_o_l2.nc'
nc = netCDF4.Dataset(iasi_file)

# variables
iasi_lat = nc['lat'][:]
iasi_lon = nc['lon'][:]

iasi_time = nc['record_start_time'][:]
since = datetime.strptime('2000-01-01 0:0:0', '%Y-%m-%d %H:%M:%S')

#----- reading sonde data

# file read
sonde_filename = dataset_dir / 'PIRATA_2018_20181105_2129.tsv'

# for 2014/2017/2018 data

col = list(range(19))
sonde_data = pd.read_csv(sonde_filename,skiprows=39,usecols=col,header=None,
                   names=["time", "Pscl", "T", "RH", "v", "u", "Height", "P", "TD", "MR", "DD", "FF", "AZ", "Range", "Lon", "Lat", "SpuKey", "UrsKey", "RadarH",],sep='\t')

# variables
sonde_lat = sonde_data['Lat']
sonde_lon = sonde_data['Lon']
sonde_location = [sonde_lat[0], sonde_lon[0]]

sonde_datei = datetime.strptime('05-11-2018 21:29:00', '%d-%m-%Y %H:%M:%S')
sonde_time = sonde_data['time'][-1:]
print(type(sonde_data))
print(type(sonde_time))
sonde_time = int(sonde_time)
print(type(sonde_time))
sonde_datef = sonde_datei + timedelta(seconds=sonde_time)
print('radiosonde rise time: ', sonde_datef - sonde_datei)
print('')

'''

# for 2008/2009/2010/2011 data

col = list(range(10))
sonde_data = pd.read_csv(sonde_filename,skiprows=0,usecols=col,header=None,
                   names=["time_min", "time_sec", "AscRate", "HgtMSL", "P", "T", "RH", "Dewp_degC", "Dewp_deg", "DicSpeed"],sep=',')

# variables
sonde_location = [14.07, -38.00]
sonde_datei = datetime.strptime('29-08-2011 22:53:00', '%d-%m-%Y %H:%M:%S')
'''

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


