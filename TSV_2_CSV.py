#----------------------------------------------------------##
#        Name: TIFX04-22-82, DataProcessing LEMA
#      Author: GOTTFRID OLSSON 
#     Created: 2022-04-27, 09:41
#     Updated: 2022-04-24, 14:10
#       About: Takes in TSV-file from Qualisys measurement
#              and converts it into CSV as well as removing
#              unncecessary header from Qualisys
##---------------------------------------------------------##

# COMMENTS/NOTES:
#   make functions to do the smoothing and removinf of zeroes ?
#
#

import pandas as pd                     # for CSV, TSV
import os                               # for get_filenames()

## CSV_handler ##
CSV_DELIMITER = ','
rawTSVfolderRelativePath = "Raw TSV"
headerRemovedTSVfolderRelativePath = "Formatted TSV"
backSlash = "\\"
currentPath = os.path.abspath(os.getcwd())

  
#tsv_file='GfG.tsv'
#csv_table=pd.read_table(tsv_file,sep='\t') 
#csv_table.to_csv('GfG.csv',index=False)  
#print("Successfully made csv file")



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

def remove_Qualisys_header_from_rawTSV_and_write_new_files(filenames_rawTSV):
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

## MAIN ##

filenames_rawTSV = get_filenames_RawTSV()
filenames_rawCSV = replace_TSV_with_CSV_ending(filenames_rawTSV)
remove_Qualisys_header_from_rawTSV_and_write_new_files(filenames_rawTSV)


#print("\n")
#print(filenames_rawTSV)
#print(filenames_rawCSV)



#EOF
