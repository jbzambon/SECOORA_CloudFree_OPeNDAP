# Program to plot DINEOF and Original MODIS SST and Chlor-a for SECOORA
#
# Joseph B. Zambon
# jbzambon@ncsu.edu
# 23 May 2018
#
# Using conda, create environment, activate, and run code
# conda env create -f secoora_cloudfree.yml 
# source activate secoora_cloudfree
# jupyter notebook  OR
# python secoora_cloudfree.py

#Dependencies
from pydap.client import open_url
import numpy as np
import datetime
import cmocean
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LogNorm
import matplotlib.colorbar as cb
import matplotlib.colors as colors
from matplotlib.mlab import bivariate_normal

# Define Date Range
# April 2017 PEACH Cruise
date_start = '2017-04-13'
date_end   = '2017-04-30'

# Define SST colorbar range ºC
sst_range = [16,30]

# OPeNDAP linked datasets
modis_sst_url = 'http://oceanus.meas.ncsu.edu:8080/thredds/dodsC/secoora/modis/sst.nc'
modis_chl_url = 'http://oceanus.meas.ncsu.edu:8080/thredds/dodsC/secoora/modis/chla.nc'
dineof_sst_url = 'http://oceanus.meas.ncsu.edu:8080/thredds/dodsC/secoora/dineof/sst.nc'
dineof_chl_url = 'http://oceanus.meas.ncsu.edu:8080/thredds/dodsC/secoora/dineof/chla.nc'
modis_sst_dataset = open_url(modis_sst_url)
modis_chl_dataset = open_url(modis_chl_url)
dineof_sst_dataset = open_url(dineof_sst_url)
dineof_chl_dataset = open_url(dineof_chl_url)

date_start = datetime.datetime.strptime(date_start,"%Y-%m-%d")
date_end   = datetime.datetime.strptime(date_end,"%Y-%m-%d")
num_days = date_end - date_start

# For inline plotting in Jupyter Notebook
#get_ipython().run_line_magic('pylab', 'inline')

parallels = np.arange(0.,90,5.)
meridians = np.arange(180.,360.,5.)

# For inline plotting in Jupyter Notebook
#figsize(22,20)
# For script-based plotting
fig=plt.figure(frameon=False,figsize=(22,20))

