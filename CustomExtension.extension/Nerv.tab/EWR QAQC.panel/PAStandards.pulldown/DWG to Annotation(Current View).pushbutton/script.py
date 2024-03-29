
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
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


from Autodesk.Revit.DB import Document,FilteredElementCollector,FamilySymbol,Transaction,\
     BuiltInCategory, ElementId, ViewSchedule, View, ImportInstance
from Autodesk.Revit.UI import TaskDialog

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
from pyrevit import forms


def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)

# selection = get_selected_elements(doc)
importInstance = []
replaceImports = []


# collect dwg from view
imports = DB.FilteredElementCollector(doc) \
    .OfClass(ImportInstance) .OwnedByView(doc.ActiveView.Id)\
    .ToElements()


for i in imports:
    if not i.LookupParameter('Name').AsString() in importInstance:
        importInstance.append(i.LookupParameter('Name').AsString())

replaceName = forms.SelectFromList.show(importInstance,
                                   multiselect=False,
                                   button_name='Select Annotation')
# Selected
for i in imports:
    if i.LookupParameter('Name').AsString() == replaceName:
        replaceImports.append(i)


# Get all Annotation Symbols
symbols = DB.FilteredElementCollector(doc) \
    .OfClass(clr.GetClrType(FamilySymbol)) .OfCategory(BuiltInCategory.OST_GenericAnnotation)\
    .ToElements()

# Select Name
sNames = []
replaceAnno = ()
# Get the selected symbol
for i in symbols:
    sNames.append(i.Family.Name)

replaceName = forms.SelectFromList.show(sNames,
                                   multiselect=False,
                                   button_name='Select Annotation')

for i in symbols:
    if i.Family.Name == replaceName:
        replaceAnno = i


t = Transaction(doc, 'Replace dwg')
t.Start()
for cad in replaceImports:
    if cad.ViewSpecific:
        max = cad.BoundingBox[doc.ActiveView].Max
        min = cad.BoundingBox[doc.ActiveView].Min
        location = (max + min)/2
        boxes = doc.Create.NewFamilyInstance(location, replaceAnno, doc.ActiveView)
        doc.Delete(cad.Id)
t.Commit()


