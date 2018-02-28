import os
PATH='E:/python_workspace/T-series_Forecast/HoltWinters3H_110205/'
OUTPATH='E:/python_workspace/T-series_Forecast/'
files = os.listdir(PATH)
print(files)

outArima=OUTPATH+'ARIMA.txt'

arima = []
for i in range(0,len(files)):
    fName= PATH + '2017110205.txt_in_' + str(i+1) + '.txt'
    file = open(fName, 'r')
    header = file.readline()

    for k in range(0,8):
        line = file.readline()

    mean = line.strip().split(',')[0]

    arima.append(mean)
    file.close()

print(arima)
out = open(outArima, 'w')
for val in arima:
    out.write(val+'\n')
out.close()