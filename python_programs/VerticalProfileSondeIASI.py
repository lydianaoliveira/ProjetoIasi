# Python program for PIRATA data

# import
from DataSelectionSondeIASI import *  #import variables from the file
import matplotlib.pyplot as plt
import numpy as np

year = str(iasi_datef.year)

#----- IASI variables
iasi_p = nc['pressure_levels_temp'][:]
iasi_p = iasi_p * 0.01  #using scale factor

if year in ['2017','2018']:
    iasi_t = nc['fg_atmospheric_temperature'][:]
    iasi_wv = nc['fg_atmospheric_water_vapor'][:]
else:
    iasi_t = nc['atmospheric_temperature'][:]
    iasi_wv = nc['atmospheric_water_vapor'][:]

# temperature and water vapor at the closest point
i = int(i)
j = int(j)
#i = 140
#j = 57
iasi_t = iasi_t[i,j,:]
iasi_wv = iasi_wv[i,j,:]

#----- sonde variables
sonde_p = sonde_data['P']
sonde_t = sonde_data['T']

if year not in ['2014','2017','2018']:
    sonde_t = sonde_t + 273.15  #convert C to K
    sonde_wv = sonde_data['RH']
else:
    sonde_wv = sonde_data['MR']  #mixing ratio variable
    sonde_wv = sonde_wv/1000  #convert g/kg to kg/kg

#----- selecting pressure levels

# function to find the nearest value
def FindNearest(array,value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

# setting the range of pressure levels
maxP = int(np.nanmax(sonde_p))
minP = int(np.nanmin(sonde_p))
lst = list(range(maxP, minP+1, -50))  #range backwards because sonde pressure is invert

# Sonde levels
sonde_p_levels = []
for a in lst:
    value = FindNearest(sonde_p, a)
    sonde_p_levels.append(value)

sonde_idx = []
sonde_duplicates = []
for b in range(len(sonde_p)):
    if sonde_p[b] in sonde_p_levels:
        sonde_idx.append(b)
        sonde_duplicates.append(sonde_p[b])

# treating duplicate numbers
idx_duplicates = []
if len(sonde_duplicates) != len(set(sonde_duplicates)):  #set() returns a sequence with only distinct elements
    #n = list(range(len(sonde_duplicates)))
    #print(n)
    for b in range(len(sonde_duplicates)):
        num = sonde_duplicates[b]
        if sonde_duplicates.count(num) > 1:
            idx_duplicates.append(b)

    idx_duplicates.pop()
    for b in idx_duplicates[::-1]:
        sonde_idx.remove(sonde_idx[b])

sonde_t_levels = []
sonde_wv_levels = []
for c in sonde_idx:
    sonde_t_levels.append(sonde_t[c])
    sonde_wv_levels.append(sonde_wv[c])

# IASI levels
iasi_p_levels = []
for x in sonde_p_levels[::-1]:  #go through a list in reverse order
    value = FindNearest(iasi_p, x)
    iasi_p_levels.append(value)

iasi_p_levels_copy = []
for k in iasi_p_levels:
    k = round(k,1)
    iasi_p_levels_copy.append(k)

iasi_idx = []
for y in range(len(iasi_p)):
    if iasi_p[y] in iasi_p_levels:
        iasi_idx.append(y)


iasi_t_levels = []
iasi_wv_levels = []
for z in iasi_idx:
    iasi_t_levels.append(iasi_t[z])
    iasi_wv_levels.append(iasi_wv[z])


#----- plot vertical profile
day = str(iasi_datef.day) +'/'+ str(iasi_datef.month) +'/'+ str(iasi_datef.year)

# temperature profile
plt.plot(iasi_t_levels, iasi_p_levels_copy, color='r', label='IASI')
plt.plot(sonde_t_levels, sonde_p_levels, color='g', label='Sonde')
#plt.ylim([10, np.nanmax(iasi_p_levels)])
plt.gca().invert_yaxis()
plt.xlabel('Temperature (K)')
plt.ylabel('Pressure (hPa)')
plt.title('Temperature Vertical Profile \n MetOp/IASI and PIRATA Radiosonde %s' %(iasi_datef))
plt.legend()
#plt.savefig(dataset_dir / 'temperature_profile_2018110412', dpi=400)
#plt.show()


# water vapour profile
plt.plot(iasi_wv_levels, iasi_p_levels_copy, color='r', label='IASI')
plt.plot(sonde_wv_levels, sonde_p_levels, color='g', label='Sonde')
#plt.ylim([10, np.nanmax(iasi_p_levels)])
plt.gca().invert_yaxis()
#plt.xlim([0, 100])
plt.xlabel('Water Vapor (kg/kg)')
plt.ylabel('Pressure (hPa)')
plt.title('Water Vapor Vertical Profile \n MetOp/IASI and PIRATA Radiosonde %s' %(iasi_datef))
plt.legend()
#plt.savefig(dataset_dir / 'watervapor_profile_2018110412', dpi=400)
#plt.show()

#----- radiosonde location

# treating missing values
sonde_lat = sonde_data['Lat'].tolist()  #convert array column to list
if -32768 in sonde_lat:
    sonde_lat.remove(-32768)
sonde_lon = sonde_data['Lon'].tolist()
if -32768 in sonde_lon:
    sonde_lon.remove(-32768)

# plot lat/lon
fig, ax = plt.subplots(figsize=(10,6))
plt.scatter(sonde_lat, sonde_lon)
plt.xlim([np.nanmin(sonde_lat)-0.05, np.nanmax(sonde_lat)+0.05])
plt.ylim([np.nanmin(sonde_lon)-0.05, np.nanmax(sonde_lon)+0.05])
plt.title('PIRATA Radiosonde Lat/Lon %s' %(sonde_datei))
#plt.savefig('radiosondeLatLon_20181104', dpi=400)
#plt.show()

# sonde displacement
minlat = np.nanmin(sonde_lat); maxlat = np.nanmax(sonde_lat)
mov_ay = (maxlat - minlat) * 111.11
print('Deslocamento latitude: %.2f km' %(mov_ay))
print('Lat max = %.2f; Lat min = %.2f \n' %(maxlat, minlat))

minlon = np.nanmin(sonde_lon); maxlon = np.nanmax(sonde_lon)
mov_ax = (maxlon - minlon) * 111.11
print('Deslocamento longitude: %.2f km' %(mov_ax))
print('Lon max = %.2f; Lon min = %.2f' %(maxlon, minlon))
print(40*'-')


