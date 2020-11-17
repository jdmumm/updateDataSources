"""
---------------------------------------------------------------------------
 _miscUtils.py ---- tool:  Print/messaging/loggins util, date/time utils
 Created: 2011; modified May 12 2015
 args:  none
------------------------------------------------------------------------------
 Author: Rebecca Strauch - ADFG-DWC-GIS
 Purpose: Utilities to simplify debugging and running of other tools.
   - Automatically decides whether a "print" or "arcpy.AddMessage" is needed 
     to help with debugging and tools progress. 
   - Creates log file in c:\ESRITEST directory.  may have problems if 
     not able to write to file
   - Has timestamp, curDate, and curFileDateTime functions to help with
     time stamping messages (not really needed in latest versions, 10.2+)
     and for MM/DD/YY and a string YYYYMMDD_HHMM format (for outfile naming)

   To call in another tool:
     - for addins, best to put in the same folder as tools script
     - for general use, can copy to c:\Python27\ArcGIS\ArcGIS 10.3   
       exact path may vary depending on your version of ArcGIS
     Call with:  
          from _miscUtils import *  

---------------------------------------------------------------------------
"""
import time
import arcpy
import os
from time import localtime

def timeStamp():
	"""
	returns time stamp.
	"""
	return time.strftime(' --  %B %d - %H:%M:%S')

def myMsgs(message):
	arcpy.AddMessage(message + ' %s' %(timeStamp()))
	print(message) # + ' %s' %(timeStamp()))

	global messageCount
	# next block would create a log file, but currently requires write permissions 
	#  on the C drive.  No time to fix right now, so blocking it out.
	'''logFolder = r"c:\FixLinkslog"
	if not arcpy.Exists(logFolder):
		arcpy.CreateFolder_management(os.sep.join(logFolder.split(os.sep)[:-1]), logFolder.split(os.sep)[-1])
	mdy = curDate()
	#mdy = curFileDateTime()
	logName = "logfile_" + mdy + ".log"
	logName = "logfile_" + "_".join(mdy.split("/")) + ".log"
	logFile = open(os.path.join(logFolder, logName), "a")  #a=append, w=create new
	if message.lower() == "blank line":
		logFile.write("\n\n")
		print "\n\n"
	elif message.lower() == "close logfile":
		logFile.write("\n\n*****  finished  *****\n\n")
		logFile.close()
	else:
		messageCount += 1
		logFile.write("0" * (5 - len(str(messageCount))) + str(messageCount) + ".   ")
		logFile.write(message)
		logFile.write("\n")
		#print message
		#arcpy.AddMessage(message)'''

def curDate():
	rawTime = localtime()
	yr = str(rawTime[0]) # Collect the year from the rawTime variable
	mo = str(rawTime[1]).zfill(2) # Collect the month from the rawTime variable
	dy = str(rawTime[2]).zfill(2) # Collect the day from the rawTime variable
	return "/".join([mo, dy, yr])

def curFileDateTime():
	rawTime = localtime()
	yr = str(rawTime[0]) # Collect the year from the rawTime variable
	mo = str(rawTime[1]).zfill(2) # Collect the month from the rawTime variable
	dy = str(rawTime[2]).zfill(2) # Collect the day from the rawTime variable
	hr = str(rawTime[3]).zfill(2) # Collect the day from the rawTime variable
	mn = str(rawTime[4]).zfill(2) # Collect the day from the rawTime variable
	return (yr + mo + dy + "_" + hr + mn)
	#return "/".join([mo, dy, yr, hr, mn])

messageCount = 0

'''***********************
log file code provided by:
Freddie Gibson (~2012)
Software Support Analyst
Desktop Unit
ESRI Support Services
'''


