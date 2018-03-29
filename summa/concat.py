#!/glade/u/home/manab/anaconda3/bin/python

import sys
import xarray as xr
import numpy as np
import glob, os
import shutil

if __name__ == "__main__":
    # User supplied information
    indir = '/glade/u/home/manab/fcast/summa/HHDW1/output/asmo'
    outdir = '/glade/u/home/manab/fcast/summa/HHDW1/output/route'
    convertdir = 'convert'
    finalfile = 'summaout.nc'
    
    startGRU = 1                              #Start GRU Index
    endGRU = 11723                            #End GRU Index
    lenGRU = 50                               #Length of every GRU string
    
    # Step 1: Convert all SUMMA output files into HRU-only
    convertdir = os.path.join(indir,convertdir)
    os.makedirs(convertdir, exist_ok=True)   #Create a convert directory
    outfilelist = glob.glob((indir+'/*.nc')) #list of all files

    for x in range(0, len(outfilelist)):
        ncconvert = xr.open_dataset(outfilelist[x])                                  #Import netCDF file

        runoffdata = ncconvert['averageInstantRunoff'].values                     #Extract averageInstantRunoff values
        runoffarray = xr.DataArray(runoffdata, dims=['time','hru'])            #Create an array of averageInstantRunoff with 2 dimensions
        ncconvert = ncconvert.drop('averageInstantRunoff')                           #Drop the original averageInstantRunoff variable
        ncconvert['averageInstantRunoff'] = runoffarray                           #Add the new array to original netCDF
        ncconvert['averageInstantRunoff'].attrs['long_name'] = "instantaneous runoff (instant)"
        ncconvert['averageInstantRunoff'].attrs['units'] = 'm s-1'

        #print('Step 1: Creating '+str(x+1)+ ' HRU-only SUMMA output file out of ' + str(len(outfilelist)))
        ncconvert_outfile = os.path.join(convertdir, os.path.basename(outfilelist[x]))#Create an output filename
        ncconvert.to_netcdf(ncconvert_outfile, 'w')                                  #Write out the final netCDF file


    #Part 3: Conatenate each GRU set in space
    spacefilelist = glob.glob(convertdir+'/*.nc')
    spacefilelist.sort()
    #print('Step 3: Concatenating by HRU space')
    ncconcat_space = xr.open_mfdataset(spacefilelist, concat_dim='hru')
    #ncconcat_space['hruId'] = ncconcat_space['hruId'].isel(time=0, drop=True)  #Dropping extra time dimension from hruId

    finalfilename = os.path.join(outdir, finalfile)
    ncconcat_space.to_netcdf(finalfilename, 'w')
    
    #print('Deleting folder and contents of convert')
    shutil.rmtree(convertdir)

    print('Concatenated all SUMMA output files to be used in MizuRoute')

