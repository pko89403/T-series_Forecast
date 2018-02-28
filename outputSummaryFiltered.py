import os
PATH='E:/python_workspace/T-series_Forecast/Filtering/'
OUTPATH='E:/python_workspace/T-series_Forecast/'
files = os.listdir(PATH)
print(files)

outArima=OUTPATH+'Filter.txt'

arima = []
for i in range(0,len(files)):
    fName= PATH + '2017110205.txt_in_' + str(i+1) + '.txt'
    file = open(fName, 'r')
    for j in range(0,4):
        line = file.readline()
    arima.append(line)
    file.close()

out = open(outArima, 'w')
for val in arima:
    out.write(val)
out.close()