#----------------------------------------------------------##
#        Name: TIFX04-22-82, DataProcessing LEMA
#      Author: GOTTFRID OLSSON 
#     Created: 2022-04-22, 13:55
#     Updated: 2022-04-23, 14:10
#       About: Takes in CSV-data från Qualisys measurement
#              and applies gaussian filter and excecutes a
#              numerical derivative to get velocity
#              Saves processed data to another CSV-file
##---------------------------------------------------------##

# COMMENTS/NOTES:
#   make functions to do the smoothing and removinf of zeroes ?
#
#

import pandas as pd                     # for CSV
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


## CSV_handler ##
CSV_DELIMITER = ','

def read_CSV(readFilePath):
    #print("In progress: Reading CSV" + CSV_filePath)
    CSV =  pd.read_csv(readFilePath, sep=CSV_DELIMITER)
    print("DONE: Reading CSV: " + readFilePath)
    return CSV

def get_CSV_header(CSV_data):
    return CSV_data.columns.values



## MAIN ##

filename_rawCSV = 'IckeOptimeradeTriggers_300V_20220422_1150'
readFilePath_rawCSV = "RAW CSV/"+str(filename_rawCSV) + ".csv"
rawData = read_CSV(readFilePath_rawCSV)
header = get_CSV_header(rawData)

rawX = rawData[header[2]]
time = rawData[header[1]]

#print(rawX, time)


rawX_noZeroes = []
time_noZeroes = []

for i in range(len(rawX)): # remove all position = zeroes from Qualisys, otherwise np.gradient() gets sad
    if rawX[i] != 0:
        rawX_noZeroes.append(rawX[i])
        time_noZeroes.append(time[i])

#print(len(rawX_noZeroes), len(time_noZeroes))

sigma = 5 #3-4 looks pretty good; 5-6 looks very smooth and nice, //2022-04-23
x_filtered = gaussian_filter1d(rawX_noZeroes, sigma)

#plt.plot(time_noZeroes, rawX_noZeroes, 'r+', label="rawX_noZeroes")
#plt.plot(time_noZeroes, x_filtered,    'b.', label="x_filtered with sigma ="+str(sigma))
#plt.legend()
#plt.show()
#scipy.ndimage.gaussian_filter1d(input, sigma, axis=- 1, order=0, output=None, mode='reflect', cval=0.0, truncate=4.0)
#quit()

x = x_filtered
t = time_noZeroes
v = np.gradient(x)/np.gradient(t)
v_unfiltered = np.gradient(rawX_noZeroes)/np.gradient(t)

plt.plot(t, v_unfiltered, label="Velocity (mm/s), unfiltered")
plt.plot(t, v, label="Velocity (mm/s), filtered sigma="+str(sigma))
#plt.plot(t, x, label="position (mm)")
plt.legend()
plt.show()


# export data to file
