
import sys, clr
import ConfigParser
from os.path import expanduser
# Set system path
home = expanduser("~")
cfgfile = open(home + "\\STVTools.ini", 'r')
config = ConfigParser.ConfigParser()
config.read(home + "\\STVTools.ini")
# Master Path
syspath1 = config.get('SysDir','MasterPackage')
sys.path.append(syspath1)
# Built Path
syspath2 = config.get('SysDir','SecondaryPackage')
sys.path.append(syspath2)

import System, Selection
import System.Threading
import System.Threading.Tasks
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, Family,Transaction,\
    FailureHandlingOptions, CurveElement, BuiltInCategory, ElementId, SpatialElementTag, RevitLinkInstance, \
    RevitLinkType, View, BoundingBoxXYZ
import re
from Autodesk.Revit.DB import Level, BuiltInParameter
from Autodesk.Revit.UI import TaskDialog
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms
from Autodesk.Revit.UI import TaskDialog, UIApplication
'''
LinkObj = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
LinkTyp = FilteredElementCollector(doc).OfClass(RevitLinkType).ToElements()
modelLst = []
count = 0
for a in LinkObj:
    line = []
    print(a.Name)
    '''
'''
from os.path import expanduser
home = expanduser("~")
print(home)
print(doc.Title)

uiapp = UIApplication(doc.Application)
application = uiapp.Application
versionName = application.VersionName
print(versionName)
viewports = FilteredElementCollector(doc).OfClass(View).ToElements()
for v in viewports:
    print v.Name
'''

# selection = Selection.get_selected_elements(doc)
import datetime
downloadModel = False
timeStamp = datetime.datetime.now().time()  # Throw away the date information
# Timer after which time download model will start
setTime = datetime.time(21, 00, 00)
if config.get('General','clouddownload') == "1" and setTime <= timeStamp:
    downloadModel = True
elif config.get('General','clouddownload') == "2":
    downloadModel = True
else:
    pass

print(downloadModel)


