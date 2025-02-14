#!/usr/bin/env python
# -*- coding: utf-8 -*-


import clr  # Common Language Runtime for .NET
import System
import math  # Standard Python math library

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *
from pyrevit import forms, revit, script,EXEC_PARAMS


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

""" ----------------------FUNCTIONS----------------------------"""

# Định nghĩa lớp MyOption để tạo danh sách checkbox với tên tùy chọn
class MyOption(forms.TemplateListItem):
    def __init__(self, orig_item, checked=False):
        """
        Gói một đối tượng (tên danh mục) vào danh sách checkbox.

        Args:
            orig_item (str): Tên danh mục
            checked (bool): Trạng thái ban đầu của checkbox (mặc định là False)

        """
        super(MyOption, self).__init__(orig_item, checked=checked)
        self.item = orig_item  # Lưu trữ danh mục ban đầu

    @property
    def name(self):
        return "{}".format(self.item)  # Hiển thị tên danh mục trong danh sách


def Flatten_lv3(lst):
    return [i for subLst in lst for i in subLst]


def Flatten_lv2(lst):
    return [subLst for subLst in lst]


def ToList(input):
    if isinstance(input, list):
        return input
    else:
        return [input]





def AllAnnotationCategories():
    allCategories = doc.Settings.Categories

    return [cat for cat in allCategories if cat.CategoryType == CategoryType.Annotation]



    """----------------------MAIN CODE----------------------------"""


if __name__ == "__main__":
    try:
        global formInputInstance

        # Lấy config
        # config = script.get_config(EXEC_PARAMS.command_name)
        # previousSelectedCategories = config.get_option('selected_category', False)

        annotationCategories = AllAnnotationCategories()
        annotationCategoriesName = [cate.Name for cate in annotationCategories]
        annotationCategoriesDict = dict(zip(annotationCategoriesName, annotationCategories))
        sortedData = sorted(annotationCategoriesName)
        # sortedData = sorted(annotationCategoriesDict)

        # Lấy danh sách tùy chọn
        # ops = sorted(annotationCategoriesDict)
        # ops = [MyOption(cate, checked=cate in previousSelectedCategories) for cate in sortedData]

        # Run Setting first
        projectInfo = doc.ProjectInformation
        param = projectInfo.LookupParameter("checkTagConfiguration")

        if param is None:
            Alert(content="Please run Setting First", title="Warning", exit=True)
        else:
            paramValue = param.AsValueString()
            if not paramValue:
                Alert(content="Please run Setting First", title="Warning", exit=True)
            else:
                data = json.loads(paramValue)
                selectCateName = data.get('listViewItem', [])

                # selectCateName = forms.SelectFromList.show(
                #     {'Annotation Categories': ops},
                #     title='Select Categories',
                #     group_selector_title='Select Categories',
                #     multiselect=True
                # )
                #
                # if not selectCateName:
                #     Alert('No choose any category.', exit=True)
                # else:
                #
                #     config.selected_category = ToList(selectCateName)
                #     script.save_config()
                #
                #
                #