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

import csv
import pandas as pd                     # for CSV
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


## CSV_handler ##
CSV_DELIMITER = ','

def read_CSV(readFilePath):
    #requires: "import pandas as pd"
    CSV =  pd.read_csv(readFilePath, sep=CSV_DELIMITER)
    print("DONE: Read CSV: " + readFilePath)
    return CSV

def get_CSV_header(CSV_data):
    return CSV_data.columns.values

def write_data_to_CSV(filenamePath, header, data):
    # requires: "import csv"
    with open(filenamePath, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, lineterminator='\n')
        csvwriter.writerow(header)
        csvwriter.writerows(data)
    print("DONE: Write data to CSV-file: "+str(filenamePath))


# ASSEMBLE VECTORS INTO ARRAY FOR WRITE_2_CSV #

def merge_vectors_for_writeCSV(frame, time, x, y, z): #ad hoc, only use this for THIS particular file; ugly but fast coding
    merged_vector = []
    for i in range(len(time)):
        temp_merge = frame[i], time[i], x[i], y[i], z[i]
        merged_vector.append(temp_merge)

    print("DONE: Merged vectors into one array for writeCSV")
    return merged_vector


## DATA PROCESSING ##

def remove_zeroValues(position, time, frame):
    position_noZeroes = []
    time_noZeroes = []
    frame_noZeroes = []

    for i in range(len(position)):
        if position[i] != 0.000:
            position_noZeroes.append(position[i])
            time_noZeroes.append(time[i])
            frame_noZeroes.append(frame[i])
    
    print("DONE: Removed values with '0.000' from position and time and frame vectors")
    return position_noZeroes, time_noZeroes, frame_noZeroes

def gaussianFilter1D(array1D, sigma):
    print("DONE: Filtered data with sigma="+str(sigma))
    return gaussian_filter1d(array1D, sigma)



## MAIN ##

filename_rawCSV = 'IckeOptimeradeTriggers_300V_20220422_1150' #needs to be filled in manually
readFilePath_rawCSV = "RAW CSV/"+str(filename_rawCSV) + ".csv"

filename_processedCSV = filename_rawCSV + "_processed_20220424_1122" #needs to be filled in manually
writeFilePath_processedCSV = "Processed CSV/"+str(filename_processedCSV) + ".csv"

rawData = read_CSV(readFilePath_rawCSV)
header = get_CSV_header(rawData)

frame = rawData[header[0]]
time  = rawData[header[1]]
rawX  = rawData[header[2]]
rawY  = rawData[header[3]]
rawZ  = rawData[header[4]]

showMultipleSigma = False #set to true if you want plot for several values for sigma in gauss filter

[rawX_noZeroes, time_noZeroes, frame_noZeroes] = remove_zeroValues(rawX, time, frame)
[rawY_noZeroes, _, _] = remove_zeroValues(rawY, time, frame)
[rawZ_noZeroes, _, _] = remove_zeroValues(rawZ, time, frame)

sigma = 5 #3-4 looks pretty good; 5-6 looks very smooth and nice, //2022-04-23
x_filtered = gaussianFilter1D(rawX_noZeroes, sigma)
y_filtered = gaussianFilter1D(rawY_noZeroes, sigma)
z_filtered = gaussianFilter1D(rawZ_noZeroes, sigma)

frame, t = frame_noZeroes, time_noZeroes
x, y, z = x_filtered, y_filtered, z_filtered
v_x, v_y, v_z = np.gradient(x)/np.gradient(t), np.gradient(y)/np.gradient(t), np.gradient(z)/np.gradient(t)
v_x_nofilter, v_y_nofilter, v_z_nofilter = np.gradient(rawX_noZeroes)/np.gradient(t), np.gradient(rawY_noZeroes)/np.gradient(t), np.gradient(rawZ_noZeroes)/np.gradient(t)

plt.plot(t, v_x_nofilter, '-', label="Velocity_x (mm/s), unfiltered")
#plt.plot(t, v_y_nofilter, ':', label="Velocity_y (mm/s), unfiltered")
#plt.plot(t, v_z_nofilter, '.-', label="Velocity_z (mm/s), unfiltered")

if showMultipleSigma:
    x_filteredArray=[]
    for i in range(2,5,1):
        sigma_loop = i+1
        x_filteredArray=gaussianFilter1D(rawX_noZeroes, sigma_loop)
        print(x_filteredArray)
        v = np.gradient(x_filteredArray)/np.gradient(t)
        plt.plot(t, v, label="Velocity_x (mm/s), filtered sigma="+str(sigma_loop))

plt.plot(t, v_x, label="Velocity_x (mm/s), filtered sigma="+str(sigma))
plt.plot(t, v_y, label="Velocity_y (mm/s), filtered sigma="+str(sigma))
plt.plot(t, v_z, label="Velocity_z (mm/s), filtered sigma="+str(sigma))
plt.legend()
#plt.show()


header = ['Frame (processed)', ' Time (s)', ' Calculated velocity X (mm/s)', ' Calculated velocity Y (mm/s)', ' Calculated velocity Z (mm/s)']
processedCSV_rows = merge_vectors_for_writeCSV(frame, t, v_x, v_y, v_z)
write_data_to_CSV(writeFilePath_processedCSV, header, processedCSV_rows)


#EOF
