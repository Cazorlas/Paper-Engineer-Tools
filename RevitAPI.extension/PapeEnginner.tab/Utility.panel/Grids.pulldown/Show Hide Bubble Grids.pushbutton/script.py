# -*- coding: utf-8 -*-

# Import library and modules
import clr
import System
import math
import string

from MainForm import MainForm

from System.Collections.Generic import *
from pyrevit import forms, revit, script

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import ObjectType

clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Prepare variables and inputs
doc = __revit__.ActiveUIDocument.Document
activeView = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
DB = Autodesk.Revit.DB
output = script.get_output()
unit = doc.GetUnits()
version = int(app.VersionNumber)


# -------------------- FUNCTIONS --------------------

def GetAllViewInSheet():
    """Lấy tất cả các view được đặt trên sheet hiện tại."""
    views_on_sheet = []

    if activeView.ViewType == ViewType.DrawingSheet:
        viewports = FilteredElementCollector(doc, activeView.Id).OfClass(Viewport).ToElements()
        for vp in viewports:
            view_obj = doc.GetElement(vp.ViewId)
            if view_obj:
                views_on_sheet.append(view_obj)
    else:
        views_on_sheet.append("Active view không phải là một sheet.")

    return views_on_sheet


def Flatten(lst):
    """Làm phẳng danh sách lồng nhau."""
    return [i for sublist in lst for i in sublist]


def is_vertical(grid):
    """Xác định grid có phải là lưới dọc không."""
    grid_curve = grid.Curve
    direction = grid_curve.Direction
    return abs(direction.X) < 0.01


def is_horizontal(grid):
    """Xác định grid có phải là lưới ngang không."""
    grid_curve = grid.Curve
    direction = grid_curve.Direction
    return abs(direction.Y) < 0.01


def filter_grids(grids):
    """Phân loại grid thành lưới dọc và lưới ngang."""
    vertical_grids = []
    horizontal_grids = []

    for grid in grids:
        if is_vertical(grid):
            vertical_grids.append(grid)
        if is_horizontal(grid):
            horizontal_grids.append(grid)

    return vertical_grids, horizontal_grids


def CanShowGridInView(grid, view):
    """Kiểm tra xem grid có thể hiển thị trong view không."""
    try:
        return grid.CanBeVisibleInView(view)
    except:
        return False


# -------------------- MAIN CODE --------------------

try:
    # Lấy tất cả các view trong sheet
    allViewInSheet = GetAllViewInSheet()
    grid_activeview = []

    # Thu thập tất cả các grid trong từng view
    for view in allViewInSheet:
        grids = FilteredElementCollector(doc, view.Id).OfClass(Grid).WhereElementIsNotElementType().ToElements()
        grid_activeview.append(grids)

    grid_activeview = Flatten(grid_activeview)


    # Mở form cho người dùng chọn
    f = MainForm()
    f.ShowDialog()

    # Kiểm tra kết quả form
    if f.DialogResult == System.Windows.Forms.DialogResult.OK:
        # Lấy dữ liệu từ form
        left_box = f._LeftBox.Checked
        right_box = f._Rigthbox.Checked
        top_box = f._Topbox.Checked
        bot_box = f._Botbox.Checked

        hide_checked = f._hidebutton.Checked
        show_checked = f._showbutton.Checked

        # Phân loại lưới dọc và ngang
        vertical_grids, horizontal_grids = filter_grids(grid_activeview)

        # Bắt đầu transaction để thực hiện thay đổi
        with Transaction(doc, 'Show/Hide Grid Bubble in All Views') as t:
            t.Start()

            # Duyệt qua tất cả các view hợp lệ
            for view in allViewInSheet:
                if isinstance(view, View) and view.ViewType in [ViewType.FloorPlan, ViewType.CeilingPlan,
                                                                ViewType.Section, ViewType.Elevation]:

                    # Xử lý lưới ngang
                    for grid in horizontal_grids:
                        if CanShowGridInView(grid, view):
                            curve = grid.Curve
                            start_point = curve.GetEndPoint(0)
                            end_point = curve.GetEndPoint(1)

                            # Hiển thị Bubble
                            if show_checked:
                                if left_box and start_point.X > end_point.X:
                                    grid.ShowBubbleInView(DatumEnds.End0, view)
                                if right_box and start_point.X < end_point.X:
                                    grid.ShowBubbleInView(DatumEnds.End1, view)

                            # Ẩn Bubble
                            if hide_checked:
                                if left_box and start_point.X > end_point.X:
                                    grid.HideBubbleInView(DatumEnds.End0, view)
                                if right_box and start_point.X < end_point.X:
                                    grid.HideBubbleInView(DatumEnds.End1, view)

                    # Xử lý lưới dọc
                    for grid in vertical_grids:
                        if CanShowGridInView(grid, view):
                            curve = grid.Curve
                            start_point = curve.GetEndPoint(0)
                            end_point = curve.GetEndPoint(1)

                            # Hiển thị Bubble
                            if show_checked:
                                if top_box and start_point.Y > end_point.Y:
                                    grid.ShowBubbleInView(DatumEnds.End0, view)
                                if bot_box and start_point.Y < end_point.Y:
                                    grid.ShowBubbleInView(DatumEnds.End1, view)

                            # Ẩn Bubble
                            if hide_checked:
                                if top_box and start_point.Y > end_point.Y:
                                    grid.HideBubbleInView(DatumEnds.End0, view)
                                if bot_box and start_point.Y < end_point.Y:
                                    grid.HideBubbleInView(DatumEnds.End1, view)

            # Commit thay đổi
            t.Commit()

except Autodesk.Revit.Exceptions.OperationCanceledException:
    pass

except Exception as ex:
    TaskDialog.Show("Error", "Warning: {}".format(ex))
