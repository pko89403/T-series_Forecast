import os
import pandas as pd
import numpy as np
import random
PATH = "C:/Users/user/Desktop/R&S_coPaper/Simulation/"
PATH_HOLTWINTERS = "C:/Users/user/Desktop/R&S_coPaper/HoltWinters3H/"
PATH_ARIMA = "C:/Users/user/Desktop/R&S_coPaper/Arima3H/"
PATH_FILTERING = "C:/Users/user/Desktop/R&S_coPaper/Filtering/"
PATH_SHORT_HOLTWINTERS = "C:/Users/user/Desktop/R&S_coPaper/SHORT_HoltWinters3H/"
PATH_SHORT_ARIMA = "C:/Users/user/Desktop/R&S_coPaper/SHORT_Arima3H/"

est_Type = [PATH_ARIMA, PATH_SHORT_ARIMA, PATH_HOLTWINTERS,PATH_SHORT_HOLTWINTERS]

lower = [[0]*8 for i in range(12)]
upper = [[0]*8 for i in range(12)]

def makeDir(dirName):
    if not os.path.isdir(dirName):
        os.mkdir(dirName)

def getDateList(path):
    date = os.listdir(path)
    return date

def makeFileName(zone, time):
    name = "zone" + str(zone) + "_pred_" + str(time) + ".txt"
    return name

def r4Values(date, file):
    for i in  range(0, len(est_Type) ) :
        read = est_Type[i] + '/' + date + '/' + file
        list = pd.read_csv(read)

        for j in range(0,len(list.values)):
            for k in range(1,3):
                lower[j][2*i + k-1] = list.values[j][k]
            for k in range(3,5):
                upper[j][2*i + k-3] = list.values[j][k]

def lower_tun():
    for i in range(0, 12):
        for j in range(0, 8):
            if( lower[i][j] < 0):
                lower[i][j] = 0

def filtering(lower, upper):
    preSample = []
    sample = []
    reSample = []
    if(np.isnan(lower) == True ): lower = 0
    if(np.isnan(upper) == True ): upper = lower
    for k in range(lower, upper):
        preSample.append(k)
    median = np.median(preSample)
    stdev = np.std(preSample)
    for k in range(0, len(preSample)):
        tmp = (preSample[k] - median)
        tmp = tmp / stdev
        if ( tmp > -1 and tmp < 1):
            sample.append(preSample[k])
    reSampleCnt = len(sample) / 4
    reSampleCnt = round(reSampleCnt)
    if(reSampleCnt < 1):
        reSampleCnt = 1
    if ( len(sample) > 0):
        random.shuffle(sample)
        for k in range(0, reSampleCnt):
            tmp = random.choice(sample)
            reSample.append( tmp )
            if(np.isnan((tmp))):
                reSample.pop()
    else:
        if(np.isnan((median)) == False):
            reSample.append(median)
    return reSample

def getMean(reSample):
    return np.mean(reSample)

def process():

    dateList = getDateList(PATH)

    for d in dateList:
        folder = os.path.join(PATH_FILTERING, d)
        makeDir(folder)

    for date in dateList:
        for zone in range(1,5):
            for time in range(8,37):
                print("date : ", date, "zone : ", zone, "time : ", time)
                fileName = makeFileName(zone, time)

                output = open(os.path.join(PATH_FILTERING, date, fileName), 'w')
                r4Values(date, fileName)
                lower_tun()
                for i in range(0,12):
                    filtered = []
                    for j in range(0,8):
                        tmp = filtering(lower[i][j], upper[i][j])
                        filtered += tmp
                    res = int(round(getMean(filtered)))
                    output.write(str(res) + "\n")
                output.close()


process()

