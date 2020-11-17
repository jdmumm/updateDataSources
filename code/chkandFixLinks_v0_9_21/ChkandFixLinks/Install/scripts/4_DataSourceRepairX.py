'''
---------------------------------------------------------------------------
Tool: RepairDetailedBrokenLinks (4)
Script:  4_DataSourceRepairX.py
Toolbox: CheckAndFixLinks.tbx
Purpose: 
 Fix "broken source links" from input .csv 
    NOTE: run from the machine and user that will use the mxd
---------------------------------------------------------------------------
 Author: Rebecca Strauch - ADFG-DWC-GIS
Created on: May 11, 2015 
   last modification: August 24, 2015

   NOTE: run from the machine and user that will use the mxd
---------------------------------------------------------------------------
 Description: 
   This script will loop thru all the MXDs within a folder, and the broken
   links and attempt to repair them based on the input comma delimited file
   with the following fields (header columns are suggested...):
        columns:
          [0] UniqID:  a record number just to help keep track of records
          [1] dataType:  contains layer, shape, or sde from ListUniqueBrokenLink
              Posible Type values:
                Raster, Raster.tif, Raster.sid, Raster.TOPO, Raster.bmp,
                Raster.gif, Raster.jpg, 
                Sde (sde connection file, test may think it's a raster type)
                Shape, Fgdb, Pgdb, Dbf, Txt
                Cover_poly, Cover_arc, Cover_region, Cover_point, Cover_tic:
                Esri.sdc
                other
                Unknown:
                Events: event table (temporary)  should skip these broken links
                Table_excel, Table_dbf, Table_dat, Table_other
          [2] newType: _review if new path not set yet
                   if same as dataType, then will be same type
                   if deiferent than dataType, format is changing
          [3] brokenPath:  contains the full path of the broken link
          [4] newPath:  contains the new path: = brokenPath if no change

   uses the inFile to replace the full path, then saves it to a new mxd 
   in 10.1/10.2 format with _fix appendd to the name

 Arguments:  
   [0] theWorkspace: Folder/directory to search (walk thru, includes subfolders)
   [1] inFile: input .csv file for updating paths
	 [2]  outWorkspace: directory where _repair folder will be create and new mxds written


 Updates:

---------------------------------------------------------------------------
'''
# Import modules
import arcpy
import os
import csv
from _miscUtils import *     # handles the myMsgs and time functions
from _gpdecorators import *  # handles main for catching errors

#----------------------------------------------------------------------

#----------------------------------------------------------------------
def findUpdatePath(inFile, searchOldPath, serviceLayer):
  #def findUpdatePath(inFile, searchOldPath, serviceLayer):
  #rtnNewPath = searchOldPath # for those that can't be found
  # serviceLyaer, blank unless a service
  with open(inFile) as inFix:
    reader = csv.reader(inFix)
    for row in reader:
      if row[3] in searchOldPath:
        oldType = (row[1].strip().lower())
        #print("{0}, {1}..row[1]: {2}, \n        serviceLayer: {3} \n".format((serviceLayer != ""), (oldType == serviceLayer), row[1].strip().lower(), serviceLayer))
        if (serviceLayer == "") and row[3]:
          myMsgs('     >>>> Match found: {}'.format(row))
          rtnNewPath = row[4]
          rtnNewType = row[2].strip().lower()
          rtnSameTypeTF = (row[1].strip().lower() == row[2].strip().lower())
          rtnOldType = row[1].strip().lower()
          rtnOldPath = row[3]
          break
        elif (serviceLayer != "") and (oldType == serviceLayer) and row[3]:
          #print("row[1]: {0}".format(row[1].lower()))
          myMsgs('     >>>> Match found: {}'.format(row))
          rtnNewPath = row[4]
          rtnNewType = row[2].strip().lower()
          rtnSameTypeTF = (row[1].strip().lower() == row[2].strip().lower())
          rtnOldType = row[1].strip().lower()
          rtnOldPath = row[3]
          break
      else:
        #print("no match")
        rtnNewPath = "no match"
        rtnNewType = False
        rtnSameTypeTF = False
        rtnOldType = row[1]
        rtnOldPath = row[3]
  return(rtnNewPath, rtnNewType, rtnSameTypeTF, rtnOldType, rtnOldPath)


