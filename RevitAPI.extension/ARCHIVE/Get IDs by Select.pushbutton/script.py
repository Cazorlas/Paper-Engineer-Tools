# TODO: import library
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

from pyrevit import script

# get current Autodesk Revit project that can interface and interact with settings and operations in the UI
uidoc = __revit__.ActiveUIDocument
# get current Revit database document from the active UI document
doc = __revit__.ActiveUIDocument.Document

# ------Note: __revit__ = Autodesk.Revit.UI.UIApplication

# TODO: Call variable & method
# get the current selection element
selection = uidoc.Selection

# ----------------------Main Code----------------------------

# TODO: Create Selected Elements list
# create placeholder elements list
ele_list = [doc.GetElement(id) for id in selection.GetElementIds()]

# TODO: Create List Data
# iterate through the list and take category of each object
category_list = [element.Category.Name for element in ele_list]

# iterate through the list and take IDs of each object
id_list = [element.Id for element in ele_list]

# iterate through the list and take name of each object
name_list = [element.Name for element in ele_list]

# TODO: Create Table

output = script.get_output()

linked_id_list = [output.linkify(id) for id in id_list]  # Create Linkify for ID

data = list(zip(name_list, category_list, linked_id_list))

show_table = output.print_table(
    table_data=data,
    title="Data Selected Elements",
    columns=["Name", "Category", "ID"],
    formats=['', '', '']
)
