#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: import library
import clr  # Common Language Runtime for .NET
import System
import math  # Standard Python math library

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *
from pyrevit import forms, revit, script

clr.AddReference('ProtoGeometry')  # Dynamo's geometry proxy
from Autodesk.DesignScript.Geometry import *  # Import everything from Dynamo's geometry

clr.AddReference("RevitAPI")  # Revit API DLLs
clr.AddReference("RevitAPIUI")  # Revit UI DLLs

import Autodesk
from Autodesk.Revit.DB import *  # Revit API classes
from Autodesk.Revit.UI import *  # Revit UI classes
from Autodesk.Revit.UI.Selection import *  # For handling Revit selections

clr.AddReference("RevitNodes")  # Dynamo nodes for Revit
import Revit  # Import Revit namespace in RevitNodes

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

from pyrevit import EXEC_PARAMS

from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, TextBox, Separator, Button, CheckBox

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager  # Document management in Revit
from RevitServices.Transactions import TransactionManager  # Transaction management

# Prepare document and other variables
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
DB = Autodesk.Revit.DB
output = script.get_output()
unit = doc.GetUnits()
version = int(app.VersionNumber)
selection = uidoc.Selection

"""----------------------FUNCTION----------------------------"""

"""----------------------MAIN CODE----------------------------"""
try:
    # Lấy config
    config = script.get_config(EXEC_PARAMS.command_name)

    dictionary_1 = {'Opt 1': 10.0, 'Opt 2': 20.0}

    # Lấy giá trị:
    configComboxBox = config.get_option('combobox',20.0)
    configTextBox = config.get_option('textbox','First Run')
    configCheckBox = config.get_option('checkbox',True)

    # keyComboBox = [key for key,val in dictionary_1.items() if val == configComboxBox]
    for key,val in dictionary_1.items():
        if val == configComboxBox:
            keyComboBox = str(key)
            break

    # Tạo form với giá trị mặc định từ config
    components = [
        Label('Pick Style:'),
        ComboBox('combobox1', {'Opt 1': 10.0, 'Opt 2': 20.0}, default=keyComboBox),
        Label('Enter Name:'),
        TextBox('textbox1', Text=configTextBox),
        CheckBox('checkbox1', 'Check this', default=configCheckBox),
        Separator(),
        Button('Select')
    ]
    form = FlexForm('Paper Engineer', components)
    form.show()
    # # values = form.get_values()
    #
    # Nếu người dùng nhấn "Select"
    if form.values:
        config.combobox = form.values.get('combobox1')
        config.textbox = form.values.get('textbox1')
        config.checkbox = form.values.get('checkbox1')
        script.save_config()
        # logger = script.get_logger()
        # logger.warning()
        print(form.values)



# Handle the case when the user cancels the operation
except Autodesk.Revit.Exceptions.OperationCanceledException:
    TaskDialog.Show("Canceled", "Operation was canceled by the user.")

# Handle any other exceptions and show an error message
except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
