import os
import math
import string
import numpy as np
import sys
sys.path.append('../src')
import util
import xarray as xr
import pandas as pd

#######################################################
# USER SPECIFIC SECTION
#======================================================
modelpath = "/glade/u/home/manab/fcast/summa/"
controlFileName = "summa.txt"
appInputFiles = [ os.path.join(modelpath, 'HHDW1/summa_zLocalParamInfo_retro.txt')]
appInputTmplts = ["summa_zLocalParamInfo_template.txt"]

#######################################################
# FUNCTION: GENERATE MODEL INPUT FILE
#======================================================
def genAppInputFile(inputData, appTmpltFiles, appInputFiles, nInputs, inputNames):
    nfiles = len(appInputFiles)
    for i in range(nfiles):
        infile = open(appTmpltFiles[i], "r")
        outfile = open(appInputFiles[i], "w")
        while 1:
            lineIn  = infile.readline()
            if lineIn == "":
                break
            lineLen = len(lineIn)
            newLine = lineIn
            if nInputs > 0:
                for fInd in range(nInputs):
                    strLen = len(inputNames[fInd])
                    while 1:
                        sInd = newLine.find(inputNames[fInd])
                        if sInd < 0:
                            break
                        #sdata = '%7.7f' % inputData[fInd]
                        sdata = '%12.2e' % inputData[fInd]
                        strdata = str(sdata)
                        ntidx = sInd + strLen
                        lineTemp = newLine[0:sInd] + strdata +  " " + newLine[ntidx:lineLen+1]
                        newLine = lineTemp
                        lineLen = len(newLine)
            outfile.write(newLine)
        infile.close()
        outfile.close()
    return

def allindices(str1, str2, listindex = [], offset=0):
    """
    return all indeces of str2 found in str1
    """
    i = str1.find(str2, offset)
    while i >= 0:
        listindex.append(i)
        i = str1.find(str2, i + len(str2))
    return listindex

#######################################################
# FUNCTION: RUN MODEL
#====================================================== 
def runApplication():
    cwd = os.getcwd()
    os.chdir(modelpath) 
    os.system("csh run_HHDW1_summa_parallel_retro.csh; wait")
    print('Debug - Ran SUMMA in parallel')
    os.system("python /glade/u/home/manab/fcast/summa/hhdw1_concat.py; wait")
    print('Debug - Ran concatenation')
    os.system("csh run_HHDW1_routing_retro.csh; wait")
    print('Debug - Ran routing')
    os.chdir(cwd)
    return

#######################################################
# FUNCTION: CALCULATE DESIRE OUTPUT
#======================================================
def getOutput():
    ## compute RMSE from 1970-01-01 to 2007-12-31
    #Qsim = np.loadtxt(modelpath + "sample_model/output/wbvars.txt.HHWM8", skiprows=1)[0:13878,18]
    #Qobs = np.loadtxt(modelpath + "sample_model/input/misc/HHWM8.NRNI.dly.mmd.txt", skiprows=1)[15159:29037,3]
    # compute RMSE from 1980-01-01 to 2000-12-31
    #Qsim = np.loadtxt(modelpath + "sample_model/output/wbvars.txt.HHWM8", skiprows=1)[3652:11322,18]
    #Qobs = np.loadtxt(modelpath + "sample_model/input/misc/HHWM8.NRNI.dly.mmd.txt", skiprows=1)[18811:26481,3]

    Qsimdat = xr.open_dataset('/glade2/work/manab/output/asmo_route/routeout.nc')
    #Qsim = Qsimdat.set_index(sSeg = 'reachID').sel(sSeg = 17003601)['IRFroutedRunoff'].values   #Gives all #3H values
    #Qsim = Qsimdat.set_index(sSeg = 'reachID').sel(sSeg = 17003601)['IRFroutedRunoff'].groupby('time.day').last().values # T21 values daily
    Qsim = Qsimdat.set_index(sSeg = 'reachID').sel(sSeg = 17003601)['IRFroutedRunoff'].resample('D',how= 'mean', dim='time') #Daily mean
    stime = str(pd.to_datetime(Qsimdat['time'].min().values).date())  #Find start and end time of SUMMA/Route simulation
    etime = str(pd.to_datetime(Qsimdat['time'].max().values).date())
    Qobs = xr.open_dataset('/glade/p/work/manab/fcast/newsumma/summa/HHDW1/obs/obsflow.dly.HHDW1.nc', engine='scipy')['flow'].loc[stime:etime].values

    metric = 'KGE'   #RMSE/KGE - Choose here

    if metric == 'KGE':
        # Kling-Gupta efficiency
        print("Calculating KGE")
        cc = np.corrcoef(Qsim,Qobs)[0,1]
        alpha = (np.std(Qsim)/np.std(Qobs)).values
        beta =  (np.sum(Qsim)/np.sum(Qobs)).values
        metriccal = np.sqrt((cc-1)**2 + (alpha-1)**2 + (beta-1)**2)   
    elif metric == 'RMSE':
        # RMSE
        print("Calculating RMSE")
        metriccal = np.sqrt(((Qsim - Qobs) ** 2).mean()).values
    else:
        raise Exception("Metric not selected correctly")

    print(metriccal)
    return metriccal
#######################################################
# MAIN PROGRAM
#======================================================
def evaluate(x):   #Here x is one set of input parameters that comes from ASMO.optimization routine
    print(x)
    pf = util.read_param_file(controlFileName)   #Reads the file summa.txt
    #for n in range(pf['num_vars']):  #Not needed because of hardcored UQ name
    #    pf['names'][n] = 'UQ_' + pf['names'][n]  #Creates pf with upper and lower bound parameter values
    genAppInputFile(x, appInputTmplts, appInputFiles, pf['num_vars'], pf['names'])
    runApplication()
    print('Stops after runApplication()')
    output = getOutput()
    print('Stops after getOutput')
    return output
