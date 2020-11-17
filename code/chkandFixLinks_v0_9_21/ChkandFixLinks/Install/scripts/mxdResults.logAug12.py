mxd = arcpy.mapping.MapDocument("CURRENT")
lyrList = arcpy.mapping.ListLayers(mxd)
lyr = lyrList[0]
lyr.dataSource
lyr.datasetName
lyr.isBroken
lyr = lyrList[1]

lyr.dataSource
lyr.datasetName
lyr.isBroken
lyr = lyrList[2]
lyr.dataSource
lyr.datasetName
lyr.isBroken
lyr = lyrList[3]
lyr.dataSource
lyr.datasetName
lyr.isBroken
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

inFile = "updateMultipleSourcePaths.csv
inFile = "updateMultipleSourcePaths.csv"
arcpy.env.workspace
theWorkspace = r"d:\_dataTest"
arcpy.env.workspace = theWorkspace
updatePath = findUpdatePath(inFile, lyr.dataSource)
import os
inFile = os.path.join(theWorkspace, inFile)
infile
inFile
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
  
updatePath = findUpdatePath(inFile, lyr.dataSource)
import csv
updatePath = findUpdatePath(inFile, lyr.dataSource)
from _miscUtils import *     # handles the myMsgs and time functions
from _gpdecorators import *

updatePath = findUpdatePath(inFile, lyr.dataSource)
lyr.isGroupLayer or ("Events" in lyr.name)
lyr.isServiceLayer
lyr.supports("DATASOURCE") and lyr.supports("DATASETNAME")
newDSPath, newDSName = os.path.split(updatePath[0])
sameType = updatePath[2] 
sameType
not updatePath[1]
updatePath[1] == "drive"
updateStatus = str(updatePath[0])
lyr in theTables
theTables = arcpy.mapping.ListTableViews(mxd)
lyr in theTables
lyr.isRasterLayer
sameType
cvrList = [r"\arc", r"\polygon", r"\region", r"\point", r"\tic" ]
lstExtDatatype = [[".shp", "SHAPEFILE_WORKSPACE" ], [".sde","SDE_Workspace"], [".mdb", "ACCESS_WORKSPACE" ], [".gdb", "FILEGDB_WORKSPACE"]]	
updatePath[0]
for extType in lstExtDatatype:
    if extType[0] in updatePath[0]:
        print(extType)
        
for extType in lstExtDatatype:
    if extType[0] in updatePath[0]:
        print(extType)
        newType = extType[1]
        
