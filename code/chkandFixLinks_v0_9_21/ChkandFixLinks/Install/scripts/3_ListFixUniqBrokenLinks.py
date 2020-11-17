'''
-------------------------------------------------------------------------------
Tool: ListUniqueBrokenLinksNoFix AND ListUniqueBrokenLinksWFix (3a and 3b)
Toolbox: CheckAndFixLinks.tbx
Script:  3_ListFixUniqBrokenLinks.py
Purpose:
 Creates unique and sorted lists of "broken sources links", with option
   to "bulk" repair drive letter changes (tool: ListUniqueBrokenLinksWFix), 
   of drive letter to UNC.  As added feature, creates a txt report of all 
   feature classes within each MXD (since it is looping thru anyway)

   NOTE: See results tab for MXD, Broken-links, and Unique-Broekn-Links counts

Created on: May 11, 2015 
   last modification July 28, 2015
-------------------------------------------------------------------------------
Author:  Rebecca Strauch - ADFG-DWC-GIS
Created on: May 11, 2015 
   last modification: August 10, 2015

Description: This script walks through all the MXDs within a folder, and
   creates a comma-delimted, xls (and optional FGDB table) listing all 
   the broken links within all Mxd's within a folder, relative to the user 
   and machine running the comand.
   It also outputs a list (.txt) report of all the feature classes within 
   each MXD, since it is looping and opening each anyway.

   NOTE: best run from the machine and user that will use the mxd since what
     is "broken" is relative to the drives and paths each user sees.

   The output of this tool has several purposes:
    - review broken links to see if a "mass" change in drive letters and/or UNC
      path is all that is needed, or will fix bulk.  If so,m can be modified for
      script 3b.
    - review broken links to find full replacement path. Modify a copy for input into
      tool #4
    - The txt report is just nice to review, and could be used as input to other
      scripts if needed. This list all features classes in an MXD, not just broken ones.
    - I included an option to output the broken links list to a FGDB table, but
      I haven't really found a use for it, so may not even ask for the variable

   NOTE--> The xls or csv output should be reviewed and a copy modified to list 
       the new source path (and type, if different).  That file (must be .csv)
       is used as input for the "RepairDetailedBrokenLinks" tool. Recommend 
       updating a copy (renamed) of the .xls file, then save-as .csv format.

       Also, if just needing to change drive and/or UNC drive names, can use
       simplified version with Tool (3b) ListUniqueBrokenLinksWFix 
       using this same script

   Another tool (3b -using same script) will allow the user to update the
   drive letters or drive letters to UNC path before creating the output.
   Different between the two tools, are the parameters requested (second 
   tool requires a .csv input)

   Tested using ArcGIS 10.3.x

   It may be possible to simplify the code with lists and tuples, however
   initial tests caused issues and I don't have time to fix that since this 
   works and may be easier for new python programers to understand, that is
   this is fairly readable.

   look into.... !newPath!.replace("T:", r"\\dfg.alaska.local\gis\Anchorage\GISStaff")

 Arguments:  
   [0] theWorkspace: Folder/directory to search (walk thru, includes subfolders)
   [1] outFile: output base filename, default BrokenSrc, script appends YYYYMMDD_HHMM
   [2] outFGDB: OPTIONAL, if want FGDB table...haven't found a use for this yet
   [3] inFile: input .csv file for updating drives when running with 3b

Functions:
  findUpdatePath - helps locate the oldPath in the .csv and extracts update path

 Updates:
------------------------------------------------------------------------------
'''
# Import modules
import arcpy
import os
import csv
from _miscUtils import *
from _gpdecorators import *

# function to speed up the update process 
def findUpdatePath(inFile):
  lstFromCSV = []
  #cnt = 0
  #returnNewPath = searchOldPath # for those that can't be found
  with open(inFile) as inFix:
    reader = csv.reader(inFix)
    for row in reader:
      oldPath = row[2]
      newPath = row[3]
      thePaths = (oldPath, newPath)
      lstFromCSV.append(thePaths)
      myMsgs('show old path: {}'.format(row[2]))
      myMsgs('     show new path: {}'.format(row[3]))
      #cnt += 1
  return(lstFromCSV)

