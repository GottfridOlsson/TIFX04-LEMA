#----------------------------------------------------------##
#        Name: TIFX04-22-82, DataProcessing LEMA
#      Author: GOTTFRID OLSSON 
#     Created: 2022-04-22, 13:55
#     Updated: 2022-05-06, 17:51
#       About: Takes in CSV-data från Qualisys measurement
#              and applies gaussian filter and excecutes a
#              numerical derivative to get velocity
#              Saves processed data to another CSV-file.
#              Process: S-measurements, I_coils, eta.
##---------------------------------------------------------##



import os
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



## DATA PROCESSING ##

def remove_zeroValues(position, time):#, *frame): #frame removed, 2022-04-27
    position_noZeroes = []
    time_noZeroes = []
    #frame_noZeroes = []
    #print("remove_zeroValues: len(time): " + str(len(time)))
    for k in range(len(position)):
        if position[k] != 0:
            position_noZeroes.append(position[k])
            time_noZeroes.append(time[k])
            #frame_noZeroes.append(frame[i])
    
    #print("DONE: Removed values with '0.000' from position and time vectors")
    return position_noZeroes, time_noZeroes#, frame_noZeroes

def gaussianFilter1D(array1D, sigma):
    #print("DONE: Filtered data with sigma="+str(sigma))
    return gaussian_filter1d(array1D, sigma)




def get_filePaths_ofFilenames_inFolder(filePathToFolder, filenames):
    filePaths = []
    for i in range(len(filenames)):
        filePaths.append(filePathToFolder + backSlash + filenames[i])
    return filePaths

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

def get_custom_header_from_S_files(filenames, endHeaderString):
    S_numbers = []
    S_header= []
    for i in range(len(filenames)):
        S_numbers.append( get_part_of_string(filenames[i], 1, 3) )#gives start to set as header for new CSV-file, e.g. "S13" or "S20"
        S_header.append( S_numbers[i] + endHeaderString)
    return S_header

def get_custom_header_from_DX_files(filenames, endHeaderString):
    DX_numbers = []
    DX_header  =[]
    for i in range(len(filenames)):
        DX_numbers.append( "DX_"+get_part_of_string(filenames[i], 4, 7) )#gives start to set as header for new CSV-file, e.g. "38mm" or "S20"
        DX_header.append( DX_numbers[i] + endHeaderString)
    return DX_header

def create_dataFrame_S_time_and_Xpos_data(filePaths, filenames):
    XposData  = get_columnData_from_CSV_files(filePaths, 2) #2 for X-position
    timeData  = get_columnData_from_CSV(filePaths[0], 1)
    header    = get_custom_header_from_S_files(filenames, " X-position (mm)")
    dataFrame = pd.DataFrame(XposData, header).transpose()
    dataFrame.insert(loc=0, column='Time (s)', value=timeData)
    return dataFrame

def create_dataFrame_DX_time_and_Xpos_data(filePaths, filenames):
    XposData  = get_columnData_from_CSV_files(filePaths, 2) #2 for X-position
    timeData  = get_columnData_from_CSV(filePaths[0], 1)
    header    = get_custom_header_from_DX_files(filenames, " X-position (mm)")
    dataFrame = pd.DataFrame(XposData, header).transpose()
    dataFrame.insert(loc=0, column='Time (s)', value=timeData)
    return dataFrame

def write_dataFrame_to_CSV(dataFrame, filePath_CSV):
    dataFrame.to_csv(filePath_CSV, CSV_DELIMITER, index=False)
    print("DONE: Write dataFrame to CSV: " + str(filePath_CSV))


def add_one_column_from_CSV_to_CSV(column, from_CSV_path, CSV_path, new_CSV_path):
    from_CSV = read_CSV(from_CSV_path)
    from_header = get_CSV_header(from_CSV)

    CSV = read_CSV(CSV_path)
    header = get_CSV_header(CSV)

    columnHeader = from_header[column]
    columnData = from_CSV[columnHeader]
    CSV.insert(loc=len(header), column=columnHeader, value=columnData)

    CSV.to_csv(new_CSV_path, CSV_DELIMITER, index=False)
    print("DONE: Add one column from " + str(from_CSV_path) + " \n      to " + str(new_CSV_path))


