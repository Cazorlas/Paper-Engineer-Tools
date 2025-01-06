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
"""-------------------------------------------------------------------------------------------"""


class MainForm(Form):
    def __init__(self):
        self.InitializeComponent()

    def InitializeComponent(self):
        # Get the directory of the running script
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "icon.ico")

        # Load custom icon (if available)
        if os.path.exists(icon_path):
            self.Icon = Icon(icon_path)

        self._currentIndex = System.Windows.Forms.Label()
        self._maxIndex = System.Windows.Forms.Label()
        self._label1 = System.Windows.Forms.Label()
        self._progressBar = System.Windows.Forms.ProgressBar()
        self.SuspendLayout()
        #
        # currentIndex
        #
        self._currentIndex.Location = System.Drawing.Point(133, 27)
        self._currentIndex.Name = "currentIndex"
        self._currentIndex.Size = System.Drawing.Size(86, 23)
        self._currentIndex.TabIndex = 2
        self._currentIndex.Text = "label1"
        self._currentIndex.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        self._currentIndex.Click += self.CurrentIndexClick
        #
        # maxIndex
        #
        self._maxIndex.Location = System.Drawing.Point(213, 27)
        self._maxIndex.Name = "maxIndex"
        self._maxIndex.Size = System.Drawing.Size(86, 23)
        self._maxIndex.TabIndex = 2
        self._maxIndex.Text = "label1"
        self._maxIndex.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        self._maxIndex.Click += self.MaxIndexClick
        #
        # label1
        #
        self._label1.Location = System.Drawing.Point(209, 32)
        self._label1.Name = "label1"
        self._label1.Size = System.Drawing.Size(10, 18)
        self._label1.TabIndex = 3
        self._label1.Text = "/"
        #
        # progressBar
        #
        self._progressBar.Location = System.Drawing.Point(36, 53)
        self._progressBar.Name = "progressBar"
        self._progressBar.Size = System.Drawing.Size(352, 34)
        self._progressBar.Step = 1
        self._progressBar.Style = System.Windows.Forms.ProgressBarStyle.Continuous

        self._progressBar.TabIndex = 1
        self._progressBar.Click += self.ProgressBarClick
        #
        # MainForm
        #
        self.ClientSize = System.Drawing.Size(421, 118)
        self.Controls.Add(self._label1)
        self.Controls.Add(self._maxIndex)
        self.Controls.Add(self._currentIndex)
        self.Controls.Add(self._progressBar)
        self.Name = "MainForm"
        self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
        self.Text = "Place Family as per CAD file"

        self.ResumeLayout(False)

    def UpdateProgress(self, value, max_value):
        """Update the progress bar and labels."""
        self._progressBar.Maximum = max_value
        self._progressBar.Value = value
        self._currentIndex.Text = str(value)
        self._maxIndex.Text = str(max_value)
        self.Refresh()  # Refresh UI for immediate update

    def ProgressBarClick(self, sender, e):
        pass

    def MaxIndexClick(self, sender, e):
        pass

    def CurrentIndexClick(self, sender, e):
        pass