for t in range(0,num_days.days+1):
    #Assume date ranges are congruent among datasets, just use modis_sst
    time=np.array(modis_sst_dataset['time'])
    t_ind = np.where(time==datetime.datetime.strftime((date_start + datetime.timedelta(t)),"%Y-%m-%d"+"T00:00:00Z"))
    t_ind = t_ind[0]
    curr_date = date_start + datetime.timedelta(t)
    # Assume coordinates are congruent among datasets, just use modis_sst
    lat = modis_sst_dataset['lat'][:]
    lon = modis_sst_dataset['lon'][:]
    # OPeNDAP linked datasets
    raw_sst = modis_sst_dataset['sst']
    raw_sst = raw_sst['sst'][int(t_ind),:,:]
    raw_sst = np.squeeze(raw_sst)
    raw_sst = np.ma.filled(raw_sst.astype(float), np.nan)
    raw_sst[raw_sst<-5]=np.nan; raw_sst= np.ma.array(raw_sst,mask=np.isnan(raw_sst))
    # Raw Chlor-a
    # OPeNDAP linked datasets
    raw_chla = modis_chl_dataset['chlor_a']
    raw_chla = raw_chla['chlor_a'][int(t_ind),:,:]
    raw_chla = np.squeeze(raw_chla)
    raw_chla = np.ma.filled(raw_chla.astype(float), np.nan)
    raw_chla[raw_chla<0]=np.nan; raw_chla= np.ma.array(raw_chla,mask=np.isnan(raw_chla))
    # DINEOF SST
    # OPeNDAP linked datasets
    dineof_sst = dineof_sst_dataset['sst']
    dineof_sst = dineof_sst['sst'][int(t_ind),:,:]
    dineof_sst = np.squeeze(dineof_sst)
    dineof_sst = np.ma.filled(dineof_sst.astype(float), np.nan)
    dineof_sst[dineof_sst<-5]=np.nan; dineof_sst= np.ma.array(dineof_sst,mask=np.isnan(dineof_sst))
    # Raw SST
    # OPeNDAP linked datasets
    dineof_chla = dineof_chl_dataset['chlor_a']
    dineof_chla = dineof_chla['chlor_a'][int(t_ind),:,:]
    dineof_chla = np.squeeze(dineof_chla)
    dineof_chla = np.ma.filled(dineof_chla.astype(float), np.nan)
    dineof_chla[dineof_chla<0]=np.nan; dineof_chla= np.ma.array(dineof_chla,mask=np.isnan(dineof_chla))
    plt.clf()
    plt.suptitle('4km Observed and Cloud Free: ' + curr_date.strftime("%d %b %Y %H"+"UTC"),fontsize=36,family='Helvetica')
    # Raw SST
    plt.subplot(2,2,1)
    map = Basemap(projection='merc',
      resolution='l',lat_0=((np.max(lat)-np.min(lat))/2),
      lon_0=((np.max(lon)-np.min(lon))/2),
      llcrnrlon=np.min(lon),llcrnrlat=np.min(lat),
      urcrnrlon=np.max(lon),urcrnrlat=np.max(lat))
    map.drawcoastlines()
    map.drawcountries()
    map.drawstates()
    [X,Y] = np.meshgrid(lon,lat)
    map.pcolormesh(X,Y,raw_sst[:,:],cmap=cmocean.cm.thermal,                   vmin=sst_range[0],vmax=sst_range[1],latlon='true')
    map.drawparallels(parallels,labels=[1,0,0,0],fontsize=18)
    map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=18)
    plt.title(('Original SST ($^\circ$C)'),fontsize=24,family='Helvetica')
    cbar=map.colorbar(location='right',ticks=np.arange(sst_range[0],sst_range[1]+0.01,2))
    cbar.ax.tick_params(labelsize=20)
    # DINEOF SST
    plt.subplot(2,2,2)
    map = Basemap(projection='merc',
      resolution='l',lat_0=((np.max(lat)-np.min(lat))/2),
      lon_0=((np.max(lon)-np.min(lon))/2),
      llcrnrlon=np.min(lon),llcrnrlat=np.min(lat),
      urcrnrlon=np.max(lon),urcrnrlat=np.max(lat))
    map.drawcoastlines()
    map.drawcountries()
    map.drawstates()
    map.pcolormesh(X,Y,dineof_sst[:,:],cmap=cmocean.cm.thermal,                   vmin=sst_range[0],vmax=sst_range[1],latlon='true')
    map.drawparallels(parallels,labels=[1,0,0,0],fontsize=18)
    map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=18)
    plt.title(('Cloud Free SST ($^\circ$C)'),fontsize=24,family='Helvetica')
    cbar=map.colorbar(location='right',ticks=np.arange(sst_range[0],sst_range[1]+0.01,2))
    cbar.ax.tick_params(labelsize=20)
    # Raw Chlorophyll-a
    plt.subplot(2,2,3)
    map = Basemap(projection='merc',
      resolution='l',lat_0=((np.max(lat)-np.min(lat))/2),
      lon_0=((np.max(lon)-np.min(lon))/2),
      llcrnrlon=np.min(lon),llcrnrlat=np.min(lat),
      urcrnrlon=np.max(lon),urcrnrlat=np.max(lat))
    map.drawcoastlines()
    map.drawcountries()
    map.drawstates()
    map.pcolormesh(X,Y,raw_chla[:,:],norm=LogNorm(vmin=0.01, vmax=100),                    cmap=cmocean.cm.algae,latlon='true')
    map.drawparallels(parallels,labels=[1,0,0,0],fontsize=18)
    map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=18)
    plt.title(('Original Chl-a (mg/m$^3$)'),fontsize=24,family='Helvetica')
    cbar=map.colorbar(location='right',norm=LogNorm(vmin=0.01, vmax=100),                      ticks=[0.01,0.1,1,10,100])
    cbar.ax.tick_params(labelsize=20)
    # DINEOF Chlorophyll-a
    plt.subplot(2,2,4)
    #ax = fig.add_subplot(2,2,4)
    map = Basemap(projection='merc',
      resolution='l',lat_0=((np.max(lat)-np.min(lat))/2),
      lon_0=((np.max(lon)-np.min(lon))/2),
      llcrnrlon=np.min(lon),llcrnrlat=np.min(lat),
      urcrnrlon=np.max(lon),urcrnrlat=np.max(lat))
    map.drawcoastlines()
    map.drawcountries()
    map.drawstates()
    map.pcolormesh(X,Y,dineof_chla[:,:],norm=LogNorm(vmin=0.01, vmax=100),                    cmap=cmocean.cm.algae,latlon='true')
    map.drawparallels(parallels,labels=[1,0,0,0],fontsize=18)
    map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=18)
    plt.title(('Cloud Free Chl-a (mg/m$^3$)'),fontsize=24,family='Helvetica')
    cbar=map.colorbar(location='right',norm=LogNorm(vmin=0.01, vmax=100),                      ticks=[0.01,0.1,1,10,100])
    cbar.ax.tick_params(labelsize=20)

    plt.savefig('secoora_' + curr_date.strftime("%Y%m%d") + '.png')