# catch_errors decorator must preceed a function using the @ notation.
@catch_errors
def main():
  """
  Main function to add updated source paths to fix broken paths
  """

  # Script arguments...    
  """ If running as standalone, hardcode theWorkspace and inFile  """
  theWorkspace = arcpy.GetParameterAsText(0)
  if not theWorkspace:
    theWorkspace = r"d:\_dataTest"
  arcpy.env.workspace = theWorkspace
  arcpy.env.overwriteOutput = True	

  inFile = arcpy.GetParameterAsText(1)
  if not inFile:
    inFile = "updateMultipleSourcePaths.csv"
    inFile = r"\\dfg.alaska.local\gis\Anchorage\GISStaff\___gisStaffConnections\RepairBrokenSrcAug242015.csv"

  outWorkspace = arcpy.GetParameterAsText(2)
  if not outWorkspace:
    outWorkspace = os.path.join(theWorkspace, "_repaired")
  '''if not os.path.isdir(outWorkspace):  
    os.makedirs(outWorkspace)
    myMsgs("created new directory {0} \n".format(outWorkspace))'''

  # Create .txt Report of what it thinks was fixed, tagged with YYYYMMDD_HHMM
  outFile = "FixedReport"
  fileDateTime = curFileDateTime()
  currentDate = curDate()
  outfileTXT = os.path.join(theWorkspace, outFile) + fileDateTime + ".txt" 
  myMsgs (outFile)
  reportFile = open(outfileTXT, 'w')
  myMsgs(  "File {0} is open?  {1}".format(outfileTXT, str(not reportFile.closed)))
  outText = "Report for what it THINKS it repaired in {0}, on {1} \n ".format(theWorkspace, currentDate)
  outText += "  Includes coverages (pts, poly, arc, anno), shapes, and FGDB data." + '\n'
  outText += "-----------------------------------------------------" + '\n'   
  reportFile.write(outText)	

  mxd = None
  outMXDName = "none"
  updatePath = []
  cvrList = [r"\arc", r"\polygon", r"\region", r"\point", r"\tic" ]
  lstExtDatatype = [[".shp", "SHAPEFILE_WORKSPACE" ], [".sde","SDE_WORKSPACE"], 
                    [".mdb", "ACCESS_WORKSPACE" ], [".gdb", "FILEGDB_WORKSPACE"], 
                    ["cover", "ARCINFO_WORKSPACE"]]	
  cntMXD = 0
  cntFixed = 0
  cntTotalFixed = 0

  # makes sure the .csv file exists
  if arcpy.Exists(inFile):
    myMsgs ("->Using {0} to repair paths.\n==============================".format(inFile))
    # walks thru the workspace to create list of files 
    for root, dirs, files in os.walk(theWorkspace): 		
      for fileName in files:
        if root == outWorkspace:  # don't process mxd's in the target directory
          pass
        else:
          fullPath = os.path.join(root, fileName)
          basename, extension = os.path.splitext(fileName)
          # Only process .mxd files
          if extension == ".mxd":
            myMsgs("\nReviewing MXD: {0}".format(fullPath))
            reportFile.write("\nReviewing MXD: {0}".format(fullPath))
            mxd = arcpy.mapping.MapDocument(fullPath)
            dfs = arcpy.mapping.ListDataFrames(mxd)
            cntMXD += 1
            cntFixed = 0
            basename, extension = os.path.splitext(fileName)
            # New output mxd name....
            outMXDName = os.path.join(outWorkspace, (str(basename) + ".mxd")) #"_fix.mxd"))
            # create list of the tables since they are handle differently
            theTables = arcpy.mapping.ListTableViews(mxd)
            # Loops thru dataframes so adding and deleting Services will work.
            for df in dfs:
              # Loops thru layers, checks for broken links and tries to repair
              lyrList = arcpy.mapping.ListLayers(mxd, "", df)
              for lyr in lyrList:
                if lyr.isBroken:
                  if not lyr.supports("DATASOURCE") and not lyr.isServiceLayer:
                    myMsgs("  ->Skipping {0} not a Service layer, and does not support DATASOURCE".format(lyr.name))
                    pass #continue
                  elif not lyr.supports("DATASOURCE") and  lyr.isServiceLayer:
                    myMsgs("  -Broken Service: {0}".format(lyr.name))
                  else:
                    myMsgs("  -Broken: {0}".format(lyr.dataSource))
                  #myMsgs("layer is Group {0} or ServiceLayer {1}".format(lyr.isGroupLayer, lyr.isServiceLayer))
                  if (lyr.isGroupLayer or ("Events" in lyr.name)) and (not lyr.isServiceLayer): # Groups and Event FC skipped
                    myMsgs("    ...skipping group or event: {0}".format(lyr.name))
                    reportFile.write("\n   *skipping group or event: {0} \n".format(lyr.name))
                    pass #break
                  elif lyr.isServiceLayer:    # services might have to be handle differently
                    if lyr.supports("SERVICEPROPERTIES"):
                      for spType, spName in lyr.serviceProperties.iteritems():
                        myMsgs("   Service Properties: {0}: {1}".format(spType, spName ))
                        if spType == "URL": 
                          dataSource = str(spName)
                          lyrType = ("service_{}".format(lyr.name))
                          break
                      myMsgs("    ->this ia a service....using add and remove layer")
                      updatePath = findUpdatePath(inFile, dataSource, lyrType.strip().lower())
                      newDSPath, newDSName = os.path.split(updatePath[0])
                      if ("service" in updatePath[3]) and ("service" in updatePath[1]):
                        insertLayer = arcpy.mapping.Layer(updatePath[0])
                        print("dataframe: {0}".format(df))
                        arcpy.mapping.InsertLayer(df, lyr, insertLayer, "AFTER")
                        arcpy.mapping.RemoveLayer(df, lyr)
                      reportFile.write("\n   ->sees this as service....{0} \n".format(dataSource))
                      # will still look at deleted version after insert, not the new version..
                      #    isBroken will give false info even if fixed, so 
                      #    don't use myMsgs("Still broken? {0}".format(lyr.isBroken)) 
                    else:
                      myMsgs("   --> a service layer but no SERVICE PROPERTIES")
                  elif lyr.supports("DATASOURCE") and lyr.supports("DATASETNAME"):   
                    # not a group, event or what it thinks is a service
                    updatePath = findUpdatePath(inFile, lyr.dataSource, "")
                    newDSPath, newDSName = os.path.split(updatePath[0])
                    sameType = updatePath[2]  
                    for cvr in cvrList:   #checks to see if the source layer is a coverage...must handle different
                      if cvr in lyr.dataSource:
                        sourceIsCoverage = True
                        break
                      else:
                        sourceIsCoverage = False
                    # updatePath[1] is False if there wasn't a match
                    #  so "not update[1]" means no match was found, and moves to next layer								
                    if not updatePath[1]:    # if no match was found
                      myMsgs("     !! no match to: {0} ".format(lyr.dataSource))
                      updateStatus = "no match, not changed"  # used for message only
                      pass
                    elif updatePath[1].strip().lower() == "drive":
                      myMsgs("     skipping drive-letter matches for now: {0}".format(lyr.dataSource))
                      updateStatus = "can only find drive match...look into it)"
                      pass
                    elif updatePath[1].strip().lower() == "_review":
                      myMsgs("      no new source assigned yet for: {0}".format(lyr.dataSource))
                      updateStatus = ("review and update {0}".format(inFile))
                      pass
                    else: #if lyr.supports("DATASOURCE") and lyr.supports("DATASETNAME"):
                      updateStatus = str(updatePath[0])   # used for message only
                      if lyr in theTables:
                        #myMsgs("  thinks its a table....using findAndReplsWorkspacePath")
                        myMsgs("        *Moving {0}: {1} to new: {2}".format(updatePath[3], lyr.dataSource, updatePath[0]))
                        reportFile.write("\n   Moving {0}: {1} to new: {2} \n".format(updatePath[3], lyr.dataSource, updatePath[0]))
                        lyr.findAndReplaceWorkspacePath(lyr.dataSource, updatePath, False)                    
                      elif lyr.isRasterLayer:
                        #myMsgs("  thinks its a raster....using findAndReplsWorkspacePath")
                        myMsgs("        *Moving {0}: {1} to new: {2}".format(updatePath[3], lyr.dataSource, updatePath[0]))
                        reportFile.write("\n   Moving {0}: {1} to new: {2} \n".format(updatePath[3], lyr.dataSource, updatePath[0]))
                        newType = "RASTER_WORKSPACE"
                        for extType in lstExtDatatype:
                          if extType[0] in updatePath[0]:
                            newType = extType[1] 
                            if extType[0] == '.gdb':
                              newDSPath = newDSPath.split('.gdb', 1)[0] + '.gdb'
                              #newType = extType[1]
                            elif extType[0] == '.sde':
                              newDSPath = newDSPath.split('.sde', 1)[0] + '.sde'
                            break                      
                        lyr.replaceDataSource(newDSPath, newType, newDSName, False)
                        if not sameType:
                          testOldTOC = updatePath[4].strip('\\')
                          if lyr.name == testOldTOC:
                            lyr.name = lyr.datasetName
                      else:
                        newType = updatePath[1] 
                        if sourceIsCoverage and sameType:
                          newDSPath = os.path.split(newDSPath)[0]
                          newType = "ARCINFO_WORKSPACE"
                        for extType in lstExtDatatype:
                          if extType[0] in updatePath[0]:
                            newType = extType[1]
                            if extType[0] == '.gdb':
                              newDSPath = newDSPath.split('.gdb', 1)[0] + '.gdb'
                              #newType = extType[1]
                            elif extType[0] == '.sde':
                              newDSPath = newDSPath.split('.sde', 1)[0] + '.sde'

                            break
                        print("line ~281 newType is: {0}".format(newType))
                        myMsgs("        *Moving {0}: {1} to new: {2}".format(updatePath[3], lyr.dataSource, updatePath[0]))
                        reportFile.write("\n  Moving {0}: {1} to new: {2}".format(updatePath[3], lyr.dataSource, updatePath[0]))
                        lyr.replaceDataSource(newDSPath, newType, newDSName, False)
                        #myMsgs("    new datasource: {0}".format(lyr.dataSource))
                    myMsgs("         **the new data source: {0}".format(updateStatus))
                    cntFixed += 1
                    myMsgs("  Still broken? {0}".format(lyr.isBroken))
                  else:
                    myMsgs("not sure what it is, but can't process {0}".format(lyr.name))
  
                else:
                  myMsgs("  -Not Broken: {0}".format(str(lyr)))

            myMsgs("  Number of links fixed processed: {0}".format(cntFixed))
            myMsgs("  -{0} Review complete.".format(fullPath))
            reportFile.write("  -Number of links fixed processed: {0} \n".format(cntFixed))						
            reportFile.write("  -{0} Review complete. \n\n".format(fullPath))

            if cntFixed > 0:
              mxd.save()
              myMsgs("saved to {0}".format(fullPath))
              reportFile.write("saved to {0}".format(fullPath))
              cntTotalFixed += cntFixed
              cntFixed = 0
            """if cntFixed > 0:
							mxd.saveACopy(outMXDName, '10.1')
							myMsgs("saved to {0}".format(outMXDName))
							cntFixed = 0"""
            '''if arcpy.Exists(outMXDName):
                              outMXDName.()
                              myMsgs("saved 1")
                              else:
                                mxd.saveACopy(outMXDName, '10.1')
                                myMsgs("saved 2")'''
            del mxd
            cntFixed = 0
  else:
    myMsgs ("ERROR:  Required repair source list: [0] does not exit. \n".format(inFile))
  outText = ("\n\n ==========================================")
  outText += ("\n Number of MXD's processed: {0} \n".format(cntMXD))
  outText += (" Total Number of links it fixed, all mxds: {0} \n".format(cntTotalFixed) )

  myMsgs(" {0}".format(outText))

  reportFile.write(outText)
  # close the .txt file, 
  reportFile.close()
  myMsgs(  "File {0} is closed?  {1}".format(outfileTXT, str(reportFile.closed)))	

  myMsgs('!!! Success !!! ')

# End main function

if __name__ == '__main__':
  main()

