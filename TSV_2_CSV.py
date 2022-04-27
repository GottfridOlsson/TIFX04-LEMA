#----------------------------------------------------------##
#        Name: TIFX04-22-82, DataProcessing LEMA
#      Author: GOTTFRID OLSSON 
#     Created: 2022-04-27, 09:41
#     Updated: 2022-04-27, 11:25
#       About: Takes in TSV-file from Qualisys measurement
#              and converts it into CSV as well as removing
#              unncecessary header from Qualisys and adding
#              corresponding units in header.
##---------------------------------------------------------##


import pandas as pd                     # for CSV, TSV
import os                               # for currentPath


## CONSTANTS ##

CSV_DELIMITER = ','
TSV_DELIMITER = '\t'

currentPath = os.path.abspath(os.getcwd())
rawTSVfolderRelativePath = "Raw TSV"
headerRemovedTSVfolderRelativePath = "Formatted TSV"
headerRemovedCSVfolderRelativePath = "Formatted CSV"
backSlash = "\\"



## FUNCTIONS ##

def get_filenames_RawTSV():
    path = currentPath + backSlash + rawTSVfolderRelativePath
    dir_list = os.listdir(path)
    print("DONE: Read all filenames in: "+str(path))
    return dir_list

def replace_part_of_string(input, searchString, newString):
    return input.replace(searchString, newString)

def replace_TSV_with_CSV_ending(strings):
    filenames_rawCSV = []
    for i in range(len(filenames_rawTSV)):
        tsv = '.tsv'
        csv = '.csv'
        newfilename_CSV = replace_part_of_string(filenames_rawTSV[i], tsv, csv)
        filenames_rawCSV.append(newfilename_CSV)
    print("DONE: Replaced TSV with CSV ending for files")
    return filenames_rawCSV

def remove_lines_from_file_and_write_new_file(oldFilePath, newFilepath, numberOfLines):
    with open(oldFilePath, 'r') as old:
        data = old.read().splitlines(True)

    with open(newFilepath, 'w') as new:
        new.writelines(data[numberOfLines:])

def remove_Qualisys_header_from_rawTSV_and_write_formattedTSV_files(filenames_rawTSV):
    rawTSV_filePaths = []
    formattedTSV_filePaths = []
    old_path = currentPath + backSlash + rawTSVfolderRelativePath 
    new_path = currentPath + backSlash + headerRemovedTSVfolderRelativePath
    for i in range(len(filenames_rawTSV)):
        rawTSV_filePaths.append(old_path + backSlash + filenames_rawTSV[i])
        formattedTSV_filePaths.append(new_path + backSlash + filenames_rawTSV[i])
    numLinesRemove = 10 #for Qualisys data n = 10
    for i in range(len(rawTSV_filePaths)):
        remove_lines_from_file_and_write_new_file(rawTSV_filePaths[i], formattedTSV_filePaths[i], numLinesRemove)

    print("DONE: Removed Qualisys header ("+str(numLinesRemove)+" lines) from TSV in: " + str(old_path) + "\n      and wrote files to formatted TSV in: " + str(new_path))


def formatted_TSV_2_formatted_CSV(filenames_rawTSV, filenames_rawCSV):

    TSV_path = currentPath + backSlash + headerRemovedTSVfolderRelativePath
    CSV_path = currentPath + backSlash + headerRemovedCSVfolderRelativePath
    for i in range(len(filenames_rawTSV)):
        formattedTSV_path = TSV_path + backSlash + filenames_rawTSV[i]
        formattedCSV_path = CSV_path + backSlash + filenames_rawCSV[i]

        # read TSV and convert to CSV with adjusted # of headers
        csv_table=pd.read_table(formattedTSV_path, sep=TSV_DELIMITER)
        header = csv_table.columns.values
        header_to_CSV = header[0:5] #last header value (6) is nonsense (extra tab) from Qualisys
        csv_table.to_csv(formattedCSV_path, CSV_DELIMITER, columns=header_to_CSV, index=False)

        # add units to header
        new_csv_table = pd.read_csv(formattedCSV_path, sep=CSV_DELIMITER)
        new_header = new_csv_table.columns.values
        new_header_to_CSV = [new_header[0], new_header[1]+" (s)", new_header[2]+" (mm)",  new_header[3]+" (mm)",  new_header[4]+" (mm)"] #add units
        new_csv_table.columns = new_header_to_CSV
        new_csv_table.to_csv(formattedCSV_path, CSV_DELIMITER, index=False)

    print("DONE: Converted formatted TSV into CSV in: " + str(CSV_path))



## MAIN ##

filenames_rawTSV = get_filenames_RawTSV()
filenames_rawCSV = replace_TSV_with_CSV_ending(filenames_rawTSV)
remove_Qualisys_header_from_rawTSV_and_write_formattedTSV_files(filenames_rawTSV) # run 2022-04-27, 09:xx
formatted_TSV_2_formatted_CSV(filenames_rawTSV, filenames_rawCSV)        #run 2022-04-27, 10:47

print("DONE: Code ran successfully!")



## EOF ##