def add_all_columns_from_CSV_to_CSV(from_CSV_path, CSV_path, new_CSV_path):
    from_CSV = read_CSV(from_CSV_path)
    from_header = get_CSV_header(from_CSV)

    CSV = read_CSV(CSV_path)
    header = get_CSV_header(CSV)

    for i in range(len(from_header)):
        columnHeader = from_header[i]
        columnData = from_CSV[columnHeader]
        CSV.insert(loc=len(header)+i, column=columnHeader, value=columnData)

    CSV.to_csv(new_CSV_path, CSV_DELIMITER, index=False)
    print("DONE: Added all columns from " + str(from_CSV_path) + " \n      to " + str(new_CSV_path))




## CONSTANTS FOR THIS PROJECT ##

currentPath = os.path.abspath(os.getcwd())
backSlash = "\\"
raw_CSV_folder_path       = currentPath + backSlash + "Raw CSV"
formatted_CSV_folder_path = currentPath + backSlash + "Formatted CSV"
processed_CSV_folder_path = currentPath + backSlash + "Processed CSV"
# S for 'final measurements of speed (10m/s)' and DX for 'Diode x-position'
filenames_S  = ['S13_20220426_1524.csv', 'S14_20220426_1526.csv', 'S15_20220426_1529.csv', 'S16_20220426_1534.csv', 'S17_20220426_1539.csv', 'S18_20220426_1547.csv', 'S19_20220426_1550.csv', 'S20_20220426_1552.csv', 'S21_20220426_1605.csv', 'S22_20220426_1609.csv', 'S23_20220426_1612.csv']
filenames_DX = ['DX_32mm_20220426.csv',  'DX_33mm_20220426.csv',  'DX_34mm_20220426.csv',  'DX_35mm_20220426.csv',  'DX_36mm_20220426.csv',  'DX_37mm_20220426.csv',  'DX_38mm_20220426.csv',  'DX_39mm_20220426.csv',  'DX_40mm_20220426.csv',  'DX_41mm_20220426.csv',  'DX_42mm_20220426.csv',  'DX_43mm_20220426.csv',  'DX_44mm_20220426.csv']
filenames_I  = ['I_Steg1_20220429_SD2.csv', 'I_Steg2_20220429_SD2.csv', 'I_Steg3_20220426.csv', 'I_Steg4_20220426.csv', 'I_Steg5_20220426.csv']
filename_I_allCoils = ['I_allCoils_20220426.csv']
filePaths_S  = get_filePaths_ofFilenames_inFolder(formatted_CSV_folder_path, filenames_S)
filePaths_DX = get_filePaths_ofFilenames_inFolder(formatted_CSV_folder_path, filenames_DX)
filePaths_I  = get_filePaths_ofFilenames_inFolder(raw_CSV_folder_path,       filenames_I)
filePath_I_allCoils_raw = raw_CSV_folder_path + backSlash + "I_allCoils_20220426.csv"
filePath_S13_through_S23_time_Xpos           = formatted_CSV_folder_path + backSlash + "S_time_Xpos_20220428.csv"
filePath_processed_S13_through_S23_time_Xvel = processed_CSV_folder_path + backSlash + "S_time_Xvel_20220428_sigma5.csv"

filePath_simulated_S_data_CSV           = formatted_CSV_folder_path + backSlash + "Simulated_S_data_20220428.csv" 
filePath_processed_and_simulated_S_data = processed_CSV_folder_path + backSlash + "Processed_and_simulated_S_Xvel_sigma5_20220428.csv"

filePath_I_all_individual_coils           = processed_CSV_folder_path + backSlash + "I_Steg12345_20220428.csv"
filePath_I_all_individual_coils_processed = processed_CSV_folder_path + backSlash + "I_Steg12345_20220428_correctedCurrent.csv"
filePath_I_allCoils = processed_CSV_folder_path + backSlash + "I_allCoils_20220428_nonCorrected.csv"

