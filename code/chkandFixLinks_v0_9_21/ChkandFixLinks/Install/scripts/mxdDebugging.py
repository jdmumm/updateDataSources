import arcpy
import os
import csv
from _miscUtils import *     # handles the myMsgs and time functions
from _gpdecorators import *  # handles main for catching errors

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

#----------------------------------------------------------------------
#inFile = "\\dfg.alaska.local\gis\Anchorage\GISStaff\wc\RepairBrokenSrc20150815_1511.csv\\dfg.alaska.local\gis\Anchorage\GISStaff\wc\RepairBrokenSrc20150815_1511.csv\\dfg.alaska.local\gis\Anchorage\GISStaff\wc\RepairBrokenSrc20150815_1511.csv"
#theWorkspace = r"d:\_dataTest
#theWorkspace = r"\\dfg.alaska.local\GIS\Anchorage\GISStaff\wc\woolington"
#arcpy.env.workspace = theWorkspace
#inFile = os.path.join(theWorkspace, inFile)
inFile = r"\\dfg.alaska.local\gis\Anchorage\GISStaff\___gisStaffConnections\RepairBrokenSrcAug242015.csv"
#r"\\dfg.alaska.local\GIS\Anchorage\GISStaff\wc\RepairBrokenSrc20150815_1511.csv"
cvrList = [r"\arc", r"\polygon", r"\region", r"\point", r"\tic" ]
lstExtDatatype = [[".shp", "SHAPEFILE_WORKSPACE" ], [".sde","SDE_WORKSPACE"], 
                  [".mdb", "ACCESS_WORKSPACE" ], [".gdb", "FILEGDB_WORKSPACE"], 
                  ["cover", "ARCINFO_WORKSPACE"], [".sid", "RASTER_WORKSPACE"]]
mxd = arcpy.mapping.MapDocument("CURRENT")
dfs = arcpy.mapping.ListDataFrames(mxd)
lyrList = arcpy.mapping.ListLayers(mxd)
theTables = arcpy.mapping.ListTableViews(mxd)
lyr = lyrList[0]


dataSource = lyr.dataSource
if lyr.isServiceLayer:
  updatePath = findUpdatePath(inFile, dataSource, lyrType.strip().lower())
else:
  updatePath = findUpdatePath(inFile, dataSource, "")

newDSPath, newDSName = os.path.split(updatePath[0])
df = dfs[0]

sameType = updatePath[2] 
sameType



for lyr in lyrList:
  print(lyr.isBroken, lyr.dataSource)
#-------------

lyr = lyrList[0]
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

for cvr in cvrList:
  print(cvr)#checks to see if the source layer is a coverage...must handle different
  if cvr in lyr.dataSource:
    sourceIsCoverage = True
    break
  else:
    sourceIsCoverage = False
sourceIsCoverage

if cvr in lyr.dataSource:
  sourceIsCoverage = True
  
not updatePath[1]
updatePath[1] == "drive"
updateStatus = str(updatePath[0])

lyr in theTables
lyr.isRasterLayer

updatePath[0]
for extType in lstExtDatatype:
  if extType[0] in updatePath[0]:
    print(extType)
    newType = extType[1]

newType
lyr.isBroken
lyr.dataSource
lyr.datasetName

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
#> Match found: ['226', 'Sde', 'Fgdb', 'C:\\Users\\sktimp.DFG\\AppData\\Roaming\\ESRI\\Desktop10.0\\ArcCatalog\\DC2008 - sdewild@wc_dev1.sde\\sde_wc_dev1.SDEWILD.DWCMasters\\sde_wc_dev1.SDEWILD.DWCHunts', '\\\\DFGANCGISPROD2\\agsprod\\data\\wc\\Master_current.gdb\\DWCMasters\\DWCHunts']
newDSPath, newDSName = os.path.split(updatePath[0])
newDSPath
#'\\\\DFGANCGISPROD2\\agsprod\\data\\wc\\Master_current.gdb\\DWCMasters'
newDSName
#'DWCHunts'
sameType = updatePath[2]  
sameType
#False
not updatePath[1]
#False
updatePath[1] == "drive"
#False
updateStatus = str(updatePath[0]) 
lyr in theTables
#False
lyr.isRasterLayer
#False
for extType in lstExtDatatype:
  if extType[0] in updatePath[0]:
    print(extType)
    newType = extType[1]

#['.gdb', 'FILEGDB_WORKSPACE']
newType

