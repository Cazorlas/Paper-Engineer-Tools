#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: import library
import clr  # Common Language Runtime for .NET
import System
import json  # Library để lưu và đọc file JSON
import os  # Library để thao tác với hệ thống file
import codecs
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

from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox

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

# Đường dẫn lưu JSON config Download
# script_dir = os.path.dirname(__file__)
# CONFIG_FILE = os.path.join(os.path.expanduser("~"), "Documents", "dynamo_config.json")

# Lấy thư mục chứa script đang chạy
script_dir = os.path.dirname(__file__)

# Lưu file JSON vào thư mục hiện tại
CONFIG_FILE = os.path.join(script_dir, "{}.json".format(EXEC_PARAMS.command_name))

# # Lấy đường dẫn thư mục AppData (C:\Users\YourName\AppData\Roaming)
# appdata_dir = os.getenv("APPDATA")
#
# # Tạo thư mục con (nếu cần)
# config_folder = os.path.join(appdata_dir, "MyDynamoConfig")
# os.makedirs(config_folder, exist_ok=True)  # Đảm bảo thư mục tồn tại
#
# # Lưu file JSON vào AppData
# CONFIG_FILE = os.path.join(config_folder, "dynamo_config.json")
#
# print("File sẽ được lưu tại:", CONFIG_FILE)



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
        json.dump(data, f, indent=4)


"""----------------------MAIN CODE----------------------------"""
try:
    # Lấy config từ JSON
    config = load_config()

    # Giá trị mặc định nếu không tìm thấy trong JSON
    dictionary_1 = {'Opt 1': 10.0, 'Opt 2': 20.0}
    configComboBox = config.get('combobox', 20.0)
    configTextBox = config.get('textbox', 'First Run')
    configCheckBox = config.get('checkbox', True)

    # Xác định giá trị mặc định của ComboBox
    keyComboBox = next((key for key, val in dictionary_1.items() if val == configComboBox), 'Opt 2')

    # Tạo form với giá trị mặc định từ config
    components = [
        Label('Pick Style:'),
        ComboBox('combobox1', dictionary_1, default=keyComboBox),
        Label('Enter Name:'),
        TextBox('textbox1', Text=configTextBox),
        CheckBox('checkbox1', 'Check this', default=configCheckBox),
        Separator(),
        Button('Select')
    ]
    form = FlexForm('Paper Engineer', components)
    form.show()

    # Nếu người dùng nhấn "Select"
    if form.values:
        new_config = {
            "combobox": dictionary_1.get(form.values.get('combobox1'), 20.0),
            "textbox": form.values.get('textbox1'),
            "checkbox": form.values.get('checkbox1')
        }
        save_config(new_config)  # Lưu lại config vào JSON

        print("Saved Config:", new_config)

# Handle the case when the user cancels the operation
except Autodesk.Revit.Exceptions.OperationCanceledException:
    TaskDialog.Show("Canceled", "Operation was canceled by the user.")

# Handle any other exceptions and show an error message
except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))  # Display a task dialog with the error message
