# -*- coding: utf-8 -*-

# TODO: Import library and modules
import clr  # This is .NET's Common Language Runtime.
import System  # The System namespace at the root of .NET
import math  # Math library from Python
import string
from Form import MainForm

from System.Collections.Generic import *  # Lets you handle generics.
from pyrevit import forms, revit, script

clr.AddReference('ProtoGeometry')  # A Dynamo library for its proxy geometry class
from Autodesk.DesignScript.Geometry import *  # Loads everything in Dynamo's

clr.AddReference("RevitAPI")  # Adding reference to Revit's API DLLs
clr.AddReference("RevitAPIUI")  # Adding reference to Revit's API DLLs

import Autodesk  # Loads the Autodesk namespace
from Autodesk.Revit.DB import *  # Loading Revit's API classes
from Autodesk.Revit.UI import *  # Loading Revit's API UI classes
from Autodesk.Revit.UI.Selection import ObjectType  # Import ObjectType to handle selection

clr.AddReference("RevitNodes")  # Dynamo's nodes for Revit
import Revit  # Loads in the Revit namespace in RevitNodes

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import \
    DocumentManager  # An internal Dynamo class that keeps track of the document that Dynamo is currently attached to
from RevitServices.Transactions import \
    TransactionManager  # A Dynamo class for opening and closing transactions to change the Revit document's database

# TODO: Prepare variable and input
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
DB = Autodesk.Revit.DB
output = script.get_output()
unit = doc.GetUnits()
version = int(app.VersionNumber)


# TODO: Functions
def create_sheet(sheet_number, sheet_name, title_block_id):
    """Create Sheets"""
    try:
        existing_sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()
        for i in existing_sheets:
            sheet_number_param = i.get_Parameter(BuiltInParameter.SHEET_NUMBER)
            if sheet_number_param.AsValueString() == sheet_number:



                return False

        with Transaction(doc, 'Create Sheets') as t:
            t.Start()

            # Create new sheets
            new_sheet = ViewSheet.Create(doc, title_block_id)

            # Set the sheet number and name
            new_sheet.SheetNumber = sheet_number
            new_sheet.Name = sheet_name

            t.Commit()

            return True
    except Exception as ex:
        TaskDialog.Show("Error: {}".format(ex))
        return False


def increment_alpha_index(index, increment=True):
    """Increment or decrement an alphabetic index like 'AA', 'AB', etc."""
    letters = string.ascii_uppercase
    index_list = list(index)

    if increment:
        i = len(index_list) - 1
        while i >= 0:
            if index_list[i] == 'Z':
                index_list[i] = 'A'
                if i == 0:
                    index_list.insert(0, 'A')
                i -= 1
            else:
                index_list[i] = chr(ord(index_list[i]) + 1)
                break
    else:
        i = len(index_list) - 1
        while i >= 0:
            if index_list[i] == 'A':
                index_list[i] = 'Z'
                if i == 0:
                    index_list.pop(0)
                i -= 1
            else:
                index_list[i] = chr(ord(index_list[i]) - 1)
                break

    return ''.join(index_list)


def generate_sheet_data(sheet_number, sheet_name, quantity, asc_check_number, asc_check_name, index_position_number,
                        index_position_name, index_number, index_name):
    """
    Generate a list of sheet numbers and sheet names based on user input.
    If 'index_name' is empty, skip adding an index to the sheet names.
    """

    # Define allowed character sets
    letters = string.ascii_uppercase  # Uppercase letters A-Z

    # Initialize result lists
    sheet_numbers = []
    sheet_names = []

    # Convert index_number and index_name to strings
    index_number_str = str(index_number)
    index_name_str = str(index_name)

    # Check if index_number is numeric or alphabetic
    if index_number_str.isdigit():
        numeric_number = True
        index_number = int(index_number)  # Convert to integer for operations
    else:
        numeric_number = False

    # Check if index_name is numeric or alphabetic
    if index_name_str.isdigit():
        numeric_name = True
        index_name = int(index_name)  # Convert to integer for operations
    else:
        numeric_name = False

    # Loop over the quantity of sheets to generate
    for i in range(quantity):
        current_sheet_number = sheet_number
        current_sheet_name = sheet_name

        # Handle Sheet Number (numeric or alphabetic)
        if numeric_number:
            current_index_number = str(index_number).zfill(len(index_number_str))
            if index_position_number == "Prefix":
                current_sheet_number = "{}{}".format(current_index_number, sheet_number)
            elif index_position_number == "Suffix":
                current_sheet_number = "{}{}".format(sheet_number, current_index_number)

            # Update index number for next iteration
            if asc_check_number:
                index_number += 1
            else:
                index_number -= 1
        else:
            # Alphabetic handling for sheet number
            if index_position_number == "Prefix":
                current_sheet_number = "{}{}".format(index_number_str, sheet_number)
            elif index_position_number == "Suffix":
                current_sheet_number = "{}{}".format(sheet_number, index_number_str)

            # Update alphabetic index for next iteration
            index_number_str = increment_alpha_index(index_number_str, asc_check_number)

        # Handle Sheet Name (numeric or alphabetic)
        if not index_name_str:
            current_sheet_name = sheet_name
        else:
            if numeric_name:
                current_index_name = str(index_name).zfill(len(index_name_str))
                if index_position_name == "Prefix":
                    current_sheet_name = "{}{}".format(current_index_name, sheet_name)
                elif index_position_name == "Suffix":
                    current_sheet_name = "{}{}".format(sheet_name, current_index_name)

                # Update index name for next iteration
                if asc_check_name:
                    index_name += 1
                else:
                    index_name -= 1
            else:
                # Alphabetic handling for sheet name
                if index_position_name == "Prefix":
                    current_sheet_name = "{}{}".format(index_name_str, sheet_name)
                elif index_position_name == "Suffix":
                    current_sheet_name = "{}{}".format(sheet_name, index_name_str)

                # Update alphabetic index for next iteration
                index_name_str = increment_alpha_index(index_name_str, asc_check_name)

        # Append generated values to result lists
        sheet_numbers.append(current_sheet_number)
        sheet_names.append(current_sheet_name)

    # Return the lists of generated sheet numbers and sheet names
    return sheet_numbers, sheet_names


"----------------------Main Code----------------------------"