filePath_processedSimulatedSdata_IallCoils = processed_CSV_folder_path + backSlash + "processedSimulatedSdata_and_IallCoils_sameKfactor_20220429.csv"

filePath_DX_all       = formatted_CSV_folder_path + backSlash + "DX_allPos_20220503.csv"
filePath_DX_processed = processed_CSV_folder_path + backSlash + "DX_processed_20220504.csv"





## MAIN ##

S_analysis = False #measurements S13-S23 taken 20220426
plot_Sdata = False #plot "gaussed and derivative and noZeroed"-data
add_simulatedData_to_S = False

I_coils_analysis = False
combineIallCoils_and_Smeasurement= False

DX_stage2_analysis = False #measurements for stage 2, X-position of sensor (diode)
#plot_DXdata_gaussed = False
plot_DXdata_sameStartTime = False

eta_calc = True
eta_calc_per_stage = True

if S_analysis:
    print("ANALYSIS: S-measurements")
    filePath = filePath_S13_through_S23_time_Xpos
    processedFilePath = filePath_processed_S13_through_S23_time_Xvel
    dataFrame_S = create_dataFrame_S_time_and_Xpos_data(filePaths_S, filenames_S)
    write_dataFrame_to_CSV(dataFrame_S, filePath)

    data = read_CSV(filePath) #data is: 0 = time, 1 = Xpos S13, 2 = Xpos S14, 3 = Xpos S15, ...
    header = get_CSV_header(data)
    Xpos_range = range(1,12) #which Xpos_S columns to keep in analysis
    column_start = min(Xpos_range)
    time = data[header[0]]

    # apply gaussian for each column in Xpos_range before velcity calc
    sigma = 5 #arbitrarily chosen as 5
    V_x_S  = [None for x in Xpos_range]
    time_S = [None for x in Xpos_range]
    V_x_header = [None for x in Xpos_range]
    Xpos_S_gaussed = [None for x in Xpos_range]
 
    for i in Xpos_range:
        # gauss filter per column (Xpos for each S-measurement)
        Xpos_S_i = data[header[i]]
        [Xpos_S_i_noZeroes, time_noZeroes] = remove_zeroValues(Xpos_S_i, time)
        Xpos_S_gaussed[i-column_start] = gaussianFilter1D(Xpos_S_i_noZeroes, sigma)

        # get velocity in x-axis by use of gradient (negative since Qualisys defines coordinate system different from us)
        V_x_S[i-column_start] = -(np.gradient(Xpos_S_gaussed[i-column_start])/np.gradient(time_noZeroes))/1000 #div 1000 to mm/s --> m/s

        # remove values from velocity that are below a certain lower limit (+ som buffer rows(?)) to align S-measurements in time with each other
        V_x_S_i = V_x_S[i-column_start]
        minSpeed = 80/1000 # 80 mm/s = 80/1000 m/s, from figure
        for k in range(len(V_x_S_i)):
            if V_x_S_i[k] > minSpeed:
                firstFastIndex = k
                break
        numIndexesBeforeMinSpeed = 50 #in order to get data where dx/dt = 0 in figure
        indexes = range(firstFastIndex-numIndexesBeforeMinSpeed, len(V_x_S_i))

        V_x_S_i_selected = [V_x_S_i[x] for x in indexes]
        time_selected    = [time_noZeroes[x] for x in indexes]

        removeNumLastDataPoints = 20 #remove last 20 points, since numerical derivative gets funky there
        V_x_S_i_selected = V_x_S_i_selected[0:len(V_x_S_i_selected)-removeNumLastDataPoints]
        time_selected    = time_selected[0:len(time_selected)-removeNumLastDataPoints]
     
        # plot to make sure it looks good
        t = time_selected
        time_S[i-column_start] = t
        V_x = V_x_S_i_selected
        V_x_S[i-column_start] = V_x
        
        if i != 3: #remove S15 which had bad data from Qualisys, 2022-04-27
            plt.plot(t, V_x, label=str(header[i])+" (calc dx/dt, sigma="+str(sigma)+")")
    
    if plot_Sdata:
        plt.legend()
        plt.show()

    # remove end points of vectors s.t. they become only as long as the shortest (for average later)
    V_x_S_temp = V_x_S.copy()
    V_x_S_temp.pop(2) #remove S15 measurement
    V_x_S_selected = V_x_S_temp 

    minVectorLen = len(min(V_x_S_selected, key=len))
    V_x_S_cut = V_x_S_selected.copy()
    for i in range(len(V_x_S_selected)):
        V_x_S_cut[i] = V_x_S_selected[i][0:minVectorLen]
        
    t = t[0:minVectorLen] 
    
    arbitraryStartTime_ms = []
    dt = 0.0001*1000 #timestep in Qualiys-data (s)*1000 to get in milliseconds (ms)
    t_index_correction_from_figure = 5 #looked at figure and picked an index value s.t. t=0 looks good w.r.t. calculated dx/dt
    for i in range(len(max(V_x_S_cut, key=len))):
        arbitraryStartTime_ms.append(dt*(i-numIndexesBeforeMinSpeed+t_index_correction_from_figure)) 

    V_x_average = np.average(V_x_S_cut, axis=0)
    V_x_header = get_custom_header_from_S_files(filenames_S, ' dx/dt (m/s)')
    V_x_header.pop(1) #remove S15 header
    V_x_dataFrame = pd.DataFrame(V_x_S_cut, V_x_header).transpose()
    V_x_dataFrame.insert(loc=0, column='Average dx/dt (m/s)', value=V_x_average)
    V_x_dataFrame.insert(loc=0, column='Arbitrary start time (ms)', value=arbitraryStartTime_ms)
    write_dataFrame_to_CSV(V_x_dataFrame, processedFilePath)

    if add_simulatedData_to_S:
        print("ANALYSIS: S-measurements: added simulated data to S-file")
        add_all_columns_from_CSV_to_CSV(filePath_simulated_S_data_CSV, processedFilePath, filePath_processed_and_simulated_S_data)
    

    # choose time for v_final and calculate standard deviation from all S-measurements at that time t_f
    t_f = 94 #[ms], choosen from figure
    tol = 0.001 #[ms]
    indexes_tf = np.where(np.isclose(arbitraryStartTime_ms, t_f, tol))
    indexes_tf = int(indexes_tf[0])
    V_f = V_x_average[indexes_tf]

    V_x_at_tf = []
    for i in range(len(V_x_S_cut)):
        V_x_at_tf.append( V_x_S_cut[i][indexes_tf] ) 
        
    sigma_f = np.std(V_x_at_tf)
    sigma_f_weighterNumberOfAveragesSeries = sigma_f/np.sqrt(len(V_x_S_cut))
    print("v_f: "+str(V_f) + " m/s \n sigma_f_weighted_N: "+str(sigma_f_weighterNumberOfAveragesSeries) + " m/s \n t_f: ("+str(t_f)+" \pm "+str(tol)+") ms\n")



    quit()
    

