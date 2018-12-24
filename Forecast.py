import numpy as np
import os
import matplotlib.pyplot as plt
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import pandas as pd
from rpy2.robjects import pandas2ri

PATH = "./inputData"
PATH_HOLTWINTERS = "./HoltWinters3H/"
PATH_ARIMA = "./Arima3H/"
PATH_FILTERING = "./Filtering/"
""" install & import R packages  """
try:
    utils = importr('utils')
    forecast = importr('forecast')
except:
    utils.install_packages('forecast', repos='http://cran.us.r-project.org')
    forecast = importr('forecast')
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" R Code for forecast h=1 means 15Minutes ( 3Hour ==12 ) """
PRED_ARIMA = """
    function(input){
    
        library(forecast)
        input <- as.numeric(input)
        input <- ts(input,frequency=37)
        
        tryCatch(
        {
            arima <- auto.arima(input)
            pred_arima <- forecast(arima, h=12)
            outdf<-data.frame(pred_arima$mean, pred_arima$lower, pred_arima$upper)
            colnames(outdf)<-c('forecast', 'lower80', 'lower95', 'upper80', 'upper95')
            round(outdf,0)
        },
        error = function(e) return(0),
        finally = NULL
        )
        
    }
"""
PRED_HOLTW = """
    function(input){
        
        library(forecast)
        input <- as.numeric(input)
        input <- ts(input, frequency=12)
        
        tryCatch(
        {
            holts <- HoltWinters(input)
            pred_holts <- forecast(holts, h=12)
            outdf<-data.frame(pred_holts$mean, pred_holts$lower, pred_holts$upper)
            colnames(outdf)<-c('forecast', 'lower80', 'lower95', 'upper80', 'upper95')
            round(outdf,0)
        },
        error = function(e) return(0),
        finally = NULL
        )
        
    }
"""
"""Function"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def read_SimData(filePath):
    rdata = pd.read_csv(filePath, header=None, index_col=0)
    a = 0
    for i in rdata.index.values:
        rdata.index.values[a] = i
        a = a+1
    return rdata


def draw_Plot(data):
    plt.plot(data)
    plt.show()

def forecast(data, select):
    rFuncForecast = robjects.r(select)
    rForecast = rFuncForecast(data)
    forecastDF=pandas2ri.ri2py(rForecast)
    return forecastDF

def allFiles(path):
    files = os.listdir(path)
    for i in range(0, len(files)):
        files[i] = PATH + '/' + files[i]
    return files

def makeDir(dirName):
    if not os.path.isdir(dirName):
        os.mkdir(dirName)

def init():
    makeDir(PATH_HOLTWINTERS)
    makeDir(PATH_ARIMA)

def write_HW_Result(fList):
        for dir in fList:
            dirName = dir.split('/')[-1]
            outDir = os.path.join(PATH_HOLTWINTERS, dirName)
            data = read_SimData(dir)
            print(len(data.index))
            for i in range(9251, len(data.index) + 1):
                outFileName = outDir + "_in_" + str(i) + ".txt"
                init = data.index[0:i].values
                print(init)
                estimation = forecast(init, PRED_HOLTW)
                np.savetxt(outFileName, estimation, fmt='%d', delimiter=",\t",
                            header="mean,lower80,lower95,upper80,upper95")

def write_ARIMA_Result(fList):
        for dir in fList:
            dirName = dir.split('/')[-1]
            outDir = os.path.join(PATH_ARIMA, dirName)
            data = read_SimData(dir)

            for i in range(9251, len(data.index) + 1):
                outFileName = outDir + "_in_" + str(i) + ".txt"
                init = data.index[0:i].values
                print(init)
                estimation = forecast(init, PRED_ARIMA)
                np.savetxt(outFileName, estimation, fmt='%d', delimiter=",\t",
                            header="mean,lower80,lower95,upper80,upper95")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" M A I N code is in here """
init()
pandas2ri.activate()
fList = allFiles(PATH)

#print("HOLTWINTERS")
#write_HW_Result(fList)
print("ARIMA")
write_ARIMA_Result(fList)

""""""""""""""""""""""""""""""