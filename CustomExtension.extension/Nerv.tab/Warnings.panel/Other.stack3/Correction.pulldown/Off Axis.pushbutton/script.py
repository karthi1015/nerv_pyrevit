import sys
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

# -*- coding: utf-8 -*-
from pyrevit.framework import List
from pyrevit import revit, DB
import clr
from collections import defaultdict
from pyrevit import script
from pyrevit import forms
import pyrevit
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Transaction, JoinGeometryUtils
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
import Warnings

__doc__ = 'Prints out a warnings by category.'\
          ' This is helpful to resolve warnings'

def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)
# t = Transaction(doc, 'Correct Lines')
# t.Start()
lines = []
if revit.doc.IsWorkshared:
    warnings = doc.GetWarnings()
# select selected warnings
    for warning in warnings:
        elementId = warning.GetFailingElements()
        additionalId = warning.GetAdditionalElements()
        text = warning.GetDescriptionText()
        if 'Line is slightly off axis' in text:
            for e in elementId:
                lines.append(doc.GetElement(e))
                print(e)

i = 0
t = Transaction(doc, 'Correct Lines')
t.Start()
for l in lines:
    #if l.Category.Name == '<Sketch>':
    off_line = l.GeometryCurve
    joined = JoinGeometryUtils.GetJoinedElements(doc, l)
    sketchPlane = l.SketchPlane
    correct_line = Warnings.CorrectLineXY(off_line, 0.02)
    print(correct_line)
    # l.SetSketchPlaneAndCurve(sketchPlane, correct_line)
    l.SetGeometryCurve(correct_line, True)
    '''
        if joined:
            for j in joined:
                JoinGeometryUtils.JoinGeometry(doc, l, j)
        
    except:
        outprint = script.get_output()
        print("Exception raised" + format(outprint.linkify(l.Id)))
        '''
t.Commit()