if I_coils_analysis:
    print("ANALYSIS: current through coils")
    for i in range(1,len(filePaths_I)): #skip first file since we use first file for current through coilpar 1
        if i == 1:
            add_one_column_from_CSV_to_CSV(1, filePaths_I[i], filePaths_I[0], filePath_I_all_individual_coils)
        else:
            add_one_column_from_CSV_to_CSV(1, filePaths_I[i], filePath_I_all_individual_coils, filePath_I_all_individual_coils)
    
    I_data = read_CSV(filePath_I_all_individual_coils)
    header = get_CSV_header(I_data)

    t = I_data[header[0]]*1000 #s --> ms
    I_coil_measured = []
    for i in range(1,len(header)):
        I_coil_measured.append(I_data[header[i]])
        plt.plot(t, I_coil_measured[i-1], label="non-corrected current coilpar "+str(i))

    plt.legend()
    #plt.show()

    # correction of measured current vs. actual current through coilpair (we used current divider as to not cap the oscilloscope)
    K_factor = [3,3,4,4,4] #measured K_i = I_actualCurrent / I_measuredCurrent  for coilpair i

    I_coil_corrected = []
    for i in range(len(I_coil_measured)):
        I_coil_corrected.append(I_coil_measured[i]*K_factor[i])
    
    #write to new CSV
    header_corrected = []
    for i in range(1,len(header)):
        header_corrected.append("Measured current through coilpair "+str(i) + " scaled by factor K_" + str(i)+" = " + str(K_factor[i-1]) + " (A)")

    dataFrame = pd.DataFrame(I_coil_corrected, header_corrected).transpose()
    dataFrame.insert(loc=0, column="Oscilloscope time (ms)", value=t)
    write_dataFrame_to_CSV(dataFrame, filePath_I_all_individual_coils_processed)



    # I_allCoils_20220426
    I_all = read_CSV(filePath_I_allCoils_raw)
    header_I_all = get_CSV_header(I_all)

    t_offset = 1.35 #ms, by looking at graph
    t = I_all[header_I_all[0]]
    t *= 1000 #s --> ms
    t += t_offset #to get first coil to trigger att t = 0

    #t_startStage = []
    #t_endStage = []
    #I_stage = []
    #for i in range(5):
    #    I_stage.append(I_all[header_I_all[1]][])

    ### split I_all into each stage (1,2,3,4,5) and correct by factor K_i according to lablogg
    #plt.plot(t, I_stage[i])

    # filePath_processedSimulatedSdata_IallCoils

    I_all[header_I_all[0]] = t
    K_all = 6 #K_i \approx 6 forall i, this is a test!
    I_zero_offset = 2 #from figure, what is the zero level raised to after we multi *= K_all 
    I_all[header_I_all[1]] *= K_all 
    I_all[header_I_all[1]] -= I_zero_offset
    I_all = I_all.rename(columns={header_I_all[0]: "Oscilloscope time (ms)", header_I_all[1]: "Measured current through all coilpairs (A) scaled by factor " + str(K_all)})
    write_dataFrame_to_CSV(I_all, filePath_I_allCoils)


    if combineIallCoils_and_Smeasurement:
        add_all_columns_from_CSV_to_CSV(filePath_I_allCoils, filePath_processed_and_simulated_S_data, filePath_processedSimulatedSdata_IallCoils)

    quit()


