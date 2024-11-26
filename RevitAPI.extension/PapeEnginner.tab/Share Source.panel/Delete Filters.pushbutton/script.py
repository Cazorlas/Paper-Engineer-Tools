# -*- coding: utf-8 -*-
import Autodesk

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

from pyrevit import forms

doc = __revit__.ActiveUIDocument.Document  # Get all data from current project
view = doc.ActiveView  # Get the data current UI view in the project
uidoc = __revit__.ActiveUIDocument  # Get the all data UI in the project
DB = Autodesk.Revit.DB  # Assign module to variable


def showDialog(title, main):
    """Hiện Dialog"""
    return TaskDialog.Show(title, main)


# ----------------------------------Main Logic---------------------------------------------------------------------------


# Get all Filters in Current View
# allFilter = FilteredElementCollector(doc,view)

# Get all Filters in Project
"""Get data filter"""
allFilter = FilteredElementCollector(doc).OfClass(DB.ParameterFilterElement).ToElements()

if not allFilter:
    showDialog("OK", "NO FILTER")
else:
    nameFilter = []

    for filter in allFilter:
        nameFilter.append(filter.Name)

    # Process raw data
    filter_dic = dict(zip(nameFilter, allFilter))

    # UI
    res = forms.SelectFromList.show(
        {'All': filter_dic},
        title='Filter List',
        group_selector_title='Select Integer Range:',
        multiselect=True
    )
    if not res:
        showDialog("NO", "Chọn filter mới xóa được")
    else:

        list_filter = []

        for name in res:
            list_filter.append(filter_dic.get(name))

        # Delete Filters
        t = Transaction(doc)
        t.Start('Delete Selected Filters')

        for i in list_filter:
            doc.Delete(i.Id)

        t.Commit()

        showDialog("OK", "GOOD JOB BOYS")
