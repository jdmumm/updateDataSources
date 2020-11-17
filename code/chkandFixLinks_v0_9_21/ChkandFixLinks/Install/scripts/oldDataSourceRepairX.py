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

 Updates:

---------------------------------------------------------------------------
"""
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
            oldPath = row[3]
            newPath = row[4]
            thePaths = (oldPath, newPath)
            lstFromCSV.append(thePaths)
            myMsgs('show old path: {}'.format(row[3]))
            myMsgs('     show new path: {}'.format(row[4]))
            #cnt += 1
    return(lstFromCSV)

# catch_errors decorator must preceed a function using the @ notation.
@catch_errors
def main():
    """
    Main function to add optionally bulk repair, and then create 
    list of layers with broken source path
    """
    myMsgs("hello world")

    # Script arguments...    
    """ If running as standalone, hardcode theWorkspace and inFile  """
    theWorkspace = arcpy.GetParameterAsText(0)
    if not theWorkspace:
        theWorkspace = r"d:\_dataTest"
    arcpy.env.workspace = theWorkspace
    
    inFile = arcpy.GetParameterAsText(1)
    if not inFile:
        inFile = "updateMultipleSourcePaths"
    #inFile = "updateMultipleSourcePaths"
    inFile = os.path.join(theWorkspace, inFile) + ".csv"
    mxd = None
    outMXDName = "none"
    # makes sure the .csv file exists
    if arcpy.Exists(inFile):
        myMsgs ("Repair source list: " + inFile)
        # walks thru the workspace to create list of files 
        for root, dirs, files in os.walk(theWorkspace):  
            for fileName in files:
                fullPath = os.path.join(root, fileName)
                #myMsgs ("Full path: " + fullPath)
                basename, extension = os.path.splitext(fileName)
                # checks to see if file is and mxd
                if extension == ".mxd":
                    myMsgs ( "*** Processing: " + fullPath + " ***")
                    mxd = arcpy.mapping.MapDocument(fullPath)
                    # sets up output mxd with _fix appended to name
                    outMXDName = os.path.join(theWorkspace, (str(basename) + "_fix.mxd"))
                    myMsgs ("the output mxd: " + outMXDName)
                    # creates list of broken links in mxd for looping
                    brknMXD = arcpy.mapping.ListBrokenDataSources(mxd)
                    # create list of the tables since they are handle differently
                    theTables = arcpy.mapping.ListTableViews(mxd)
                    # Loops thru broken links and fixes links
                    for brknItem in brknMXD:
                        if brknItem in theTables:
                            myMsgs("table: " + str(brknItem.name))
                        elif brknItem.isGroupLayer:
                            myMsgs("group or service: " + str(brknItem))
                        elif brknItem.supports("dataSource"):
                            myMsgs ("layer: " + str(brknItem))
                            lyrSource = brknItem.dataSource.strip()
                            lyrTOCname = (brknItem.name).strip()
                            f = open(inFile, "r")
                            for rec in f:
                                col = rec.split(",")
                                # only processes it if there is a newPath in column 4
                                if len(col) < 5: 
                                    myMsgs("skip")
                                    next
                                else:
                                    recno   = (col[0]).strip()
                                    theType = (col[1]).strip()
                                    TOCname = (col[2]).strip()
                                    oldPath = (col[3]).strip()
                                    newPath = (col[4]).strip()
                                    #myMsgs(newPath)                                
                                #theType = (col[0]).strip()
                                #oldPath = (col[1]).strip()
                                #TOCname =  (col[2]).strip()
                                #theNewPath = (col[3]).strip()
                                #oldPathQ = 'r"' + (col[1]).strip() + '"'
                                #TOCnameQ =  'r"' + (col[2]).strip() + '"'
                                #theNewPathQ = 'r"' + (col[3]).strip() + '"'                                
                                #myMsgs("the new Path with quotes: " + theNewPath)
                                
                                #myMsgs ("       layer old path: " + oldPath)
                                #myMsgs ("         layer source: " + lyrSource)
                                #myMsgs ("   layer old TOC name: " + TOCname)
                                #myMsgs ("         layer in TOC: " + lyrTOCname)
                                c1 =  (oldPath == lyrSource)
                                c2 =  (TOCname == lyrTOCname)
                                c3 =  (oldPathQ == lyrSource)
                                
                                myMsgs = c1c2c3
                                #myMsgs ("new path:  " + theNewPath)
                                if oldPath == lyrSource and TOCname == lyrTOCname:
                                    print (oldPath == lyrSource)
                                    print (TOCname == lyrTOCname)
                                    myMsgs ("layer in TOC: " + lyrTOCname)
                                    myMsgs ("layer old path: " + oldPath)
                                    myMsgs ("new path:  " + theNewPath)
                                    if ".shp" in brknItem.dataSource:
                                        myMsgs ("layer type: " + theType)
                                        brknItem.replaceDataSource(oldPath, "SHAPEFILE_WORKSPACE", theNewPathQ, False)
                                    elif ".sde" in brknItem.dataSource:
                                        myMsgs ("layer type: " + theType)
                                        brknItem.replaceDataSource(oldPath, "SDE_WORKSPACE", theNewPathQ, False)                                    
                                    else:
                                        brknItem.findAndReplaceWorkspacePath(oldPath, theNewPathQ, False)
                                    myMsgs(" successfully updated " + TOCname)
                                    mxd.save()
                                    
                                    lyrNewSource = brknItem.dataSource.strip()
                                    myMsgs ("new source: " + lyrNewSource )
                                    #mxd.save()
                                    #brknItem.save()
                                """    
                                else:
                                    myMsgs("next path...")"""
                            #theNewPath = ""
                            #myMsgs ("the mxd saved: " + basename + extension)
                    #mxd.save()
                    #mxd.saveACopy(outMXDName, '10.1')
                    del mxd
    
        #del mxd
    else:
        myMsgs ("Repair source list: " + inFile + " does not exit.")
       
    #del mxd
    myMsgs('!!! Success !!! ')

# End main function

if __name__ == '__main__':
    main()

