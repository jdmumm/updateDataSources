import arcpy
import pythonaddins
import os
relPath = os.path.dirname(__file__)
toolPath = relPath + r"\CheckAndFixLinks.tbx"

class btnGDBInventory(object):
    """Implementation for GDBInventory_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(toolPath, "ListFGDBsize")

class btnFCInventory(object):
    """Implementation for FCInventory_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(toolPath, "FCInventoryReport")

class btnListBrokenSources(object):
    """Implementation for ListBrokenSources_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(toolPath, "ListUniqueBrokenLinksNoFix")

class btnFixDriveLetters(object):
    """Implementation for FixDriveLetters_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(toolPath, "ListUniqueBrokenLinksWFix")

class btnDataSourceRepair(object):
    """Implementation for DataSourceRepair_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(toolPath, "RepairDetailedBrokenLinks")

class SpareButton1(object):
    """Implementation for SpareButton1_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass

class YieldForInstructions(object):
    """Implementation for SpareButton2_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pass
