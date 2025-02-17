#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: import library
import clr  # Common Language Runtime for .NET
import System
import math  # Standard Python math library
import json  # Library để lưu và đọc file JSON
import os  # Library để thao tác với hệ thống file

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

CONFIG_FILE = os.path.join(os.getenv("APPDATA"), "MathParameterConfig.json")

"""----------------------FUNCTION----------------------------"""


def load_config():
    """Đọc config từ file JSON, nếu không có thì dùng giá trị mặc định."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}  # Nếu file lỗi, trả về rỗng
    return {}  # Nếu không có file, trả về rỗng


def save_config(data):
    """Lưu config vào file JSON."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


"""----------------------MAIN CODE----------------------------"""
if __name__ == "__main__":
    try:
        # Lấy config từ JSON
        config = load_config()

        # Giá trị mặc định nếu không tìm thấy trong JSON
        modeWorking = config.get('modeWorking', False)

        # Tạo form với giá trị mặc định từ config
        components = [
            Label('Mode:'),
            CheckBox('checkbox1', 'Run directly', default=modeWorking),
            Label("No need to choose the Parameter for the next time."),
            Separator(),
            Button('Save')
        ]
        form = FlexForm('Paper Engineer', components)
        form.ShowDialog()

        # Nếu người dùng nhấn "Select"
        if form.values:
            newConfig = {
                "modeWorking": form.values.get('checkbox1')
            }

            save_config(newConfig)  # Lưu lại config vào JSON


    # Handle the case when the user cancels the operation
    except Autodesk.Revit.Exceptions.OperationCanceledException:
        TaskDialog.Show("Canceled", "Operation was canceled by the user.")

    # Handle any other exceptions and show an error message
    except Exception as ex:
        TaskDialog.Show("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
