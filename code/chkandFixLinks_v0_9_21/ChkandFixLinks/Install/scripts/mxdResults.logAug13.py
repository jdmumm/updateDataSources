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
        rtnOldPath = row[3]
        #print("returnNewPath: {0}".format(returnNewPath))	
        #print("returnNewType: {0}".format(returnNewType))	
        break
      else:
        #print("no match")
        rtnNewPath = "no match"
        rtnNewType = False
        rtnSameTypeTF = False
        rtnOldType = row[1]
        rtnOldPath = row[3]
  return(rtnNewPath, rtnNewType, rtnSameTypeTF, rtnOldType, rtnOldPath)

inFile = "updateMultipleSourcePaths.csv"
theWorkspace = r"d:\_dataTest"
arcpy.env.workspace = theWorkspace
inFile = os.path.join(theWorkspace, inFile)
cvrList = [r"\arc", r"\polygon", r"\region", r"\point", r"\tic" ]
lstExtDatatype = [[".shp", "SHAPEFILE_WORKSPACE" ], [".sde","SDE_Workspace"], [".mdb", "ACCESS_WORKSPACE" ], [".gdb", "FILEGDB_WORKSPACE"]]	
mxd = arcpy.mapping.MapDocument("CURRENT")
lyrList = arcpy.mapping.ListLayers(mxd)
theTables = arcpy.mapping.ListTableViews(mxd)

for lyr in lyrList:
  print(lyr.isBroken, lyr.dataSource)
  
lyr = lyrList[7]
lyr.dataSource
lyr.datasetName
lyr.isBroken
updatePath = findUpdatePath(inFile, lyr.dataSource)
newDSPath, newDSName = os.path.split(updatePath[0])
lyr.isGroupLayer or ("Events" in lyr.name)
lyr.isServiceLayer
lyr.supports("DATASOURCE") and lyr.supports("DATASETNAME")
sameType = updatePath[2] 
sameType
lyr in theTables
lyr.isRasterLayer
updatePath[0]
newDSPath
newDSName
lyr.replaceDataSource(newDSPath, newType, newDSName, False)
for extType in lstExtDatatype:
  if extType[0] in updatePath[0]:
    print(extType)
    newType = extType[1]
    
newType
lyr.replaceDataSource(newDSPath, newType, newDSName, False)
lyr.dataSource
lyr - lyrList[1]
lyr = lyrList[1]
lyr.dataSource
lyr.isBroken
lyr = lyrList[5]
lyr.dataSource
lyr.isBroken