newType
lyr.dataSource
newDSPath
lyr.replaceDataSource(

lyr.datasetName
updatePath
newDSName
lyr.replaceDataSource(newDSPath, newType, newDSName, False)
lyr.dataSource
lyr.isBroken
lyr = lyrList[4]
lyr.dataSource
lyr.datasetName
lyr.isBroken
updatePath = findUpdatePath(inFile, lyr.dataSource)
newDSPath, newDSName = os.path.split(updatePath[0])
sameType = updatePath[2]  
sameType
for extType in lstExtDatatype:
    if extType[0] in lyr.dataSource:
        print(extType)
        newType = extType[1]
        
for extType in lstExtDatatype:
    if extType[0] in updatePath[0]:
        print(extType)
        newType = extType[1]
        
lyr.isBroken
lyr.dataSource
lyr.datasetName
newType
lyr.replaceDataSource(newDSPath, newType, newDSName, False)
lyr.isBroken
lyr.dataSource
lyr.datasetName
lyr = lyrList[5]
lyr.isBroken
lyr.dataSource
lyr.datasetName
not lyr.supports("DATASOURCE")
lyr.isGroupLayer or ("Events" in lyr.name)
lyr.isServiceLayer
lyr.supports("DATASOURCE") and lyr.supports("DATASETNAME")
updatePath = findUpdatePath(inFile, lyr.dataSource)
newDSPath, newDSName = os.path.split(updatePath[0])
newDSPath
newDSName
sameType = updatePath[2]  
sameType
not updatePath[1]
updatePath[1] == "drive"


updateStatus = str(updatePath[0]) 
lyr in theTables
lyr.isRasterLayer
for extType in lstExtDatatype:
    if extType[0] in updatePath[0]:
        print(extType)
        newType = extType[1]
        
for extType in lstExtDatatype:
    if extType[0] in updatePath[0]:
        print(extType)
        newType = extType[1]
        
newType
lyr.replaceDataSource(newDSPath, newType, newDSName, False)
lyr.isBroken
lyr.dataSource
newDSPath
'.sde' in lyr.dataSource
lyr.dataSource
lyr2 = lyrList[6]
lyr2.dataSource
'.sde' in lyr2.dataSource
updatePath[2]
updatePath[3]
lyr = lyrList[6]
lyr.isBroken
lyr.supports("DATASOURCE") and lyr.supports("DATASETNAME")
lyr.dataSource
lyr.datasetName
lyr.isServiceLayer
lyr.isRasterizingLayer
lyr.isRasterLayer
lyr.isNetworkAnalystLayer
lyr.isGroupLayer
lyr.isFeatureLayer
lyrList
for zz in lyrList:
    print(zz.isRasterizingLayer, zz.isFeatureLayer, zz.isBroken, zz.dataSource)
    
for zz in lyrList:
    print(zz.isRasterizingLayer, zz.isFeatureLayer, zz.isBroken, zz.dataSource)
    
for zz in lyrList:
    for .sde in zz:
        print(zz.isBroken, zz.datasetName, zz.dataSource)
        
for zz in lyrList:
    for ".sde" in zz:
        print(zz.isBroken, zz.datasetName, zz.dataSource)
        
lyr.dataSource
".sde" in lyr.dataSource
lyr.datasetName
lyr.name
lyr2 = lyrList[5]
lyr2.dataSource
lyr.workspacePath
lyr.dataSource
updatePath
newDSName
newDSPath
newType
lyr.dataSource
lyr.replaceDataSource(newDSPath, newType, newDSName, False)
lyr.dataSource
lyrList
lyr = lyrList[16]
lyr.dataSource
lyr.datasetName
zz = strip(lyr.datasetName, .)
zz = split(lyr.datasetName)
zz = os.split(lyr.datasetName)
zz = os.path.split(lyr.datasetName)
zz
zz = lyr.datasetName.rsplit
zz
zz = string.rsplit(lyr.datasetName)
zz = lyr.datasetName.rsplit(".")
zz
zz2 = lyr.datasetName.split(".")
zz2
zz2 = zz[2]
zz2
".sde" in lyr.dataSource
newDSName
zz
lyr.datasetName
lyr.dataSource
print(newDSPath, newType, newDSName)
mxd
lry
lry
lyr = lyrList[16]
lyr
lyr.dataSource
newDSPath
updatePath = findUpdatePath(inFile, lyr.dataSource)
newDSPath
newDSPath, newDSName = os.path.split(updatePath[0])
updatePath
lyr.dataSource
lyr.findAndReplaceWorkspacePath(lyr.dataSource, updatePath[0], False)
lyr.dataSource
mxd.replaceWorkspaces(lyr.dataSource, "SDE_WORKSPACE", updatePath[0], "FILEGDB_WORKSPACE", False)
mxd
mxd.replaceWorkspaces(lyr.dataSource, "SDE_WORKSPACE", updatePath[0], "FILEGDB_WORKSPACE", False)
lyr.dataSource
lyr.workspacePath
mxd.replaceWorkspaces(lyr.workspacePath, "SDE_WORKSPACE", updatePath[0], "FILEGDB_WORKSPACE", False)
lyr.dataSource
lyr = lyrList[17]
lyr.dataSource
updatePath
updatePath[0]
lyr.workspacePath
lyr.dataSource
lyr.datasetName
lyr.longName
lyr.name
lyr.supports
lyr.supports[0]
lyr.description
zzz = lyr.dataSource - lyr.datasetName
zzz = lyr.dataSource.rstrip(lyr.datasetName)
zzz
lyr.dataSource
lyr.datasetName
newDSPath
newDSName
updatePath = findUpdatePath(inFile, lyr.dataSource)
newDSPath, newDSName = os.path.split(updatePath[0])

newDSName
updatePath = findUpdatePath(inFile, lyr.dataSource)

updatePath[0]