#'FILEGDB_WORKSPACE'

for extType in lstExtDatatype:
  if extType[0] in updatePath[4]:
    print(extType)
    newType = extType[1]

lyr.replaceDataSource(newDSPath, newType, newDSName, False)
lyr.isBroken
#True
lyr.dataSource
#u'\\\\DFGANCGISPROD2\\agsprod\\data\\wc\\Master_current.gdb\\DWCMasters\\sde_wc_dev1.SDEWILD.DWCMasters\\DWCHunts'
newDSPath
#'\\\\DFGANCGISPROD2\\agsprod\\data\\wc\\Master_current.gdb\\DWCMasters'
'.sde' in lyr.dataSource
#False
lyr.dataSource
#u'\\\\DFGANCGISPROD2\\agsprod\\data\\wc\\Master_current.gdb\\DWCMasters\\sde_wc_dev1.SDEWILD.DWCMasters\\DWCHunts'

lyr2 = lyrList[6]
lyr2.dataSource
#u'C:\\Users\\sktimp.DFG\\AppData\\Roaming\\ESRI\\Desktop10.0\\ArcCatalog\\DC2008 - sdewild@wc_dev1.sde\\sde_wc_dev1.SDEWILD.DWCMasters\\sde_wc_dev1.SDEWILD.DWCHunts'
'.sde' in lyr2.dataSource
#True
updatePath[3]
#'Sde'
lyr2.isBroken
#True
lyr2.supports("DATASOURCE") and lyr.supports("DATASETNAME")

for zz in lyrList:
  if zz.supports("DATASOURCE"):
    print("{0}, {1}".format(zz.supports("WORKSPACEPATH"),zz.dataSource))
if 


for cvr in cvrList:
  if cvr in lyr.dataSource:
    myMsgs("yes")
    newDSPath = os.path.split(newDSPath)[0]
    newType = "ARCINFO_WORKSPACE"
    #newDSName = (newDSPath)[1] + "_" + newDSName
    
    
for xx in lyrList:    
  for extType in lstExtDatatype:
    if extType[0] in updatePath[0]:
      newType = extType[1] 
      print newType
      if extType[0] == '.gdb':
        newDSPath = newDSPath.split('.gdb', 1)[0] + '.gdb'
        print newDSPath
      break
    
    
cntMe = 0
for xx in lyrList:
  if xx.supports("SERVICEPROPERTIES"):
    print("lyr{0}: {1}".format(cntMe, xx.ServiceProperties))
    cntMe += 1
    
    
lyr.isRasterLayer
for extType in lstExtDatatype:
  if extType[0] in updatePath[0]:
    newType = extType[1] 
    if extType[0] == '.gdb':
      newDSPath = newDSPath.split('.gdb', 1)[0] + '.gdb'
    break    

  
lyr.replaceDataSource(newDSPath, newType, newDSName, False)
if not sameType:
  testOldTOC = updatePath[4].strip('\\')
  if lyr.name == testOldTOC:
    lyr.name = lyr.datasetName
    
if lyr.isServiceLayer:    
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
    reportFile.write("\n   ->sees this as service....{0} \n".format(lyr.dataSource))
    myMsgs("Still broken? {0}".format(lyr.isBroken))

if lyr2.isServiceLayer:    
  if lyr2.supports("SERVICEPROPERTIES"):
    cnt = 0
    for i, j in lyr2.serviceProperties.iteritems():
      if cnt == 2:
        myMsgs("   i and j: {0}  and {1}".format(str(i), str(j)))
        dataSource = str(j)
        pass #break
      else:
        cnt += 1 
    myMsgs("    ->sees this as service....using findAndReplaceWorkspacePath")
    updatePath = findUpdatePath(inFile, dataSource)
    
    lyr2.findAndReplaceWorkspacePath(lyr2.dataSource, updatePath, False)
    reportFile.write("\n   ->sees this as service....{0} \n".format(lyr2.dataSource))
    myMsgs("Still broken? {0}".format(lyr2.isBroken))