if DX_stage2_analysis:
    print("ANALYSIS: DeltaV as function of sensor position stage 2")

    # do same analysis as for S_analysis for DX-files up until we have speed as function of arbitrary time
    filePaths = filePaths_DX
    acc_filePath = filePath_DX_all

    dataFrame_DX = create_dataFrame_DX_time_and_Xpos_data(filePaths_DX, filenames_DX)
    write_dataFrame_to_CSV(dataFrame_DX, acc_filePath)

    data = read_CSV(acc_filePath)
    header = get_CSV_header(data)
    time = data[header[0]]
    #print("time:" + str(time))
    Xpos = []
    N_DX_measurements = 13 +1 #number of DX-meas plus 1 bcs. index
    for i in range(1,N_DX_measurements):
        Xpos.append(data[header[i]])

    # apply gaussian for each column in Xpos_range before velcity calc
    sigma = 5 #arbitrarily chosen as 5
    V_x   = [None for x in range(1,N_DX_measurements)]
    t     = [None for x in V_x]
    Xpos_gaussed = [None for x in V_x]
    V_x_header = [None for x in V_x]
 
    for i in range(1,N_DX_measurements):
        # gauss filter per column (Xpos for each S-measurement)
        Xpos_i = Xpos[i-1]
        [Xpos_i_noZeroes, time_noZeroes] = remove_zeroValues(Xpos_i, time)
        Xpos_gaussed[i-1] = gaussianFilter1D(Xpos_i_noZeroes, sigma)

        # get velocity in x-axis by use of gradient (negative since Qualisys defines coordinate system different from us)
        V_x[i-1] = -(np.gradient(Xpos_gaussed[i-1])/np.gradient(time_noZeroes))/1000 #div 1000 to mm/s --> m/s
        
        # remove values from velocity that are below a certain lower limit (+ som buffer rows(?)) to align S-measurements in time with each other
        V_x_i = V_x[i-1]
        minSpeed = 50/1000 # 80 mm/s = 80/1000 m/s
        for k in range(len(V_x_i)):
            firstFastIndex = 0
            if V_x_i[k] > minSpeed:
                firstFastIndex = k
                break
        numIndexesBeforeMinSpeed = 50 #in order to get data where dx/dt = 0 in figure
        indexes = range(firstFastIndex-numIndexesBeforeMinSpeed, len(V_x_i))

        V_x_i_selected = [V_x_i[x] for x in indexes]
        time_selected  = [time_noZeroes[x] for x in indexes]

        removeNumLastDataPoints = 20 #remove last points, since numerical derivative gets funky there
        V_x_i_selected = V_x_i_selected[0:len(V_x_i_selected)-removeNumLastDataPoints]
        time_selected  = time_selected[0:len(time_selected)-removeNumLastDataPoints]
     
        # plot to make sure it looks good
        V_x[i-1] = V_x_i_selected
        t = time_selected #_noZeroes
        
        #plt.plot(t, V_x[i-1], label=str(header[i])+" (DX calc. dx/dt, sigma="+str(sigma)+")")
        
    #if plot_DXdata_gaussed:
        #plt.legend()
        #plt.show()

    arbitraryStartTimes_ms = []
    for i in range(len(V_x)):
        arbitraryStartTimes_ms.append(time[0:len(V_x[i-1])]*1000) # (s)*1000 = (ms)
        plt.plot(arbitraryStartTimes_ms[i], V_x[i-1], label=str(header[i])+" (DX calc. dx/dt, sigma="+str(sigma)+")" )

    if plot_DXdata_sameStartTime:
        plt.legend()
        plt.show()


    # pick times to calculate v_1 and v_2 (times from figure, plot_DXdata_sameStartTime)
    t_v1 = 35 #(ms)
    t_v2 = 58 #60 #(ms), 59 looks good
    tol = 0.0005 #this number gives correct value of time 35ms and 60ms
    
    v_1 = []
    v_2 = []
    for i in range(len(V_x)):
        index_v_1 = np.where(np.isclose(arbitraryStartTimes_ms[i], t_v1, tol))
        index_v_2 = np.where(np.isclose(arbitraryStartTimes_ms[i], t_v2, tol))
        index_v_1 = int(index_v_1[0])
        index_v_2 = int(index_v_2[0])
        v_1.append(V_x[i][index_v_1])
        v_2.append(V_x[i][index_v_2])
    

    Delta_v_21 = [abs(x-y) for x,y in zip(v_2, v_1)] #https://stackoverflow.com/questions/23173294/how-to-mathematically-subtract-two-lists-in-python
    
    processedFilePath = filePath_DX_processed
    header = ["Calculated Delta v_21 (m/s) at times t1: "+str(t_v1)+" (ms) and t2: "+str(t_v2)+" (ms)", "Stage 2: DX distance (mm)"]
    DX_mm_data = [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44] #couldn't be bothered to make this programmatically
    Delta_v_data = [Delta_v_21, DX_mm_data]
    Delta_v_dataFrame = pd.DataFrame(Delta_v_data, header).transpose()
    write_dataFrame_to_CSV(Delta_v_dataFrame, processedFilePath)
    print(Delta_v_21)
    
    # TODO: 
    #how to calculate uncertainty in Delta_v[i] for DXi?

    quit()

