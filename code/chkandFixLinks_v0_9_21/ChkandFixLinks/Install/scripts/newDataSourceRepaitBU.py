"""
---------------------------------------------------------------------------
Tool: Fix "broken source links" from input .csv 
Script:  DataSourceRepair.py
Created on: May 11, 2015 
   last modification May 13, 2015
---------------------------------------------------------------------------
 Author: Rebecca Strauch - ADFG-DWC-GIS
 Purpose: Fixes broken data source link(s) in MXDs in a file, or one at a time

   NOTE: run from the machine and user that will use the mxd
---------------------------------------------------------------------------
 Description: 
   This script will loop thru all the MXDs within a folder, and the broken
   links and attempt to repair them based on the input comma delimited file
   with the following fields (header columns are suggested...):
        column 1:  contains layer, shape, or sde from ListUniqueBrokenLink
            header: type
        Column 2:   contains the name in the TOC from ListUniqueBrokenLink
            header:  TOCRef
        column 3: contains the full path of the broken link
            header: FullPath   
        column 4   contains the full new path you want = col2 if no change
            header:  NewPath
   uses the inFile to replace the full path, then saves it to a new mxd 
   in 10.1/10.2 format with _fix appendd to the name

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
	cnt = 0
	returnNewPath = searchOldPath # for those that can't be found
	with open(inFile) as inFix:
		reader = csv.reader(inFix)
		for row in reader:
			if row[3] in searchOldPath:
				print('Found: {}'.format(row))
				cnt += 1
				returnNewPath = row[4]
				returnNewType = row[2]  #(row [1] != row[2])
				print("returnNewPath: {0}".format(returnNewPath))	
				print("returnNewType: {0}".format(returnNewType))	
				break
			else:
				#print("no match")
				returnNewPath = "no match"
				returnNewType = False
		#print("searching for: {0}".format(searchOldPath))	
		#print("returnNewPath: {0}".format(returnNewPath))	
		#print("returnNewType: {0}".format(returnNewType))	
	return(returnNewPath, returnNewType)



# catch_errors decorator must preceed a function using the @ notation.
@catch_errors
def main():
	"""
	Main function to add update source path
	"""

	# Script arguments...    
	""" If running as standalone, hardcode theWorkspace and inFile  """
	theWorkspace = arcpy.GetParameterAsText(0)
	if not theWorkspace:
		theWorkspace = r"d:\_dataTest"
	theWorkspace = r"d:\_dataTest"
	arcpy.env.workspace = theWorkspace
	arcpy.env.overwriteOutput = True
	outWorkspace = os.path.join(theWorkspace, "_repair")

	inFile = arcpy.GetParameterAsText(1)
	if not inFile:
		inFile = "updateMultipleSourcePaths.csv"
	#inFile = "FixSource4.csv"
	#inFile = os.path.join(theWorkspace, inFile) + ".csv"
	# opens the infile.csv, read only; then creates tuple of inFile
	#f = open(inFile, "r")    
	#update_list = [tuple(line.strip().split(",") for line in f)]


	mxd = None
	outMXDName = "none"
	newPath = []
	# makes sure the .csv file exists
	if arcpy.Exists(inFile):
		myMsgs ("Repair source list: " + inFile)
		# walks thru the workspace to create list of files 
		for root, dirs, files in os.walk(theWorkspace): 
			if root == outWorkspace:
				print("heh now")
				pass
			# creates list of .mxd's and works thru them
			mxdList = arcpy.ListFiles("*.mxd")
			for fileName in mxdList:
				fullPath = os.path.join(root, fileName)             
				mxd = arcpy.mapping.MapDocument(fullPath)
				myMsgs ("*** Processing mxd: " + fullPath)
				#mxd.findAndReplaceWorkspacePaths("v:\\",  "\\\\dfg.alaska.local\\gis\\Anchorage\\gisshare\\", validate=False)
				#mxd.findAndReplaceWorkspacePaths("t:\\",  "\\\\dfg.alaska.local\\gis\\Anchorage\\GISStaff\\", validate=False)
				#mxd.findAndReplaceWorkspacePaths("u:\\",  "\\\\dfg.alaska.local\\gis\\Anchorage\\GISStaff\\", validate=False)
				# New output mxd....
				basename, extension = os.path.splitext(fileName)
				outMXDName = os.path.join(outWorkspace, (str(basename) + "_fix.mxd"))
				# create list of the tables since they are handle differently
				theTables = arcpy.mapping.ListTableViews(mxd)
				# Loops thru layers, checks for broken links and tries to repai
				lyrList = arcpy.mapping.ListLayers(mxd)
				for lyr in lyrList:
					if lyr.isBroken:
						if lyr.isGroupLayer or ("Events" in lyr.name):
							print("...skipping group or event")
							break
						#print(lyr.isServiceLayer)
						if lyr.isServiceLayer:
							if lyr.supports("SERVICEPROPERTIES"):
								cnt = 0
								for i, j in lyr.serviceProperties.iteritems():
									if cnt == 2:
										dataSource = str(j)
										break
									else:
										cnt += 1 
								print("sees this as service....using findAndReplsWorkspacePath")
								newPath = findUpdatePath(inFile, dataSource)
								lyr.findAndReplaceWorkspacePath(lyr.dataSource, newPath, False)
							else:
								print("--> a service layer but no SERVICE PROPOERTIES")
						else:
							print(lyr.dataSource)
							newPath = findUpdatePath(inFile, lyr.dataSource)
							newDSPath, newDSName = os.path.split(newPath[0])
							print("..newDSPAth " + newDSPath)
							print("..newDSName " + newDSName)
							sameType = newPath[1]
							print("    same type? " + str(sameType))
							cvrList = [r"\arc", r"\polygon", r"\region", r"\point", r"\tic" ]
							#print newDSPath
							if newPath == "no match":
								print("...no match to: "  + lyr.dataSource)
								newPath[0] = "not found"
								break
							elif lyr.supports("dataSource") and lyr.supports("datasetName"):
								if lyr in theTables:
									print("thinks its a table....using findAndReplsWorkspacePath")
									lyr.findAndReplaceWorkspacePath(lyr.dataSource, newPath, False)                    
								elif lyr.isRasterLayer:
									print("thinks its a raster....using findAndReplsWorkspacePath")
									#lyr.replaceDataSource(newPath, "RASTER_WORKSPACE", lyr.datasetName, False)
									lyr.findAndReplaceWorkspacePath(lyr.dataSource, newPath, False)
								elif  lyr.supports("dataSource") and lyr.supports("datasetName"):
									if not sameType and newPath[1] == "gdb":
										print("..................moving to fgdb")
										lyr.replaceDataSource(newDSPath, "FILEGDB_WORKSPACE", newDSName, False)           
									elif r".shp" in lyr.dataSource:
										print("thinks its a shape")
										lyr.replaceDataSource(newDSPath, "SHAPEFILE_WORKSPACE", lyr.datasetName, False)
									elif r".sde" in lyr.dataSource:
										print("thinks its a sde")
										lyr.replaceDataSource(newDSPath, "SDE_Workspace", lyr.datasetName, False)
									elif r".mdb" in lyr.dataSource:
										print("thinks its a pgdb")
										lyr.replaceDataSource(newDSPath, "ACCESS_WORKSPACE", lyr.datasetName, False)
									elif r".gdb" in lyr.dataSource:
										print("thinks its a fgdb")

										lyr.replaceDataSource(newDSPath, "FILEGDB_WORKSPACE", lyr.datasetName, False)
									elif sameType:
										for cvr in cvrList:
											if cvr in lyr.dataSource:
												print("to WS sametype is True")
												lyr.replaceDataSource(newDSPath, "ARCINFO_WORKSPACE", newDSName, False)
									elif not sameType:
										for cvr in cvrList:

											lyr.replaceDataSource(newDSPath, "FILEGDB_WORKSPACE", newDSName, False)
																																
																																								
							"""else:
                                newPath[0] = "not found" """
							print("   **** the new data source: "  +  newPath[0])
							print("")

				print(outMXDName)
				#mxd.saveACopy(outMXDName, '10.1')
			if arcpy.Exists(outMXDName):
																
																				
					outMXDName.save()
				else:
          mxd.saveACopy(outMXDName, '10.1')
				del mxd
	else:
		myMsgs ("Repair source list: " + inFile + " does not exit.")

	myMsgs('!!! Success !!! ')

# End main function

if __name__ == '__main__':
	main()

