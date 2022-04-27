#----------------------------------------------------------##
#        Name: TIFX04-22-82, DataProcessing LEMA
#      Author: GOTTFRID OLSSON 
#     Created: 2022-04-22, 13:55
#     Updated: 2022-04-27, 11:38
#       About: Takes in CSV-data från Qualisys measurement
#              and applies gaussian filter and excecutes a
#              numerical derivative to get velocity
#              Saves processed data to another CSV-file
##---------------------------------------------------------##



import os
import csv
from unittest import result
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


# FILE PATHS #

def get_filePaths_ofFilenames_inFolder(filePathToFolder, filenames):
    filePaths = []
    for i in range(len(filenames)):
        filePaths.append(filePathToFolder + backSlash + filenames[i])
    return filePaths



## CONSTANTS FOR THIS PROJECT ##

currentPath = os.path.abspath(os.getcwd())
backSlash = "\\"
formatted_CSV_folder_path = currentPath + backSlash + "Formatted CSV"

# S for 'final measurements of speed (10m/s)' and DX for 'Diode x-position'
filenames_S  = ['S13_20220426_1524.csv', 'S14_20220426_1526.csv', 'S15_20220426_1529.csv', 'S16_20220426_1534.csv', 'S17_20220426_1539.csv', 'S18_20220426_1547.csv', 'S19_20220426_1550.csv', 'S20_20220426_1552.csv', 'S21_20220426_1605.csv', 'S22_20220426_1609.csv', 'S23_20220426_1612.csv']
filenames_DX = ['DX_32mm_20220426.csv',  'DX_33mm_20220426.csv',  'DX_34mm_20220426.csv',  'DX_35mm_20220426.csv',  'DX_36mm_20220426.csv',  'DX_37mm_20220426.csv',  'DX_38mm_20220426.csv',  'DX_39mm_20220426.csv',  'DX_40mm_20220426.csv',  'DX_41mm_20220426.csv',  'DX_42mm_20220426.csv',  'DX_43mm_20220426.csv',  'DX_44mm_20220426.csv']
filePaths_S  = get_filePaths_ofFilenames_inFolder(formatted_CSV_folder_path, filenames_S)
filePaths_DX = get_filePaths_ofFilenames_inFolder(formatted_CSV_folder_path, filenames_DX)



# small main #


def get_columnData_from_CSV(filePath, column):
    CSV = read_CSV(filePath)
    header = get_CSV_header(CSV)
    columnData = CSV[header[column]]
    return columnData

def get_part_of_string(string, startIndexInclusive, endIndexInclusive):
    result = string[startIndexInclusive-1:endIndexInclusive]
    return result

def get_columnData_from_CSV_files(filePaths, column):
    columnData = []
    for i in range(len(filePaths)):
        columnData.append(get_columnData_from_CSV(filePaths[i], column))
    return columnData

def get_Xpos_header_from_S_files(filenames):
    S_numbers = []
    S_header= []
    for i in range(len(filenames)):
        S_numbers.append( get_part_of_string(filenames[i], 1, 3) )#gives start  to set as header for new CSV-file, e.g. "S13" or "S20"
        S_header.append( S_numbers[i] + " X-position (mm)")
    return S_header

def create_dataFrame_S_time_and_Xpos_data(filePaths, filenames):
    XposData  = get_columnData_from_CSV_files(filePaths, 2)
    timeData  = get_columnData_from_CSV(filePaths[0], 1)
    header    = get_Xpos_header_from_S_files(filenames)
    dataFrame = pd.DataFrame(XposData, header).transpose()
    dataFrame.insert(loc=0, column='Time (s)', value=timeData)
    return dataFrame

def write_dataFrame_to_CSV(dataFrame, filePath_CSV):
    dataFrame.to_csv(filePath_CSV, CSV_DELIMITER, index=False)
    print("DONE: Write dataFrame to CSV: " + str(filePath_CSV))

get_columnData_from_CSV(filePaths_S[0], 0) #gets columndata (x) for all files, do loop
get_part_of_string(filenames_S[0], 1, 3) #gives start of "S13" to set as header for new CSV-file

get_columnData_from_CSV_files(filePaths_S, 2)
get_Xpos_header_from_S_files(filenames_S)

dataFrame_S = create_dataFrame_S_time_and_Xpos_data(filePaths_S, filenames_S)
write_dataFrame_to_CSV(dataFrame_S, formatted_CSV_folder_path + backSlash + "S13_through_S23_time_Xpos.csv")

quit()






## MAIN ##

filename_rawCSV = 'IckeOptimeradeTriggers_300V_20220422_1150' #needs to be filled in manually
readFilePath_rawCSV = "RAW CSV/"+str(filename_rawCSV) + ".csv"

filename_processedCSV = filename_rawCSV + "_processed_20220424_1122" #needs to be filled in manually
writeFilePath_processedCSV = "Gaussed and derivative CSV/"+str(filename_processedCSV) + ".csv"

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

#time_startAtTequals0 = time - time
time_milliSecond = time*1000
v_x_meterPerSecond, v_y_meterPerSecond, v_z_meterPerSecond = -v_x/1000, -v_y/1000, -v_z/1000
v_x, v_y, v_z = v_x_meterPerSecond, v_y_meterPerSecond, v_z_meterPerSecond
header = ['Frame (processed)', ' Time (ms)', ' Calculated velocity X (m/s)', ' Calculated velocity Y (m/s)', ' Calculated velocity Z (m/s)']
processedCSV_rows = merge_vectors_for_writeCSV(frame, t, v_x, v_y, v_z)
write_data_to_CSV(writeFilePath_processedCSV, header, processedCSV_rows)


#EOF
