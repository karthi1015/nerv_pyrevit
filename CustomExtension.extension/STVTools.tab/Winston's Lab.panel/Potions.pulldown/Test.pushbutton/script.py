
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
    FailureHandlingOptions, CurveElement, BuiltInCategory, ElementId, SpatialElementTag

from Autodesk.Revit.DB.Architecture import RoomTag
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

# Body
output = []
t = Transaction(doc, "Get Orphaned Room Tag")
# Transaction Start
#t.Start()
cl = FilteredElementCollector(doc)
tag = cl.OfClass(SpatialElementTag).ToElements()
for z in tag:
#	x = z.IsOrphaned
#	if x:
#		y = z.Id
#		#doc.Delete(y)
#		i = y.ToString()
#		wset = z.GetParameters("Workset")
#		for a in wset:
#			b = a.AsString()
#		output.append(i)
#		output.append(b)
	wset = z.GetParameters("Workset")
	for a in wset:
		b = a.AsValueString()
		output.append(b)
#t.Commit()
print(output)