# catch_errors decorator must preceed a function using the @ notation.
@catch_errors
def main():
  """
  Main function to add optionally bulk repair, and then create 
  list of layers with broken source path
  """
  # Script arguments...    
  """ If running as standalone, hardcode theWorkspace """
  theWorkspace = arcpy.GetParameterAsText(0)
  if not theWorkspace:
    theWorkspace = r"d:\_dataTest" # \_repair" # r"\\dfg.alaska.local\gis\Anchorage\GISStaff\wc\Specareas"
  if r'\_repair' in theWorkspace:
    processRepairDir = True
  else:
    processRepairDir = False
    
  outFile = arcpy.GetParameterAsText(1)
  if not outFile:
    outFile = "BrokenSrc" # r"N:\RangeMaps\MXD"
  # Create new output file names, tagged with YYYYMMDD_HHMM
  fileDateTime = curFileDateTime()
  currentDate = curDate()
  outfileTXT = os.path.join(theWorkspace, outFile) + fileDateTime + ".txt" 
  outFileCSV = os.path.join(theWorkspace, outFile) + fileDateTime + ".csv"
  outFileXLS = os.path.join(theWorkspace, outFile) + fileDateTime + ".xls"
  myMsgs (outFile)
  reportFile = open(outfileTXT, 'w')

  # Option FGDB, dataset or folder (folder will create an INFO table)
  outFGDB = arcpy.GetParameterAsText(2)
  if not outFGDB:
    pass
  else:
    #outFGDB = "" 
    # Create new Table output name name tagged with same YYYYMMDD_HHMM
    outFGDBtable = os.path.join(outFGDB, outFile) + fileDateTime
    myMsgs (outFGDBtable)  

  inFile = arcpy.GetParameterAsText(3)
  if not inFile:
    pass
  else:
    #inFile = "massChangeDrivefix.csv" """
    #if arcpy.Exists(inFile):
    inFile = os.path.join(theWorkspace, inFile)
    lstMassPathUpdate = findUpdatePath(inFile)
    print("inFile: " + inFile)

  # Opens .csv file in write mode  
  csvFile = open(outFileCSV, "w") 

  myMsgs("File {0} open?  {1}".format(str(outFileCSV), str(not csvFile.closed)))
  # writes column names to .csv file
  csvFile.write("UniqID, dataType, newType, brokenPath, newPath\n")
  # initialize  list and count variables
  uniqueList = []
  mxdCount = 0       # how many mxds are processed
  brokenCount = 0    # total number of broken links found
  uniqCount = 0      # how many UNIQUE broken links found

  # also writing a txt document of all the FC within an MXD, cause I can
  reportFile = open(outfileTXT, 'w')
  myMsgs(  "File {0} is open?  {1}".format(outfileTXT, str(not reportFile.closed)))
  outText = "List of all BROKEN Feature class types in {0}, on {1} \n ".format(theWorkspace, currentDate)
  outText += "  Includes coverages (pts, poly, arc, anno), shapes, and FGDB data." + '\n'
  outText += "-----------------------------------------------------" + '\n'   
  reportFile.write(outText)

  # recursively walk thru all folders and files
  for root, dirs, files in os.walk(theWorkspace): 
    # creates list of .mxd's and works thru them
    for fileName in files:
      if r"\_repair" in root and not processRepairDir:
        #myMsgs("root {0} dirs {1}".format(root, dirs))
        pass
      else:
        fullPath = os.path.join(root, fileName)
        basename, extension = os.path.splitext(fileName)
        # Only process .mxd files
        if extension == ".mxd":
          myMsgs ( "--> Processing: {0} ".format(fullPath))
          reportFile.write("--> Processing: {0} \n ".format(fullPath))
          mxd = arcpy.mapping.MapDocument(fullPath)
          if arcpy.Exists(inFile):
            for updatePath in lstMassPathUpdate:
              #print("mxd.findAndReplaceWorkspacePaths(" + updatePath[0] + "," + updatePath[1] + ", False)" )
              myMsgs("mxd.findAndReplaceWorkspacePaths({0}, {1}, False)".format(updatePath[0], updatePath[1]))
              mxd.findAndReplaceWorkspacePaths(updatePath[0], updatePath[1], False)
              mxd.save()                
          # increment mxd count
          mxdCount += 1
          # creates list of broken links
          theMXD = arcpy.mapping.ListBrokenDataSources(mxd)
          # creates list of what it sees as a tableview
          theTables = arcpy.mapping.ListTableViews(mxd)
          # only process the datasources with broken links
          for lyr in theMXD:
            # increments broken link count
            brokenCount += 1
            # Events are dynamic, so no actual path
            if "Events" in lyr.name:
              # Event tables are temporary and need source update separately
              anItem = ("Events_Table", "--based_on_other_data")  
            # Tables must be treated differently, for some reason
            elif lyr in theTables:
              theSource = lyr.dataSource
              myMsgs("      **** TableView:  " + lyr.name + ", " + theSource)
              if r".xls" in lyr.name:
                lyrType = "table_excel"
              elif r".dbf" in lyr.name:
                lyrType = "table_dbf"
              elif r".dat" in lyr.name:
                lyrType = "table_dat"
              else:
                lyrType = "table_other"
              anItem = (lyrType, theSource)
            # Can't access some Service details like path, so treated differently
            elif lyr.isServiceLayer:  # Can't access Service details like path
              if lyr.supports("SERVICEPROPERTIES"):
                cnt = 0
                for spType, spName in lyr.serviceProperties.iteritems():
                  #myMsgs("   Service Properties: {0}: {1}".format(spType, spName ))
                  if spType == "URL":
                    lyrType = ("service_{}".format(lyr.name))
                    dataSource = str(spName)
                    #pass
                myMsgs("      --> {0}, {1}".format(lyrType, dataSource))
                theSource = dataSource
              anItem = (lyrType, theSource)
            # List various raster layers
            elif lyr.isRasterLayer:
              #myMsgs("  * Raster: {0}".format(str(lyr.name)))
              if r".sde" in lyr.name:
                myMsgs("      ****** SDE: {0}".format(str(lyr.name)))
                lyrType = "sde"
              elif r".tif" in lyr.name:
                lyrType = "raster.tif"
              elif r".sid" in lyr.name:
                lyrType = "raster.sid"
              elif r".tpq" in lyr.name:
                lyrType = "raster.TOPO"
              elif r".bmp" in lyr.name:
                lyrType = "raster.bmp"
              elif r".gif" in lyr.name:
                lyrType = "raster.gif"
              elif r".jpg" in lyr.name:
                lyrType = "raster.jpg"
              else:
                lyrType = "raster"
              myMsgs("      ** {0}: {1} ".format(lyrType, str(lyr.name)))
              anItem = (lyrType, lyr.dataSource)
            # Groups are strange too, so sorting them out, just in case
            #     ...may just skip writting these to file ??
            elif lyr.isGroupLayer:  # not sure if this is needed, but doesn't hurt
              myMsgs ("      ****** Group: {0}".format(str(lyr.name)))
              anItem = ("Group", lyr.name)
            # Feature layers of many types
            elif lyr.isFeatureLayer:
              if lyr.supports("dataSource"): # everything else pretty much
                theSource = lyr.dataSource
                if r".sde" in theSource:  # sde connection files
                  myMsgs("      **** SDE: {0}".format(theSource))
                  lyrType = "sde" 
                elif r".shp" in theSource:  # shapes
                  myMsgs("      ** Shape: {0}".format(theSource))
                  lyrType = "shape"
                elif r".gdb" in theSource:  # file gdb
                  myMsgs("      **  fgdb: {0}".format(theSource))
                  lyrType = "fgdb"                            
                elif r".mdb" in theSource:  # personal gdb or access file
                  myMsgs("      **   pgdb: {0}".format(theSource))
                  lyrType = "pgdb"                            
                elif r".dbf" in theSource:  # dbase format
                  myMsgs("      **    dbf: {0}".format(theSource))
                  lyrType = "dbf"                            
                elif r".txt" in theSource:  # text file
                  myMsgs("      **    txt: {0}".format(theSource))
                  lyrType = "txt"                            
                elif r"\polygon" in theSource:  # coverage polygon features
                  myMsgs("      *** cvrPly: {0}".format(theSource))
                  lyrType = "cover_poly"                            
                elif r"\arc" in theSource:  # coverage arc features
                  myMsgs("      *** cvrArc: {0}".format(theSource))
                  lyrType = "cover_arc"                            
                elif r"\region" in theSource:  # coverage region features
                  myMsgs("      *** cvrReg: {0}".format(theSource))
                  lyrType = "cover_region"                            
                elif r"\point" in theSource:  # coverage point features
                  myMsgs("      *** cvrPts: {0}".format(theSource))
                  lyrType = "cover_point"                            
                elif r"\tic" in theSource:  # coverage point features
                  myMsgs("      *** cvrTic: {0}".format(theSource))
                  lyrType = "cover_tic"                            
                elif r".sdc" in theSource:  # shapes
                  myMsgs("      **   esri: {0}".format(theSource))
                  lyrType = "esri.sdc"
                else: # pretty much everything else 
                  myMsgs("      * Layer: {0},{1}".format(lyr.name, theSource))
                  lyrType = "other"
                #anItem = (lyrType, theSource, lyr.name)
                anItem = (lyrType, theSource)
              else:
                myMsgs("Unknown")
                #anItem = ("Unknown", "blah", lyr.name)
                anItem = ( "__Unknown", "document: " + fullPath)
  
            else:
              myMsgs("***Can't classify **********************************")
              anItem = ("__Unknown", "document: " + fullPath)
            # creates tuple list of uniq combinations, increments uniqcount
            reportFile.write("      {0} \n ".format(anItem))
            if anItem not in uniqueList: 
              uniqueList.append(anItem)
              uniqCount += 1
  uniqueList.sort()  # sorts the list, order Type, Path, TOC
  myMsgs( "---------------------------------------------------" )
  # creates increments value for the UniqID field, just cause I can
  #   added after the append, sort to keep from controlling order and uniqueness
  uniqID = 1   
  # Write each record to .csv file. Order changed to be:
  #   UniqID, lyType, "_review" (as a flag), and broken path
  for item in uniqueList:
    csvFile.write("{}, {}, {},{}\n".format(uniqID, item[0], "_review", item[1]))
    uniqID += 1   # increments UniqID value
  # close .csv file, and shows result
  csvFile.close()
  myMsgs("outFile is closed:  " + str(csvFile.closed))
  # gives some stats on MXDs process, and found and unique broken links ..
  #    Output counts to the .txt file and as a message
  outText2 = "-------------------------------------------------------" + '\n'   
  outText2 +=  (" \n Number of mxd processed:   {0} \n ".format(str(mxdCount)))
  outText2 += ("Number of broken links found: {0} \n ".format(str(brokenCount)))
  outText2 += ("Number of unique broken links: {0} \n ".format(str(uniqCount - 1)))
  reportFile.write(outText2)
  myMsgs(" {0}".format(outText2))

  # close the .txt file, 
  reportFile.close()
  myMsgs(  "File {0} is closed?  {1}".format(outfileTXT, str(reportFile.closed)))

  # Creates Excel .xls file from the .csv ....easier to edit (ver 1)
  arcpy.TableToExcel_conversion(outFileCSV, outFileXLS) 

  # If the option FGDB, dataset of folder were give, create a (GIS) table
  if arcpy.Exists(outFGDB):
    arcpy.ExcelToTable_conversion(outFileXLS, outFGDBtable)
    myMsgs("Created FGDB table " + outFGDBtable)
  else:
    myMsgs(" No FGDB table created. Update the .XLS file: " + outFileXLS +  
           ".... \n   .....then use ExcelToTable for update script.")

  myMsgs('!!! Success !!!  ')

# End main function

if __name__ == '__main__':
  main()
