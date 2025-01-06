# -*- coding: utf-8 -*-

# TODO: Import library and modules
import clr  # This is .NET's Common Language Runtime.
import System  # The System namespace at the root of .NET
import math  # Math library from Python
import string
from Form import MainForm
from Functions import *

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

"----------------------Main Code----------------------------"
try:
    "----------------------------Get all Titile Blocks Family----------------------------"
    titileBlocks_family = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).ToElements()

    # Get Family Type
    titileBlocks = [titleBlock for titleBlock in titileBlocks_family if
                    isinstance(titleBlock, Autodesk.Revit.DB.FamilySymbol)]

    # Get type name of titleblock
    all_typename = []
    for t in titileBlocks:
        # Get the Family Type Name Parameter
        parameter = t.get_Parameter(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM)

        # Get the Value of the Parameter
        typeName = parameter.AsValueString()

        # Add the Name to the Output List
        all_typename.append(typeName)

    "----------------------------Create Dictionary----------------------------"
    dict_titleblocks = dict(zip(all_typename, titileBlocks))

    "----------------------------TEST CASE----------------------------"
    # sheet_numbers, sheet_names = generate_sheet_data("-STT", "Floor Plan-", 15, True, True, "Prefix", "Suffix", "aaA",
    #                                                  "aa")
    # print(sheet_numbers)
    # print(50 * "-")
    # print(sheet_names)
    "-----------------------------------------------------------------"
    "----------------------------RUN FORMS----------------------------"
    f = MainForm(all_typename)
    f.ShowDialog()
    "----------------------------ACTION----------------------------"
    if f.DialogResult == System.Windows.Forms.DialogResult.OK:
        # DATA FROM FORM
        sheet_number = f._textBox1.Text
        sheet_name = f._textBox2.Text
        quantity_sheet = int(f._textBox5.Text)
        index_number = f._textBox3.Text
        index_name = f._textBox4.Text

        # Value from ComboBox
        combo_number = f._comboBox1.SelectedItem
        combo_name = f._comboBox2.SelectedItem

        # CheckBox values
        asc_check1 = f._checkBox1.Checked
        dsc_check2 = f._checkBox2.Checked
        asc_check3 = f._checkBox3.Checked
        dsc_check4 = f._checkBox4.Checked

        # Value from CheckedListBox
        selected_titleblock = f._checkedListBox1.Items[0]

        # GET TITLE BLOCKS FROM DICTIONARY
        titileBlock = dict_titleblocks.get(selected_titleblock)
        titileBlock_id = titileBlock.Id

        # Generate sheet numbers and names based on input
        sheet_numbers, sheet_names = generate_sheet_data(sheet_number, sheet_name,
                                                         quantity_sheet, asc_check1,
                                                         asc_check3, combo_number,
                                                         combo_name, index_number, index_name)

        # CREATE SHEET
        "Start a transaction group to create the sheets"
        tg = TransactionGroup(doc, 'Create Sheets')
        tg.Start()
        a = 0

        # Create the sheets based on the generated data
        for i in range(quantity_sheet):
            if create_sheet(sheet_numbers[i], sheet_names[i], titileBlock_id):
                a += 1
            else:
                print("Sheet number '{}' already exists. Please change sheet numbers.".format(sheet_numbers[i]))


        tg.Assimilate()

        print(50*"-")
        print("There are {} sheets have been created".format(a))

    else:
        pass

except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))
