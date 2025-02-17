#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO: Import libraries and modules
import clr  # Common Language Runtime for .NET
import System
import json
import os
import math  # Standard Python math library

# Excel Library
clr.AddReference('Microsoft.Office.Interop.Excel')
from Microsoft.Office.Interop import Excel

# Import necessary .NET and Revit API libraries
from System.Collections.Generic import *
from pyrevit import forms, revit, script, EXEC_PARAMS

from rpw.ui.forms import *
from MainForm import MainForm

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

import threading
import System.Threading
import System.Windows.Forms
from System.Windows.Forms import Application

# TODO: Prepare variables and input
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
view = doc.ActiveView
DB = Autodesk.Revit.DB
output = script.get_output()
version = int(app.VersionNumber)
selection = uidoc.Selection

# Đặt lệnh này NGAY SAU khi import System.Windows.Forms
Application.EnableVisualStyles()

""" ----------------------FUNCTIONS----------------------------"""


def Flatten_lv3(lst):
    return [i for subLst in lst for i in subLst]


def Flatten_lv2(lst):
    return [subLst for subLst in lst]


def ToList(input):
    if isinstance(input, list):
        return input
    else:
        return [input]


def AllElementOfCategoryInView(chooseView, categoryName):
    categoryName = ToList(categoryName)
    allCategories = doc.Settings.Categories
    valid_cate = []
    alleles = []
    for cate in allCategories:
        for category in categoryName:
            if cate.Name == category:
                valid_cate.append(cate)

    for cate in valid_cate:
        alleles.append(FilteredElementCollector(doc, chooseView.Id).OfCategoryId(
            cate.Id).WhereElementIsNotElementType().ToElements())

    return Flatten_lv3(alleles)


def AllAnnotationCategories():
    allCategories = doc.Settings.Categories

    return [cat for cat in allCategories if cat.CategoryType == CategoryType.Annotation]


def GetTaggedElement(tag):
    result = []
    if version < 2022:
        taggedElement = tag.GetTaggedLocalElement()
        result.append(taggedElement)
    else:
        taggedElements = tag.GetTaggedLocalElements()
        for element in taggedElements:
            result.append(element)
    return result


def SetDifference(lst1, lst2):
    """lst 1 > lst2"""
    result = []
    for item1 in lst1:
        if item1 not in lst2:
            result.append(item1)
    return result


def GroupByKey(items, keys):
    # Create unique key lists
    unique_keys = []
    for key in keys:
        if key not in unique_keys:
            unique_keys.append(key)

    # Create empty lists according to unique keys
    group_lst = []
    for i in range(len(unique_keys)):
        group_lst.append([])

    # Get index of the input keys in unique key lists
    ind_lst = []
    for key in keys:
        ind_lst.append(unique_keys.index(key))

    # Group by key
    for item, ind in zip(items, ind_lst):
        group_lst[ind].append(item)

    return group_lst, unique_keys


def GetElementCategory(ele):
    return ele.Category.Name


def GetFamilyNameOfElement(ele):
    return ele.LookupParameter('Family').AsValueString()


def GetTypeNameOfElement(ele):
    return ele.Name


def TaggedOrNotTagged(lstCate):
    result = []
    for cate in lstCate:
        getAll = AllElementOfCategoryInView(view, cate)
        if len(getAll) == 0:

            result.append(False)
        else:
            result.append(True)
    return result


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


if __name__ == "__main__":
    try:
        CONFIG_FILE = os.path.join(os.getenv("APPDATA"), "CheckTagConfig.json")
        global formInputInstance

        annotationCategories = AllAnnotationCategories()
        annotationCategoriesName = [cate.Name for cate in annotationCategories]
        annotationCategoriesDict = dict(zip(annotationCategoriesName, annotationCategories))
        sortedData = sorted(annotationCategoriesName)

        # Hanlde UI Output
        config = load_config()
        checkedItems = config.get('listViewItem', [])

        if len(checkedItems) == 0:
            Alert(content="Please run Setting First", title="Warning", exit=True)
        else:
            selectCateName = config.get('listViewItem', [])

            processCateTagta = TaggedOrNotTagged(selectCateName)

            allTagOfCategoryInView = AllElementOfCategoryInView(view, selectCateName)
            taggedElement = Flatten_lv3([GetTaggedElement(tag) for tag in allTagOfCategoryInView])  # List 2

            cateNameOfTaggedElement = sorted(list(set([ele.Category.Name for ele in taggedElement])))
            allModelElement = AllElementOfCategoryInView(view, cateNameOfTaggedElement)  # List 1

            allEle = AllElementOfCategoryInView(view, selectCateName)

            """----------------------Compare and find elements have not been tagged----------------------------"""

            taggedElementId = [element.Id for element in taggedElement]
            modelElementId = [element.Id for element in allModelElement]

            notTaggedElementId = SetDifference(modelElementId, taggedElementId)
            notTaggedCategoryName = [doc.GetElement(id).Category.Name for id in notTaggedElementId]

            groupElementByCategory = GroupByKey(notTaggedElementId, notTaggedCategoryName)
            notTaggedElementGroup = groupElementByCategory[0]  # Get elements have been grouped
            notTaggedCategoryGroup = groupElementByCategory[1]

            taggedCategory = list(set(cateNameOfTaggedElement) - set(notTaggedCategoryGroup))

            try:
                if len(allTagOfCategoryInView) == 0:
                    Alert('All Elements Have Not Been Tagged.', exit=True)
                elif len(notTaggedCategoryGroup) > 0:
                    notTaggedCategory = [GetElementCategory(doc.GetElement(Id)) for Id in notTaggedElementId]
                    notTaggedFamilyRaw = [GetFamilyNameOfElement(doc.GetElement(Id)) for Id in notTaggedElementId]
                    notTaggedTypeRaw = [GetTypeNameOfElement(doc.GetElement(Id)) for Id in notTaggedElementId]
                    notTaggedIdRaw = [Id.IntegerValue for Id in notTaggedElementId]

                    groupFamily = GroupByKey(notTaggedFamilyRaw, notTaggedCategory)
                    notTaggedFamily = groupFamily[0]

                    groupType = GroupByKey(notTaggedTypeRaw, notTaggedCategory)
                    notTaggedType = groupType[0]

                    groupId = GroupByKey(notTaggedIdRaw, notTaggedCategory)
                    notTaggedId = groupId[0]

                    data = [[list(zip(family, typeName, ids))] if len(family) == 1 else [[(fam, typ, Id)] for
                                                                                         fam, typ, Id in
                                                                                         zip(family, typeName, ids)]
                            for
                            family, typeName, ids in zip(notTaggedFamily, notTaggedType, notTaggedId)]

                    """-------------RUN FORM-------------"""
                    f = MainForm(notTaggedCategory, notTaggedFamilyRaw, notTaggedTypeRaw, notTaggedIdRaw,
                                 processCateTagta,
                                 selectCateName, notTaggedCategoryGroup, taggedCategory, data)

                    # Application.Run(f)
                    f.Show()

                # if len(taggedCategory) != 0:
                #     result = ", ".join(map(str, taggedCategory))
                #     Alert('All Elements Of {} Have Been Tagged.'.format(result))

            except Exception as exx:
                TaskDialog.Show("Failed", "Warning: {}".format(exx))  # Corrected string formatting







    except Autodesk.Revit.Exceptions.OperationCanceledException:
        pass

    except Exception as ex:
        TaskDialog.Show("Error", "Warning: {}".format(ex))  # Corrected string formatting