if eta_calc:
    v_f = 10.01 # (m/s) from S-analysis, 2022-05-03
    v_f_pm = 0.07 # (m/s) from standard deviation of mean v_f from S-analysis, 2022-05-03
    u = 305 #(V) from lablogg, 2022-05-03
    u_pm = 5 #(V)
    m = 0.11820 # (kg), mass projectile
    m_pm = 0.00005 #(kg)
    C_stage    = [493*1e-6, 488*1e-6, 495*1e-6, 501*1e-6, 492*1e-6] #(farad), measured: 2022-05-10
    C_stage_pm = [0.5*1e-6, 0.5*1e-6, 0.5*1e-6, 0.5*1e-6, 0.5*1e-6] #(farad), measured: 2022-05-10
    C = np.average(C_stage)
    C_pm = np.average(C_stage_pm)
    N_c = len(C_stage) #5 capacitors

    E_capacitors = 0
    
    for i in range(N_c):
        E_capacitors += (1/2)*C_stage[i]*u**2
        print(E_capacitors)
    E_projectile = (1/2)*m*v_f**2

    eta = E_projectile/E_capacitors # = m*v^2 / C*V^2

    #error propagation formula (formula: F(x_1, x_2, ..., x_n) has \pm DeltaF : DeltaF^2 = sum_{i=1}^{n} (dF/dx_i * Deltax_i )^2 )
    eta_pm_exakt = m*v_f**2/(N_c*C*u**2) * np.sqrt( (m_pm/m)**2 + (2*v_f_pm/v_f)**2 + (C_pm/C)**2 + (2*u_pm/u)**2 )

    print("Total eta = ("+str(eta*100) +" \pm_max "+str(eta_pm_exakt*100) + ") % (exakt errorpropagation)")

    if eta_calc_per_stage:
        v_in_stage     = [0, 3.6, 5.8, 7.4, 8.8] #from figure
        v_in_stage_pm  = [0, 0.05, 0.05, 0.05, 0.05] #from figure
    
        v_out_stage    = [3.6, 5.8, 7.4, 8.8, 10.01]
        v_out_stage_pm = [0.05, 0.05, 0.05, 0.05, 0.05]
        

        v_out_2_minus_v_in_2_stage = []
        delta_vin_vout_squared_stage_pm = []
        for j in range(len(v_in_stage)):
            v_out_2_minus_v_in_2_stage.append(v_out_stage[j]**2 - v_in_stage[j]**2)
            
            #errorpropagation formula for v_out^2 - v_in^2: (calc. exakt by hand, formula: DeltaF^2 = sum_i (dF/dx_i * Deltax_i)^2 )
            delta_vin_vout_squared_stage_pm.append( 2*np.sqrt(v_in_stage[j]**2 * v_in_stage_pm[j]**2 + v_out_stage[j]**2 * v_out_stage_pm[j]**2) )

        #deltaV_stage    = [3.6, 2.22, 1.6, 1.40, 1.20]  #(m/s)
        deltaV_stage_pm = [0.1, 0.05, 0.1, 0.05, 0.05] #(m/s)
        C_stage    = [493*1e-6, 488*1e-6, 495*1e-6, 501*1e-6, 492*1e-6] #(farad)
        C_stage_pm = [0.5*1e-6, 0.5*1e-6, 0.5*1e-6, 0.5*1e-6, 0.5*1e-6] #(farad)
        
        for k in range(len(v_out_2_minus_v_in_2_stage)):
            eta = m*v_out_2_minus_v_in_2_stage[k]/(C_stage[k]*u**2)
             # eta_pm_max = m_pm*abs(v_out_2_minus_v_in_2_stage[k]/(C_stage[k]*u**2)) + deltaV_stage_pm[k]*abs(2*m*v_out_2_minus_v_in_2_stage[k]/(C_stage[k]*u**2)) + C_stage_pm[k]*abs((-1)*m*v_out_2_minus_v_in_2_stage[k]/(C_stage[k]**2*u**2)) + V_pm*abs((-2)*m*v_out_2_minus_v_in_2_stage[k]/(C_stage[k]*V**3))
            # error propagation formula (Exakt)
            eta_pm_exakt = m*v_out_2_minus_v_in_2_stage[k]/(C_stage[k]*u**2) * np.sqrt( (m_pm/m)**2 + (delta_vin_vout_squared_stage_pm[k]/v_out_2_minus_v_in_2_stage[k])**2 + (C_stage_pm[k]/C_stage[k])**2 + (2*u_pm/u)**2 )

            print("Stage "+ str(k+1)+"; eta = ("+str(eta*100) +" \pm_max "+str(eta_pm_exakt*100) + ") % (exakt error propagation)")

    quit()


#EOF