if lyr.isServiceLayer:    
  if lyr.supports("SERVICEPROPERTIES"):
    for spType, spName in lyr.serviceProperties.iteritems():
      myMsgs("   Service Properties: {0}: {1}".format(spType, spName ))
      if spType == "URL": 
        dataSource = str(spName)
        lyrType = ("service_{}".format(lyr.name))
        myMsgs("ds {0}, lt:{1}".format(dataSource, lyrType))
    myMsgs("    ->sees this as service....using findAndReplaceWorkspacePath")

    updatePath = findUpdatePath(inFile, dataSource, lyrType)
    newDSPath, newDSName = os.path.split(updatePath[0])
    #oldFullPath = os.path.join(dataSource, lyr.name)
    #lyr.findAndReplaceWorkspacePath(lyr.dataSource, updatePath, False)
    #reportFile.write("\n   ->sees this as service....{0} \n".format(lyr.dataSource))
    myMsgs("Still broken? {0}".format(lyr.isBroken))
    if ("service" in updatePath[3]) and ("service" in updatePath[1]):
      #oldLayerFile = os.path.join(newDSName, lyr.name)
      myMsgs("yep")
      insertLayer = arcpy.mapping.Layer(updatePath[0])
      arcpy.mapping.InsertLayer(df, lyr, insertLayer, "AFTER")
      arcpy.mapping.RemoveLayer(df, lyr)
      #arcpy.RefreshActiveView()
      #arcpy.RefreshTOC(mxd)
    #lyr.findAndReplaceWorkspacePath(lyr.dataSource, updatePath, False)
    #reportFile.write("\n   ->sees this as service....{0} \n".format(dataSource))
    myMsgs("Still broken? {0}".format(lyr.isBroken))
    


df = arcpy.mapping.ListDataFrames(mxd)[0]
mxd.activeView = data_frame.name
addLayer  = arcpy.mapping.Layer(r"\\dfg.alaska.local\gis\Anchorage\GISStaff\___gisStaffConnections\serviceLayers\dfg_public_base.lyr")
arcpy.mapping.AddLayer(data_frame, commonbase,"TOP")
arcpy.mapping.AddLayer(data_frame, commonbase,"AUTO_ARRANGE")


###

import arcpy
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
lyrList = arcpy.mapping.ListLayers(mxd)

# for display purposes, selecting 4th layer, just so not top or bottom)
lyr = lyrList[3]
lyr.isServiceLayer  #true

arcpy.mapping.RemoveLayer(df, lyr)

addLayer  = arcpy.mapping.Layer(r"\\gisserver\serviceLayers\dfg_public_base.lyr")
arcpy.mapping.AddLayer(df, addLayer)
lyrList = arcpy.mapping.ListLayers(mxd)
theTables = arcpy.mapping.ListTableViews(mxd)
lyr = lyrList[0]


insertLayer = arcpy.mapping.Layer(updatePath[0])


for lyr in lyrList:
  if lyr.isBroken:
    if not lyr.supports("DATASOURCE"):
      myMsgs("  -> Broken {0}: does not support DATASOURCE".format(lyr.name))
    else:
      myMsgs("  -Broken: {0}".format(lyr.dataSource))
    #myMsgs("layer is Group {0} or ServiceLayer {1}".format(lyr.isGroupLayer, lyr.isServiceLayer))
    if (lyr.isGroupLayer or ("Events" in lyr.name)) and (not lyr.isServiceLayer): # Groups and Event FC skipped
      myMsgs("    ...skipping group or event: {0}".format(lyr.name))
      pass
    elif lyr.isServiceLayer:
      if lyr.supports("SERVICEPROPERTIES"):
        myMsgs("is service")
        cnt = 0
        for i, j in lyr.serviceProperties.iteritems():
          if cnt == 2:
            myMsgs("   i and j: {0}  and {1}".format(str(i), str(j)))
            dataSource = str(j)
            pass #break
          else:
            cnt += 1 
        myMsgs("    ->sees this as service....using findAndReplaceWorkspacePath")





def printInputs(x, y, z):
  if z:
    print("z")
  else:
    print("xy only")
    
    
    
with open(inFile) as inFix:
  reader = csv.reader(inFix)
  for row in reader:
    if serviceLayer:
      if (row[3] in searchOldPath) and serviceLayer in row[1].strip().lower():
        myMsgs('     > Match found: {}'.format(row))
        rtnNewPath = row[4]
        rtnNewType = row[2]
        rtnSameTypeTF = ( row[1].strip().lower() == row[2].strip().lower() )
        rtnOldType = row[1]
        rtnOldPath = row[3]
        break
    elif row[3] in searchOldPath:
      myMsgs('     > Match found: {}'.format(row))
      rtnNewPath = row[4]
      rtnNewType = row[2]
      rtnSameTypeTF = ( row[1].strip().lower() == row[2].strip().lower() )
      rtnOldType = row[1]
      rtnOldPath = row[3]
      break
    else:
      rtnNewPath = "no match"
      rtnNewType = False
      rtnSameTypeTF = False
      rtnOldType = row[1]
      rtnOldPath = row[3]
