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



