# -*- coding: utf-8 -*-

import clr
from pyrevit import forms
from System.Collections.Generic import *
from rpw.ui.forms import Alert
import sys

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
DB = Autodesk.Revit.DB

# ----------------------------START CODE------------------------------
try:
    # ----------------------------Select Template Sheet------------------------------
    grid_activeview = FilteredElementCollector(doc, view.Id).OfClass(Grid).WhereElementIsNotElementType().ToElements()

    selected_option = forms.CommandSwitchWindow.show(
        ['3D to 2D', '2D to 3D'],
        message='Select Option:', )

    # ----------------------------TRANSACTION------------------------------
    if not selected_option:
        sys.exit()
    if selected_option == '3D to 2D':
        t = Transaction(doc, 'Convert Grids')
        t.Start()

        for i in grid_activeview:
            i.SetDatumExtentType(DatumEnds.End0, view, DatumExtentType.ViewSpecific)
            i.SetDatumExtentType(DatumEnds.End1, view, DatumExtentType.ViewSpecific)

        t.Commit()

    if selected_option == '2D to 3D':
        t = Transaction(doc, 'Convert Grids')
        t.Start()

        for i in grid_activeview:
            i.SetDatumExtentType(DatumEnds.End0, view, DatumExtentType.Model)
            i.SetDatumExtentType(DatumEnds.End1, view, DatumExtentType.Model)

        t.Commit()

    Alert('Convert Grids Sucessfully', 'Transaction Done')

except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))
