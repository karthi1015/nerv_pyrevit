
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
    RevitLinkType, FilteredWorksetCollector, WorksetKind, ElementWorksetFilter, ViewFamilyType, ViewFamily, \
    ViewDrafting, ElementTransformUtils, CopyPasteOptions, ViewSheet, View
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

targetCate = ["Lines", "Text Notes", "Raster Images", "Dimensions", "Generic Annotations"]
def WorksetElements(doc, workset):
    elementCollector = FilteredElementCollector(doc)
    elementWorksetFilter = ElementWorksetFilter(workset.Id, False)
    worksetElemsfounds = elementCollector.WherePasses(elementWorksetFilter).ToElements()
    return worksetElemsfounds
# Collect Sheet Workset
def FindSheetFromDoc(doc, sheetName):
    sheet = ()
    viewports = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()
    for i in viewports:
        name = i.LookupParameter('Sheet Name').AsString()
        number = i.LookupParameter('Sheet Number').AsString()
        all = "View \"Sheet: " + number + ' - ' + name + "\""
        # print('1' + all)
        if sheetName == all:
            sheet = i
            break
        else:
            return
    return sheet

def SheetWorksetCollector(doc):
    worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.ViewWorkset).ToWorksets()
    sheetWorkset = []
    for workset in worksets:
        # print(workset.Name)
        if workset.Name[6:11] == 'Sheet':
            sheetWorkset.append(workset)
    return sheetWorkset

# Check for forbidden elements from a targets category list and return these elements
def SheetElementCheck(doc, sheetWorkset, targets):
    model = []
    elems = WorksetElements(doc, sheetWorkset)
    for elem in elems:
        cate = elem.Category
        if cate:
            print(cate.Name)
            if str(elem.Category.Name) in targets:
                model.append(elem.Id)
    return model

def CreateDrafting(doc):
    vd = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
    draftingType = ()
    for v in vd:
        if v.ViewFamily == ViewFamily.Drafting:
            draftingType = v
            break
    draftingView = ViewDrafting.Create(doc, draftingType.Id)
    # draftingView.Name = name + draftingView.Name
    return draftingView
FindSheetFromDoc(doc, "View \"Sheet: A102 - Site Plan")
sheets = SheetWorksetCollector(doc)

# Location and Copy Paste Options
trans = None
op = CopyPasteOptions()


# Copy Loop
for sheet in sheets:
    elements = SheetElementCheck(doc, sheet, targetCate)
    # Check if there are elements to copy
    if elements:
        sheetName = sheet.Name
        print(sheetName)
        origin = FindSheetFromDoc(doc, sheetName)
        print(origin, View)
        originSheetName = origin.LookupParameter('Sheet Name').AsString()
        t = Transaction(doc, 'Copy ' + sheetName + ' to drafting')
        t.Start()
        dView = CreateDrafting(doc)
        dView.Name = originSheetName + ' ' + dView.Name
        ElementTransformUtils.CopyElements(origin, elements, dView, trans, op)
        t.Commit()



