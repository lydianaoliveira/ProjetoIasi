
# Plot vertical profile IASI

'''
objetivo: obter perfil vertical em um determinado ponto dos dados
fg_atmospheric_temperature: var tridimensional (lat, lon, pressure_levels_temp)
'''

# bibliotecas
import netCDF4
import numpy as np
import pathlib as plib
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta

#----- dataset directory
current_dir = plib.Path.cwd()  #default directory
dataset_dir = current_dir / '20080330'  #folder with the data

# file read
filename = dataset_dir / 'W_XX-EUMETSAT-Darmstadt,HYPERSPECT+SOUNDING,METOPA+IASI_C_EUMP_20080330112056_7498_eps_o_l2.nc'
nc = netCDF4.Dataset(filename)
#print(nc.variables)

# variables
lat = nc['lat'][:]
#print('lat.shape: ', lat.shape)
#print(lat[382,60])
lon = nc['lon'][:]
#print('lon.shape: ', lon.shape)
#print(lon[382,60])

ptemp = nc['pressure_levels_temp'][:]
ptemp = ptemp * 0.01
#print('p_temp.shape: ', p_temp.shape)
#print(p_temp)
min_ptemp = np.nanmin(ptemp)
max_ptemp = np.nanmax(ptemp)

#temp = nc['fg_atmospheric_temperature'][:]
temp = nc['atmospheric_temperature'][:]
#print('temp.shape: ', temp.shape)
#data = temp[0,0]  #primeiro valor
#print(data.shape)

p_humid = nc['pressure_levels_humidity'][:]
#print(p_humid)
#humid = nc['fg_atmospheric_water_vapor'][:]
humid = nc['atmospheric_water_vapor'][:]
#print(humid)

#----- data da passagem
start_time = nc['record_start_time'][:]
since = datetime.strptime("2000-01-01 0:0:0", '%Y-%m-%d %H:%M:%S')
#print(type(since))

date_i = start_time[382]
date_i = date_i.item()  #convertendo numpy.int32 em int
#print(date_i)
#print(type(date_i))

date = since + timedelta(seconds=date_i)
print(date)


#----- plot perfil vertical
# Escolha do ponto para se extrair os dados da var
profile = temp[300,30,:]

# Convertendo para escala logarítimica
#p_temp = np.log10(p_temp)

# Plot de temperatura vs níveis de pressão
plt.plot(profile, ptemp)
plt.ylim([min_ptemp, max_ptemp])  #ajuste dos limites do eixo y
plt.gca().invert_yaxis()  #inverte eixo y
plt.xlabel('Temperatura (K)')
plt.ylabel('Pressão (hPa)')
plt.title('Perfil Vertical - MetOp/IASI /n 30-11-2018')
plt.show()
