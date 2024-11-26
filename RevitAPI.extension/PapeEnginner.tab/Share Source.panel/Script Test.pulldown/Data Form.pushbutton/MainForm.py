# -*- coding: utf-8 -*-
from mailbox import Message

import clr
import System
import string
from rpw.ui.forms import Alert



# Importing necessary references for Revit and Windows Forms
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import *

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

import System.Drawing
import System.Windows.Forms
import os
from System.Drawing import Icon  # Import Icon class
import System.Diagnostics  # Open Link when press Button

from System.Drawing import *
from System.Windows.Forms import *

# Adding a reference to the system to use List
clr.AddReference('System')
from System.Collections.Generic import List

"""---------------------------Get active document and view from Revit------------------------"""
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
uiviews = uidoc.GetOpenUIViews()
uiview = [x for x in uiviews if x.ViewId == view.Id][0]
"""-------------------------------------------------------------------------------------------"""


# Main form class
class MainForm(Form):
    def __init__(self, lstEle):
        self.lstEle = lstEle
        self.InitializeComponent()

    def InitializeComponent(self):
        # Get the directory of the running script
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "icon.ico")
        # Load custom icon (if available)
        if os.path.exists(icon_path):
            self.Icon = Icon(icon_path)

        # Create DataGridView and columns
        self._dataGridView1 = System.Windows.Forms.DataGridView()
        self._Column1 = System.Windows.Forms.DataGridViewTextBoxColumn()
        self._Column2 = System.Windows.Forms.DataGridViewTextBoxColumn()
        self._Column3 = System.Windows.Forms.DataGridViewButtonColumn()  # Define as ButtonColumn

        self._dataGridView1.BeginInit()
        self.SuspendLayout()

        # Configure DataGridView
        self._dataGridView1.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize
        self._dataGridView1.Columns.AddRange(System.Array[System.Windows.Forms.DataGridViewColumn](
            [self._Column1, self._Column2, self._Column3]))

        # Add rows dynamically for each element
        for ele in self.lstEle:
            self._dataGridView1.Rows.Add(ele.Name, ele.Id.IntegerValue)  # Add "Zoom" button text

        # Configure layout and DataGridView
        self._dataGridView1.Dock = System.Windows.Forms.DockStyle.Fill
        self._dataGridView1.Location = System.Drawing.Point(0, 0)
        self._dataGridView1.Name = "dataGridView1"
        self._dataGridView1.Size = System.Drawing.Size(702, 384)
        self._dataGridView1.TabIndex = 1
        self._dataGridView1.CellContentClick += self.DataGridView1CellContentClick  # Bind click event

        # Define Columns
        self._Column1.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.Fill
        self._Column1.HeaderText = "Name Element"
        self._Column1.Name = "Column1"

        self._Column2.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.Fill
        self._Column2.HeaderText = "ID Element"
        self._Column2.Name = "Column2"

        self._Column3.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.Fill
        self._Column3.HeaderText = "Zoom Element"
        self._Column3.Name = "Column3"
        self._Column3.Text = "Zoom"  # Set button text
        self._Column3.UseColumnTextForButtonValue = True  # Display button text

        # Setup Form
        self.ClientSize = System.Drawing.Size(702, 384)
        self.Controls.Add(self._dataGridView1)
        self.Name = "MainForm"
        self.Text = "SubForm"
        self._dataGridView1.EndInit()
        self.ResumeLayout(False)

    def DataGridView1CellContentClick(self, sender, e):
        """Handles button clicks in the Zoom column."""
        if e.ColumnIndex == 2:  # If the "Zoom Element" column button is clicked
            selectedRow = sender.Rows[e.RowIndex]
            elementId = int(selectedRow.Cells[1].Value)  # Retrieve the element ID
            element = doc.GetElement(ElementId(elementId))
            if element and hasattr(element, "get_BoundingBox"):
                bbox = element.get_BoundingBox(None)
                if bbox:
                    # Convert BoundingBox to global coordinates
                    pt1 = XYZ(bbox.Min.X, bbox.Min.Y, bbox.Min.Z)
                    pt2 = XYZ(bbox.Max.X, bbox.Max.Y, bbox.Max.Z)
                    uiview.ZoomAndCenterRectangle(pt1, pt2)

