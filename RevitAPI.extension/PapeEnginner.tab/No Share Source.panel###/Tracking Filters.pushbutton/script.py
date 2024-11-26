# -*- coding: utf-8 -*-
"""
Delete all Filters in Project
"""
import Autodesk

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

from pyrevit import forms

doc = __revit__.ActiveUIDocument.Document  # Get all data from current project
view = doc.ActiveView  # Get the data current UI view in the project
uidoc = __revit__.ActiveUIDocument  # Get the all data UI in the project
DB = Autodesk.Revit.DB  # Assign module to variable


def showDialog(title, main):
    """Show TaskDialog"""
    return TaskDialog.Show(title, main)


# ----------------------------------Main Logic---------------------------------------------------------------------------


# TODO: Get information of filters
all_Filter = FilteredElementCollector(doc).OfClass(DB.ParameterFilterElement).ToElements()
filterName = [doc.GetElement(Id).Name for Id in filterIdList]
filterDict = dict(zip(filterName,filterIdList))
filterParamId = [GetParameterIdFromFilter(Id) for Id in filterIdList]


