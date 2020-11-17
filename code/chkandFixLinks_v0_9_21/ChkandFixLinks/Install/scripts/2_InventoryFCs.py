'''
---------------------------------------------------------------------------
Tool:    FCInventoryReport 
Toolbox: CheckAndFixLinks.tbx
Script:  2_InventoryFCs.py
Purpose: 
   This script will walk thru all the feature classes within a folder 
   and create a text report, comma-delimted and an Excel .xls file.
   Include shapes, coverages, rasters, tables, connections, and FGDB

   Column names:  FType	FCname	FullPath
-------------------------------------------------------------------------------
 Author:  Rebecca Strauch - ADFG-DWC-GIS
 Created on: 4/10/2013 
   last modification: August 10, 2015

 Description: To create list of the features classes within a folder, including
   coverages (pts, poly, arc, anno), shapes, grids and FGDB data. Outputs list
   to a text report file (not much formatting) in the folder being scanned named
     FCInventoryYYYYMMDD_HHMM.txt
   with the date and time as part of the name. This should always create
   a new file, unless you run it twice within same minute.  

   Must have write permissions on the output folder in question.

   Known issue (with built-in workaround): for some reason some, but not  
     all (ArcInfo) grids want to duplicate the folder name before the 
     describe. I'm now checking to make sure it exists, if not, I am removing
     the duplicate portion, and letting it run.  Seems to work.
------------------------------------------------------------------------------
 Arguments:  
   [0] theWorkspace: Folder/directory to search (walk thru, includes subfolders)
   [1] outFile: output base filename, default GDBList, script appends YYYYMMDD_HHMM

 Updates:          
---------------------------------------------------------------------------
'''
# Import modules
import arcpy
import os
from _miscUtils import *
from _gpdecorators import *

# catch_errors decorator must preceed a function using the @ notation.
@catch_errors
def main():
  """
  Main function to create text file report of all Feature Classes in folder
  """
  #setup environment
  arcpy.env.overwriteOutput = True

  # Script arguments...    
  """ If running as standalone, hardcode theWorkspace and outFile  """
  theWorkspace = arcpy.GetParameterAsText(0)
  if not theWorkspace:
    theWorkspace = r"D:\_dataTest"    

  outFile = arcpy.GetParameterAsText(1)
  if not outFile:
    outFile = "FCInventory" 
  # Create new output name name tagged with YYYYMMDD_HHMM
  fileDateTime = curFileDateTime()
  currentDate = curDate()

  # Create new output name tagged with YYYYMMDD_HHMM
  outfileTXT = os.path.join(theWorkspace, outFile) + fileDateTime + ".txt" #theWorkspace + "\FCInventory" + fileDateTime + ".txt"
  outFileCSV = os.path.join(theWorkspace, outFile) + fileDateTime + ".csv"  #theWorkspace + "\FCInventory" + fileDateTime + ".csv"
  outFileXLS = os.path.join(theWorkspace, outFile) + fileDateTime + ".xls"
  myMsgs(theWorkspace + ", " + outfileTXT)
  reportFile = open(outfileTXT, 'w')
  csvFile = open(outFileCSV, 'w')
  myMsgs(  "File {0} is open? {1}".format(outfileTXT, str(not reportFile.closed)))
  myMsgs(  "File {0} is open? {1}".format(str(outFileCSV), str(not csvFile.closed)))
  #myMsgs(  "File " + str(csvFile) + " is closed?  " + str(csvFile.closed))     
  myMsgs("Writing the report to: " + outfileTXT + " and " + outFileCSV)

  outText = "List of all GIS data in " + theWorkspace + " on " + currentDate + '\n'
  outText += "  Includes coverages (pts, poly, arc, anno), shapes, and FGDB data." + '\n'
  outText += "-----------------------------------------------------" + '\n'

  reportFile.write(outText)
  csvFile.write("FType, FCname, FullPath\n")

  def inventory_data(workspace, datatypes):
    for path, path_names, data_names in arcpy.da.Walk(
      workspace, datatype=datatypes):
      if "tic" in data_names:
        data_names.remove('tic')
      for data_name in data_names:
        fcName = os.path.join(path, data_name)
        #myMsgs("Show for debug: " + fcName)
        if not arcpy.Exists(fcName):
          # workaround for raster folder name duplicating
          fcName = os.path.dirname(fcName)
        desc = arcpy.Describe(fcName)
        #myMsgs("debug, desc it to me: " + desc.dataType)
        yield [path, data_name, desc.dataType] #, desc]

  i = 0
  for feature_class in inventory_data(theWorkspace, "FeatureClass"):
    if i == 0:
      myMsgs(' ' + feature_class[0])
      outText = ' ' + feature_class[0] + '\n'
      reportFile.write(outText)
      path0 = feature_class[0]
      i =+ 1
    elif not path0 == feature_class[0]:
      myMsgs(' ' + feature_class[0])
      outText = ' ' + feature_class[0] + '\n'
      reportFile.write(outText)
      i = 0
    myMsgs("       " + feature_class[2] + ":  " + feature_class[1])
    outText = ("       " + feature_class[2] + ":  " + feature_class[1] + '\n')
    reportFile.write(outText)
    csvFile.write("{},{}, {}\n".format(feature_class[2], feature_class[1], feature_class[0]))

  reportFile.close()
  csvFile.close()
  myMsgs(  "File {0} is closed? {1}".format(outfileTXT, str(reportFile.closed)))
  myMsgs(  "File {0} is closed? {1}".format(outFileCSV, str(csvFile.closed)))

  # Creates Excel .xls file from the .csv ....easier to edit (ver 1)
  arcpy.TableToExcel_conversion(outFileCSV, outFileXLS) 

  myMsgs('!!! Success !!!  ')

# End main function

if __name__ == '__main__':
  main()
