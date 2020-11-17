"""
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
   last modification: August 10, 2015

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
"""
# Import modules
import arcpy
import os
import csv
from _miscUtils import *     # handles the myMsgs and time functions
from _gpdecorators import *  # handles main for catching errors

#----------------------------------------------------------------------

#----------------------------------------------------------------------
def findUpdatePath(inFile, searchOldPath):
  #rtnNewPath = searchOldPath # for those that can't be found
  with open(inFile) as inFix:
    reader = csv.reader(inFix)
    for row in reader:
      if row[3] in searchOldPath:
        myMsgs('     > Match found: {}'.format(row))
        rtnNewPath = row[4]
        rtnNewType = row[2]
        rtnSameTypeTF = (row[1] == row[2])
        rtnOldType = row[1]
        #print("returnNewPath: {0}".format(returnNewPath))	
        #print("returnNewType: {0}".format(returnNewType))	
        break
      else:
        #print("no match")
        rtnNewPath = "no match"
        rtnNewType = False
        rtnSameTypeTF = False
        rtnOldType = row[1]
  return(rtnNewPath, rtnNewType, rtnSameTypeTF, rtnOldType)



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

  outWorkspace = arcpy.GetParameterAsText(2)
  if not outWorkspace:
    outWorkspace = os.path.join(theWorkspace, "_repair")
  if not os.path.isdir(outWorkspace):  
    os.makedirs(outWorkspace)
    myMsgs("created new directory {0} \n".format(outWorkspace))

  # Create new output file names, tagged with YYYYMMDD_HHMM
  outFile = "FixedReport"
  fileDateTime = curFileDateTime()
  currentDate = curDate()
  outfileTXT = os.path.join(theWorkspace, outFile) + fileDateTime + ".txt" 
  #outFileCSV = os.path.join(theWorkspace, outFile) + fileDateTime + ".csv"
  #outFileXLS = os.path.join(theWorkspace, outFile) + fileDateTime + ".xls"
  myMsgs (outFile)
  reportFile = open(outfileTXT, 'w')
  myMsgs(  "File {0} is open?  {1}".format(str(reportFile), str(not reportFile.closed)))
  outText = "Report for what it THINKS it repaired in {0}, on {1} \n ".format(theWorkspace, currentDate)
  outText += "  Includes coverages (pts, poly, arc, anno), shapes, and FGDB data." + '\n'
  outText += "-----------------------------------------------------" + '\n'   
  reportFile.write(outText)	

  mxd = None
  outMXDName = "none"
  updatePath = []
  cvrList = [r"\arc", r"\polygon", r"\region", r"\point", r"\tic" ]
  lstExtDatatype = [[".shp", "SHAPEFILE_WORKSPACE" ], [".sde","SDE_Workspace"], [".mdb", "ACCESS_WORKSPACE" ], [".gdb", "FILEGDB_WORKSPACE"]]	
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
            reportFile.write("\nReviewing MXD: {0} \n".format(fullPath))
            mxd = arcpy.mapping.MapDocument(fullPath)
            cntMXD += 1
            cntFixed = 0
            basename, extension = os.path.splitext(fileName)
            # New output mxd name....
            outMXDName = os.path.join(outWorkspace, (str(basename) + ".mxd")) #"_fix.mxd"))
            # create list of the tables since they are handle differently
            theTables = arcpy.mapping.ListTableViews(mxd)
            # Loops thru layers, checks for broken links and tries to repair
            lyrList = arcpy.mapping.ListLayers(mxd)
            for lyr in lyrList:
              if lyr.isBroken:
                if not lyr.supports("DATASOURCE"):
                  continue
                myMsgs("  -Broken: {0}".format(lyr.dataSource))
                #myMsgs("layer is Group {0} or ServiceLayer {1}".format(lyr.isGroupLayer, lyr.isServiceLayer))
                if lyr.isGroupLayer or ("Events" in lyr.name): # Groups and Event FC skipped
                  myMsgs("    ...skipping group or event: {0}".format(lry.name))
                  reportFile.write("    ...skipping group or event: {0} \n".format(lry.name))
                  pass #break
                elif lyr.isServiceLayer:    # services might have to be handle differently
                  if lyr.supports("SERVICEPROPERTIES"):
                    cnt = 0
                    for i, j in lyr.serviceProperties.iteritems():
                      if cnt == 2:
                        myMsgs("   i and j: {0}  and {1}".format(str(i), str(j)))
                        dataSource = str(j)
                        pass #break
                      else:
                        cnt += 1 
                    myMsgs("    ->sees this as service....using findAndReplaceWorkspacePath")
                    updatePath = findUpdatePath(inFile, dataSource)
                    lyr.findAndReplaceWorkspacePath(lyr.dataSource, updatePath, False)
                    reportFile.write("    ->sees this as service....{0} \n".format(lyr.dataSource))
                  else:
                    myMsgs("   --> a service layer but no SERVICE PROPOERTIES")
                elif lyr.supports("DATASOURCE") and lyr.supports("DATASETNAME"):   
                  # not a group, event or what it thinks is a service
                  updatePath = findUpdatePath(inFile, lyr.dataSource)
                  newDSPath, newDSName = os.path.split(updatePath[0])
                  #myMsgs("       returned from FindUpdatePath: {0}".format(updatePath))
                  sameType = updatePath[2]  
                  #myMsgs("         sameType? {0}".format(sameType))
                  # updatePath[1] is False if there wasn't a match
                  #  so "not update[1]" means no match was found, and moves to next layer								
                  if not updatePath[1]:    # if no match was found
                    myMsgs("     !! no match to: "  + lyr.dataSource)
                    updateStatus = "no match, not changed"  # used for message only
                    pass
                  else: #if lyr.supports("DATASOURCE") and lyr.supports("DATASETNAME"):
                    updateStatus = str(updatePath[0])   # used for message only
                    if lyr in theTables:
                      #myMsgs("  thinks its a table....using findAndReplsWorkspacePath")
                      myMsgs("        *Table: moving {0} to {1}".format(updatePath[3], updatePath[1]))
                      reportFile.write("        *Table: moving {0} to {1} \n".format(updatePath[3], updatePath[1]))
                      #lyr.findAndReplaceWorkspacePath(lyr.dataSource, updatePath, False)                    
                      lyr.findAndReplaceWorkspacePath(lyr.dataSource, updatePath, False)                    
                    elif lyr.isRasterLayer:
                      #myMsgs("  thinks its a raster....using findAndReplsWorkspacePath")
                      myMsgs("        *Raster: moving {0} to {1}".format(updatePath[3], updatePath[1]))
                      reportFile.write("        *Raster: moving {0} to {1} \n".format(updatePath[3], updatePath[1]))
                      #lyr.replaceDataSource(updatePath, "RASTER_WORKSPACE", lyr.datasetName, False)
                      lyr.findAndReplaceWorkspacePath(lyr.dataSource, updatePath, False)
                      #elif  lyr.supports("dataSource") and lyr.supports("datasetName"):

                    else:
                      if sameType:
                        for extType in lstExtDatatype:
                          if extType[0] in lyr.dataSource:
                            newType = extType[1]
                      else:
                        for extType in lstExtDatatype:
                          if extType[0] in updatePath[0]:
                            newType = extType[1]
                      myMsgs("        *{0}: moving {1} to {2}".format(extType[0], updatePath[3], updatePath[1]))
                      reportFile.write("        *Shape: moving {0} to {1} \n".format(updatePath[3], updatePath[1]))
                      lyr.replaceDataSource(newDSPath, newType, lyr.datasetName, False)																				

                    '''#myMsgs("  same type....using findAndReplsWorkspacePath")
										myMsgs("        *Same Type: moving {0} to {1}".format(updatePath[3], updatePath[1]))
										reportFile.write("        *Same Type: moving {0} to {1} \n".format(updatePath[3], updatePath[1]))
										#lyr.findAndReplaceWorkspacePath(lyr.dataSource, updatePath, False)
										lyr.replaceDataSource(newDSPath, newType, lyr.datasetName, False)

										elif not sameType: # and (updatePath[1] == "Fgdb" or updatePath[1] == "fgdb"):
											for extType in lstExtDatatype:
												if extType[0] in updatePath[0]:
													newType = extType[1]
													myMsgs("        *{0}: moving {1} to {2}".format(extType[0], updatePath[3], updatePath[1]))
													reportFile.write("        *Shape: moving {0} to {1} \n".format(updatePath[3], updatePath[1]))
													lyr.replaceDataSource(newDSPath, newType, lyr.datasetName, False)																								
											if r".shp" in newDSPath: #lyr.dataSource:
												#print("thinks its a shape")
												myMsgs("        *Shape: moving {0} to {1}".format(updatePath[3], updatePath[1]))
												reportFile.write("        *Shape: moving {0} to {1} \n".format(updatePath[3], updatePath[1]))
												lyr.replaceDataSource(newDSPath, "SHAPEFILE_WORKSPACE", lyr.datasetName, False)											
											elif r".sde" in newDSPath: #lyr.dataSource:
												#print("thinks its a sde")
												#myMsgs("      ... was a <sde>, now a {0}".format(str(lyr.dataSource)))
												myMsgs("        *SDE: moving {0} to {1}".format(updatePath[3], updatePath[1]))
												reportFile.write("        *SDE: moving {0} to {1} \n".format(updatePath[3], updatePath[1]))
												lyr.replaceDataSource(newDSPath, "SDE_Workspace", lyr.datasetName, False)
											elif r".mdb" in newDSPath: #lyr.dataSource:
												#print("thinks its a pgdb")
												#myMsgs("      ... was a <pgdb>, now a {0}".format(str(lyr.dataSource)))
												myMsgs("      ...PGDB: moving {0} to {1}".format(updatePath[3], updatePath[1]))
												reportFile.write("      ...PGDB: moving {0} to {1} \n".format(updatePath[3], updatePath[1]))
												lyr.replaceDataSource(newDSPath, "ACCESS_WORKSPACE", lyr.datasetName, False)	
											elif r".gdb" in newDSPath: #lyr.dataSource:
												#print("thinks its a pgdb")
												#myMsgs("      ... was a <pgdb>, now a {0}".format(str(lyr.dataSource)))
												myMsgs("      ...PGDB: moving {0} to {1}".format(updatePath[3], updatePath[1]))
												reportFile.write("      ...PGDB: moving {0} to {1} \n".format(updatePath[3], updatePath[1]))
												lyr.replaceDataSource(newDSPath, "FILEGDB_WORKSPACE", lyr.datasetName, False)												
											else:
												for cvr in cvrList:
													if cvr in lyr.dataSource:
														#print("to WS sametype is True")
														#myMsgs("     ...cvr to fgdb: {0}".format(str(lyr.dataSource)))
														myMsgs("        *Cover: moving {0} to {1}".format(updatePath[3], updatePath[1]))
														reportFile.write("        *Cover: moving {0} to {1} \n".format(updatePath[3], updatePath[1]))
														lyr.replaceDataSource(newDSPath, "ARCINFO_WORKSPACE", newDSName, False)'''

                  myMsgs("         **the new data source: {0}".format(updateStatus))
                  #myMsgs("")
                  cntFixed += 1
                else:
                  myMsgs("not sure what it is, but can't process {0}".format(lyr.name))

              else:
                myMsgs("  -Not Broken: {0}".format(str(lyr)))

            myMsgs("-{0} Review complete.".format(fullPath))
            myMsgs(" Number of links fixed processed: {0}".format(cntFixed))
            reportFile.write("-{0} Review complete. \n".format(fullPath))
            reportFile.write(" Number of links fixed processed: {0} \n".format(cntFixed))						

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
  outText = ("\n ==========================================")
  outText += ("\n Number of MXD's processed: {0} \n".format(cntMXD))
  outText += (" Total Number of links it fixed, all mxds: {0} \n".format(cntTotalFixed) )

  myMsgs(" {0}".format(outText))

  reportFile.write(outText)
  # close the .txt file, 
  reportFile.close()
  myMsgs(  "File {0} is closed?  {1}".format(str(reportFile), str(reportFile.closed)))	

  myMsgs('!!! Success !!! ')

# End main function

if __name__ == '__main__':
  main()

