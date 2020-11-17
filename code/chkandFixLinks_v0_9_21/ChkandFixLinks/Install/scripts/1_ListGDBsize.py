'''
-------------------------------------------------------------------------------
 Tool:    ListFGDBsize 
 Toolbox: CheckAndFixLinks.tbx
 Script:  1_ListGDB.py 
 Purpose: 
  Creates a comma-delmited (.csv) and .xls file of GDB and their 
   size on disk ( approximate MBs).  
   Column names:  Name, GDBpath, ApproxMB
-------------------------------------------------------------------------------   
 Author:  Rebecca Strauch - ADFG-DWC-GIS
 Created on: May 11, 2015
   last modification: August 10, 2015

 Description: This script will walk thru all the File GDB within a folder 
   (incl Subfolders) and create a comma-delimted and Excel .xls list of the 
   File GDBs and their size on disk.

 Arguments:  
   [0] theWorkspace: Folder/directory to search (walk thru, includes subfolders)
   [1] outFile: output base filename, default GDBList, script appends YYYYMMDD_HHMM

 Updates:   
------------------------------------------------------------------------------
'''
import arcpy
import os
from _miscUtils import *
from _gpdecorators import *

# catch_errors decorator must preceed a function using the @ notation.
@catch_errors
def main():
  """
  Main function to create comma delimited file of GDBs in (sub)folder(s)
  """
  # Script arguments...    
  """ If running as standalone, hardcode theWorkspace and outFile  """
  theWorkspace = arcpy.GetParameterAsText(0)
  if not theWorkspace:
    theWorkspace = r"d:\_dataTest"
  arcpy.env.workspace = theWorkspace

  outFile = arcpy.GetParameterAsText(1)
  if not outFile:
    outFile = "GDBList" 
  # Create new output names tagged with start-time YYYYMMDD_HHMM
  fileDateTime = curFileDateTime()
  outFileCSV = os.path.join(theWorkspace, outFile) + fileDateTime + ".csv"
  outFileXLS = os.path.join(theWorkspace, outFile) + fileDateTime + ".xls"    
  myMsgs (outFileCSV)

  def get_size(start_path = '.'):  
    total_size = 0  
    for dirpath, dirnames, filenames in os.walk(start_path):  
      for fc in filenames:  
        fp = os.path.join(dirpath, fc)  
        total_size += os.path.getsize(fp) 
    return total_size  

  with open(outFileCSV, 'w') as csvFile:
    myMsgs("File  {0} is open: {1}".format(outFileCSV, str(not csvFile.closed)))
    csvFile.write("Name, GDBpath, ApproxMB\n")
    for dirpath, dirnames, filenames in os.walk(theWorkspace):  
      for dirname in dirnames:  
        if dirname.endswith('.gdb'):  
          gdb = os.path.join(dirpath, dirname)  
          size = get_size(gdb)  / (1024.00 * 1024)
          size = "{:2f}".format(size)
          myMsgs ("  FGDB:  {0}".format(dirname)) # + ": " +  str(size) + " MB")
          csvFile.write("{0},{1},{2}\n".format(dirname, gdb, size))  

  myMsgs('!!! Success !!!  ')
  csvFile.close()
  arcpy.TableToExcel_conversion(outFileCSV, outFileXLS) #, "NAME", "CODE")
  myMsgs("File  {0} is closed: {1}".format(outFileCSV, str(csvFile.closed)))
# End main function

if __name__ == '__main__':
  main()
