import numpy as np
import os
import matplotlib.pyplot as plt
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import pandas as pd
from rpy2.robjects import pandas2ri

PATH = "C:/Users/user/Desktop/R&S_coPaper/Simulation/"
PATH_HOLTWINTERS = "C:/Users/user/Desktop/R&S_coPaper/HoltWinters3H/"
PATH_ARIMA = "C:/Users/user/Desktop/R&S_coPaper/Arima3H/"
PATH_FILTERING = "C:/Users/user/Desktop/R&S_coPaper/Filtering/"
PATH_SHORT_HOLTWINTERS = "C:/Users/user/Desktop/R&S_coPaper/SHORT_HoltWinters3H/"
PATH_SHORT_ARIMA = "C:/Users/user/Desktop/R&S_coPaper/SHORT_Arima3H/"

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
        input <- ts(input,frequency=4)
        
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
        input <- ts(input, frequency=4)
        
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
    df = pd.DataFrame()

    for root, dirs, files in os.walk(path):
        rootpath = os.path.join(os.path.abspath(path), root)
        df[rootpath] = files

    return df

def makeDir(dirName):
    if not os.path.isdir(dirName):
        os.mkdir(dirName)

def init():
    makeDir(PATH_HOLTWINTERS)
    makeDir(PATH_ARIMA)
    makeDir(PATH_SHORT_HOLTWINTERS)
    makeDir(PATH_SHORT_ARIMA)

def write_HW_Result(fList):
        for dir in fList.columns[1: ]:
            dirName = dir.split('/')[-1]
            outDir = os.path.join(PATH_HOLTWINTERS, dirName)
            makeDir(outDir)

            for file in fList[dir]:
                readPath = os.path.join(dir, file)
                data = read_SimData(readPath)

                for i in range(1, len(data.index) + 1):
                    outFileName = outDir + '/' + file.split('.')[0] + "_pred_" + str(i) + ".txt"
                    init = data.index[0:i].values
                    estimation = forecast(init, PRED_HOLTW)
                    np.savetxt(outFileName, estimation, fmt='%d', delimiter=",\t",
                               header="mean,lower80,lower95,upper80,upper95")

def write_ARIMA_Result(fList):
        for dir in fList.columns[1: ]:
            dirName = dir.split('/')[-1]
            outDir = os.path.join(PATH_ARIMA, dirName)
            makeDir(outDir)

            for file in fList[dir]:
                readPath = os.path.join(dir, file)
                data = read_SimData(readPath)

                for i in range(1, len(data.index) + 1):
                    outFileName = outDir + '/' + file.split('.')[0] + "_pred_" + str(i) + ".txt"
                    init = data.index[0:i].values
                    estimation = forecast(init, PRED_ARIMA)
                    np.savetxt(outFileName, estimation, fmt='%d', delimiter=",\t",
                               header="mean,lower80,lower95,upper80,upper95")

def write_HW_MinInput_Result(fList):
        for dir in fList.columns[1: ]:
            dirName = dir.split('/')[-1]
            outDir = os.path.join(PATH_SHORT_HOLTWINTERS, dirName)
            makeDir(outDir)

            for file in fList[dir]:
                readPath = os.path.join(dir, file)
                data = read_SimData(readPath)

                for i in range(0, len(data.index)-7):
                    outFileName = outDir + '/' + file.split('.')[0] + "_pred_" + str(i+8) + ".txt"
                    init = data.index[i: i+8].values
                    estimation = forecast(init, PRED_HOLTW)
                    np.savetxt(outFileName, estimation, fmt='%d', delimiter=",\t",
                               header="mean,lower80,lower95,upper80,upper95")


def write_Arima_MinInput_Result(fList):
    for dir in fList.columns[1:]:
        dirName = dir.split('/')[-1]
        outDir = os.path.join(PATH_SHORT_ARIMA, dirName)
        makeDir(outDir)

        for file in fList[dir]:
            readPath = os.path.join(dir, file)
            data = read_SimData(readPath)

            for i in range(0, len(data.index) - 7):
                outFileName = outDir + '/' + file.split('.')[0] + "_pred_" + str(i+8) + ".txt"
                init = data.index[i: i+8].values
                estimation = forecast(init, PRED_ARIMA)
                np.savetxt(outFileName, estimation, fmt='%d', delimiter=",\t",
                           header="mean,lower80,lower95,upper80,upper95")
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""" M A I N code is in here """
init()
pandas2ri.activate()
fList = allFiles(PATH)
print("HW MININPUT")
write_HW_MinInput_Result(fList)
print("ARIMA MININPUT")
write_Arima_MinInput_Result(fList)
print("HOLTWINTERS")
write_HW_Result(fList)
print("ARIMA")
write_ARIMA_Result(fList)

""""""""""""""""""""""""""""""