return(rtnNewPath, rtnNewType, rtnSameTypeTF, rtnOldType, rtnOldPath)



import arcpy
mxd = arcpy.mapping.MapDocument("CURRENT")
dfs = arcpy.mapping.ListDataFrames(mxd)
lyrList = arcpy.mapping.ListLayers(mxd)
lyr = lyrList[0]
lyr.isBroken
lyr.dataSource
lyr.name
lyr.isBroken
# manually fix the source now
lyr.dataSource
lyr.name
lyr.name = lyr.datasetName
lyr.name

for lyr in lyrList:
  if lyr.supports("WORKSPACEPATH"):
    # logfile.write("The datasetName before replacement is " + lyr.datasetName + '\n')
    # logfile.write("The old connection string before replacement is " + lyr.workspacePath + '\n')
    if lyr.supports("DATASOURCE"):
      if lyr.supports("SERVICEPROPERTIES"):
        print("The layer name in mxd in Prod is " + lyr.name)
        serverVersion = lyr.serviceProperties
        user = str(servProp.get('UserName', 'N/A'))
        serverID = str(servProp.get('Server', 'N/A'))
        serverInstance = str(servProp.get('Service', 'N/A'))
        serverVersion = str(servProp.get('Version', 'N/A')) 
        #print("serviceProps: {0}".format(servProp))
        print("user: {0}".format(user))
        print("serverID: {0}".format(serverID))
        print("serverInstance: {0}".format(serverInstance))
        print("serverVersion: {0}".format(serverVersion))
        



mxd = arcpy.mapping.MapDocument("CURRENT")

lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:  
  if lyr.serviceProperties["ServiceType"] == "SDE":  
    for k, v in lyr.serviceProperties.iteritems():  
      print ("Property: {:<30}Value:{}".format(k,v))



#for 10.3.x      
for lyr in arcpy.mapping.ListLayers(mxd):  
  if lyr.supports("SERVICEPROPERTIES"):  
    if lyr.serviceProperties["ServiceType"] == "SDE":  
      for k, v in lyr.serviceProperties.iteritems():  
        print "Property: {:<30}Value:{}".format(k,v)  
        
        
        
        
        
        
        

for spType, spName in lyr.serviceProperties.iteritems():
  myMsgs("   Service Properties: {0}: {1}".format(spType, spName ))
  if spType == "URL": 
    dataSource = str(spName)
    lyrType = ("service_{}".format(lyr.name))
    break
myMsgs("    ->this ia a service....using add and remove layer")
  
  
for cvr in cvrList:   #checks to see if the source layer is a coverage...must handle different
  if cvr in lyr.dataSource:
    sourceIsCoverage = True
    break
  else:
    sourceIsCoverage = False




newType = updatePath[1] 
if sourceIsCoverage and sameType:
  newDSPath = os.path.split(newDSPath)[0]
  newType = "ARCINFO_WORKSPACE"
for extType in lstExtDatatype:
  if extType[0] in updatePath[0]:
    newType = extType[1]
    if extType[0] == '.gdb':
      newDSPath = newDSPath.split('.gdb', 1)[0] + '.gdb'
    break
myMsgs("        *Moving {0}: {1} to new: {2}".format(updatePath[3], lyr.dataSource, updatePath[0]))
print("line 272 newType is: {0}".format(newType))

\\dfg.alaska.local\gis\Anchorage\GISStaff\___gisStaffConnections\_sde\_prodDC - sdedfg@wc_mgmt_master.sde\sde_wc_mgmt_master.SDEWILD.DWCMasters\sde_wc_mgmt_master.SDEWILD.UCU_poly


#SDE
  xxx = updatePath[0].split('.sde')[0] + ".sde"
>>> xxx
'\\\\dfg.alaska.local\\gis\\Anchorage\\GISStaff\\___gisStaffConnections\\_sde\\_prodDC - sdedfg@wc_mgmt_master.sde'
>>> lyr.replaceDataSource(xxx, newType, newDSName, False)
>>> lyr.isBroken
False
>>> arcpy.RefreshTOC
<function RefreshTOC at 0x1C379AB0>
>>> arcpy.RefreshTOC()



