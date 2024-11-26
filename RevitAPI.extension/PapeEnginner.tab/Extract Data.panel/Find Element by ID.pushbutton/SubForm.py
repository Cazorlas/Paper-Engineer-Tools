#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
"""---------------------------Functions to call Form------------------------------------------"""


def ShowNotification(title, content):
    """Input: Title of Form, Content of Form. Return a ShowDialog Form"""
    notiForm = NotiForm(title, content)
    notiForm.ShowDialog()


def ShowDataForm(document, lstEleId):
    dataForm = DataForm(document, lstEleId)
    # Get the Revit main window handle and assign as owner
    revitWindowHandle = System.Diagnostics.Process.GetCurrentProcess().MainWindowHandle
    hostWindow = System.Windows.Forms.Control.FromHandle(revitWindowHandle)
    dataForm.Owner = hostWindow  # Set Revit as the form owner

    # Show the form modelessly
    dataForm.Show()
    # f.TopMost = True  # Keep the form on top of Revit


"""----------------------------------All Forms------------------------------------------------"""


# Notification Form
class NotiForm(Form):
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.InitializeComponent()

    def InitializeComponent(self):
        # Get the directory of the running script
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "icon.ico")
        # Load custom icon (if available)
        if os.path.exists(icon_path):
            self.Icon = Icon(icon_path)

        self._panel1 = System.Windows.Forms.Panel()
        self._panel2 = System.Windows.Forms.Panel()
        self._button = System.Windows.Forms.Button()
        self._content = System.Windows.Forms.Label()
        self._panel1.SuspendLayout()
        self._panel2.SuspendLayout()
        self.SuspendLayout()

        # Panel1
        self._panel1.BackColor = System.Drawing.SystemColors.MenuHighlight
        self._panel1.Controls.Add(self._button)
        self._panel1.Dock = System.Windows.Forms.DockStyle.Bottom
        self._panel1.Location = System.Drawing.Point(0, 95)
        self._panel1.Name = "panel1"
        self._panel1.Size = System.Drawing.Size(372, 39)
        self._panel1.TabIndex = 2

        # Panel2
        self._panel2.Controls.Add(self._content)
        self._panel2.Dock = System.Windows.Forms.DockStyle.Fill
        self._panel2.Location = System.Drawing.Point(0, 0)
        self._panel2.Name = "panel2"
        self._panel2.Size = System.Drawing.Size(372, 95)
        self._panel2.TabIndex = 3

        # Button
        self._button.DialogResult = System.Windows.Forms.DialogResult.Cancel
        self._button.Font = System.Drawing.Font("Microsoft Sans Serif", 8.25)
        self._button.Location = System.Drawing.Point(286, 3)
        self._button.Name = "button"
        self._button.Size = System.Drawing.Size(83, 30)
        self._button.TabIndex = 0
        self._button.Text = "Close"
        self._button.UseVisualStyleBackColor = True
        self._button.Click += self.ButtonClick

        # Content
        self._content.Font = System.Drawing.Font("Microsoft Sans Serif", 10)
        self._content.Location = System.Drawing.Point(3, 9)
        self.ClientSize = System.Drawing.Size(372, 134)
        self._content.MaximumSize = System.Drawing.Size(366, 83)
        self._content.MinimumSize = System.Drawing.Size(366, 83)
        self._content.Name = "content"
        self._content.Size = System.Drawing.Size(366, 83)
        self._content.TabIndex = 0
        self._content.Text = self.content

        # Form
        self.CancelButton = self._button
        self.ClientSize = System.Drawing.Size(398, 134)
        self.MaximumSize = System.Drawing.Size(400, 163)
        self.MinimumSize = System.Drawing.Size(400, 163)
        self.Controls.Add(self._panel2)
        self.Controls.Add(self._panel1)
        self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle
        self.Name = "Notification Form"
        self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
        self.Text = self.title
        self._panel1.ResumeLayout(False)
        self._panel2.ResumeLayout(False)
        self.ResumeLayout(False)

    def ButtonClick(self, sender, e):
        self.Close()

    def Panel2Paint(self, sender, e):
        pass

    def ContentClick(self, sender, e):
        pass


# Data Grid Form
class DataForm(Form):
    def __init__(self, document, lstEleId):
        self.document = document
        self.lstEleId = lstEleId
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
        for id in self.lstEleId:

            ele = self.document.GetElement(id)

            if ele:
                nameEle = ele.Name
                # nameEle = str(ele.Name) if hasattr(ele, "Name") else "Unnamed Element"
                idEle = ele.Id.IntegerValue
                zoomText = "Zoom"
            else:
                nameEle = "ID was not found"
                idEle = id.IntegerValue
                zoomText = ""  # Leave zoom button empty for invalid IDs

            self._dataGridView1.Rows.Add(nameEle, idEle, zoomText)

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
        self._Column1.ToolTipText = 'Element Name will show here.\nIf there is no name, it will display "ID was not found"'
        self._Column1.Name = "Column1"

        self._Column2.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.Fill
        self._Column2.HeaderText = "ID Element"
        self._Column2.ToolTipText = "Element ID will show here"
        self._Column2.Name = "Column2"

        self._Column3.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.Fill
        self._Column3.HeaderText = "Zoom Element"
        self._Column3.Name = "Column3"
        self._Column3.Text = "Zoom"  # Set button text
        self._Column3.ToolTipText = "Click to zoom to element. \nIf element was not found, don't try to click"
        self._Column3.UseColumnTextForButtonValue = True  # Display button text

        # Setup Form
        self.ClientSize = System.Drawing.Size(702, 384)
        self.Controls.Add(self._dataGridView1)
        self.Name = "DataForm"
        self.Text = "DataForm"
        self._dataGridView1.EndInit()
        self.ResumeLayout(False)

    def DataGridView1CellContentClick(self, sender, e):
        """Handles button clicks in the Zoom column."""
        if e.ColumnIndex == 2:  # If the "Zoom Element" column button is clicked
            selectedRow = sender.Rows[e.RowIndex]
            elementId = int(selectedRow.Cells[1].Value)  # Retrieve the element ID
            element = self.document.GetElement(ElementId(elementId))

            if element:
                if isinstance(element, RevitLinkInstance):
                    # Handle Revit link transformation
                    linkDoc = element.GetLinkDocument()
                    transform = element.GetTransform()
                    linkElementId = ElementId(int(selectedRow.Cells[1].Value))
                    linkElement = linkDoc.GetElement(linkElementId)

                    if linkElement and hasattr(linkElement, "get_BoundingBox"):
                        bbox = linkElement.get_BoundingBox(None)
                        if bbox:
                            # Apply the transformation to the bounding box
                            pt1 = transform.OfPoint(bbox.Min)
                            pt2 = transform.OfPoint(bbox.Max)
                            uiview.ZoomAndCenterRectangle(pt1, pt2)
                elif hasattr(element, "get_BoundingBox"):
                    # Handle normal elements
                    bbox = element.get_BoundingBox(None)
                    if bbox:
                        pt1 = bbox.Min
                        pt2 = bbox.Max
                        uiview.ZoomAndCenterRectangle(pt1, pt2)
            else:
                ShowNotification("Error", "Element not found or not valid.")
