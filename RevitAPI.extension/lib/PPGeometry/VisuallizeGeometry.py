#!/usr/bin/env python
# -*- coding: utf-8 -*-

import clr
import System
from System.Collections.Generic import List

import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

# Prepare document and other variables
# doc = __revit__.ActiveUIDocument.Document
# view = doc.ActiveView
# uidoc = __revit__.ActiveUIDocument
# app = __revit__.Application
# DB = Autodesk.Revit.DB
# unit = doc.GetUnits()
# version = int(app.VersionNumber)
""" ----------------------MAIN CODE----------------------------"""
class Visualize:

    @staticmethod
    def CreateDirectShape(doc, geometryObjects, builtInCategory=BuiltInCategory.OST_GenericModel):

        # Tạo DirectShape từ Document và category
        directShape = DirectShape.CreateElement(doc, ElementId(int(builtInCategory)))

        # Thiết lập hình dạng cho DirectShape
        directShape.SetShape(geometryObjects)
        return directShape

    @staticmethod
    def VisualizePoint(doc,points):
        # Giả sử 'points' là danh sách các đối tượng GeometryObject (có thể là các điểm dạng XYZ đã được chuyển đổi thành GeometryObject nếu cần)
        with Transaction(doc, "Create Points") as t:
            t.Start()
            # Ở đây, chúng ta gọi CreateDirectShape để tạo DirectShape từ danh sách points
            visualizePoint = PPVisualize.CreateDirectShape(doc,List[GeometryObject]([Point.Create(points)]))
            t.Commit()

        return visualizePoint
