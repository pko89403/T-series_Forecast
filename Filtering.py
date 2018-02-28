import os
import pandas as pd
import numpy as np
import random

PATH = "./inputData"
PATH_HOLTWINTERS = "./HoltWinters3H_110205/"
PATH_ARIMA = "./Arima3H_110205/"
PATH_FILTERING = "./Filtering/"
SAMPLING_SIZE=1000
est_Type = [PATH_ARIMA, PATH_HOLTWINTERS]

lower = [[0]*4 for i in range(12)]
upper = [[0]*4 for i in range(12)]

def makeDir(dirName):
    if not os.path.isdir(dirName):
        os.mkdir(dirName)

def getDateList(path):
    date = os.listdir(path)
    return date

def makeFileName(date, time):
    name = date + "_in_" + str(time) + ".txt"
    return name

def r4Values(file):
    for i in  range(0, len(est_Type) ) :
        read = est_Type[i] + '/' + file

        list = pd.read_csv(read)

        for j in range(0,len(list.values)):
            for k in range(1,3):
                if(np.isnan(list.values[j][k]) == True):
                    list.values[j][k] == 0
                lower[j][2*i + k-1] = list.values[j][k]
            for k in range(3,5):
                if(np.isnan(list.values[j][k]) == True):
                    list.values[j][k] == 0
                upper[j][2*i + k-3] = list.values[j][k]


def filtering(lower, upper):
    preSample = []
    sample = []
    reSample = []

    if(np.isnan(lower) == True ): lower = 0
    if(np.isnan(upper) == True ): upper = lower

    if(lower < 0): lower = 0

    if(lower == upper):
        reSample = [lower] * SAMPLING_SIZE
        return reSample

    if( lower > upper):
        for k in range(upper, lower):
            preSample.append(k)
    else:
        for k in range(lower, upper):
            preSample.append(k)

    median = np.median(preSample)
    stdev = np.std(preSample)
    for k in range(0, len(preSample)):
        tmp = (preSample[k] - median) # Mahalanobis distance ( X - mean ) /  stdev
        if( stdev == 0) :   tmp = 0
        else:   tmp = tmp / stdev

        if ( tmp > -1 and tmp < 1 ):
            sample.append(preSample[k])

    if( len(sample) == 0 ): sample.append(median)

    for k in range(0, SAMPLING_SIZE):
        tmp = random.choice(sample)
        reSample.append( tmp )




    return reSample

def getMean(reSample):
    return np.mean(reSample)

def process():
    makeDir(PATH_FILTERING)
    dates = os.listdir(PATH)
    for date in dates:
        for time in range(1,231):
            fileName = makeFileName(date, time)
            oName = os.path.join(PATH_FILTERING, fileName)
            output = open(oName, 'w')
            r4Values(fileName)
            for i in range(0,12):
                filtered = []
                for j in range(0,4):
                    tmp = filtering(lower[i][j], upper[i][j])
                    filtered += tmp

                if(len(filtered) == 0):
                    res = 0
                else:
                    res = int(round(getMean(filtered)))

                output.write(str(res) + "\n")
            output.close()


process()

