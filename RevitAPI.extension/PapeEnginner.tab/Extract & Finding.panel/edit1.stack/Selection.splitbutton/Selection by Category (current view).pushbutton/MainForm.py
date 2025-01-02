# -*- coding: utf-8 -*-
from mailbox import Message

import clr
import System
import string
from rpw.ui.forms import Alert

from SubForm import *
from pyrevit import forms, revit, script

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

"""------------------------------------------------------------------------------------------"""


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

        self._listView = System.Windows.Forms.ListView()
        self._categoryHeader = System.Windows.Forms.ColumnHeader()
        self._textBox1 = System.Windows.Forms.TextBox()
        self._labelFind = System.Windows.Forms.Label()
        self._btnOk = System.Windows.Forms.Button()
        self._btnCancel = System.Windows.Forms.Button()
        self._labelNotice = System.Windows.Forms.Label()
        self.SuspendLayout()
        #
        # listView
        #
        self._listView.CheckBoxes = True
        self._listView.Columns.AddRange(System.Array[System.Windows.Forms.ColumnHeader](
            [self._categoryHeader]))
        self._listView.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                  System.Drawing.GraphicsUnit.Point, 0)
        self._listView.HoverSelection = True
        self._listView.Location = System.Drawing.Point(4, 12)
        self._listView.Name = "listView"
        self._listView.Size = System.Drawing.Size(252, 159)
        self._listView.TabIndex = 0
        self._listView.UseCompatibleStateImageBehavior = False
        self._listView.View = System.Windows.Forms.View.Details
        self._listView.SelectedIndexChanged += self.ListViewSelectedIndexChanged
        #
        # categoryHeader
        #
        self._categoryHeader.Text = "Category"
        self._categoryHeader.Width = 223
        #
        # textBox1
        #
        self._textBox1.Location = System.Drawing.Point(276, 58)
        self._textBox1.Name = "textBox1"
        self._textBox1.Size = System.Drawing.Size(149, 20)
        self._textBox1.TabIndex = 1
        self._textBox1.TextChanged += self.TextBox1TextChanged
        #
        # labelFind
        #
        self._labelFind.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._labelFind.Location = System.Drawing.Point(431, 52)
        self._labelFind.Name = "labelFind"
        self._labelFind.Size = System.Drawing.Size(45, 29)
        self._labelFind.TabIndex = 2
        self._labelFind.Text = "Find"
        self._labelFind.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        self._labelFind.Click += self.Label1Click
        #
        # btnOk
        #
        self._btnOk.BackColor = System.Drawing.SystemColors.ActiveCaption
        self._btnOk.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                               System.Drawing.GraphicsUnit.Point, 0)
        self._btnOk.Location = System.Drawing.Point(276, 100)
        self._btnOk.Name = "btnOk"
        self._btnOk.Size = System.Drawing.Size(137, 28)
        self._btnOk.TabIndex = 3
        self._btnOk.Text = "Select"
        self._btnOk.UseVisualStyleBackColor = False
        self._btnOk.Click += self.BtnOkClick
        #
        # btnCancel
        #
        self._btnCancel.BackColor = System.Drawing.SystemColors.ActiveCaption
        self._btnCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
        self._btnCancel.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._btnCancel.Location = System.Drawing.Point(276, 143)
        self._btnCancel.Name = "btnCancel"
        self._btnCancel.Size = System.Drawing.Size(137, 28)
        self._btnCancel.TabIndex = 3
        self._btnCancel.Text = "Cancel"
        self._btnCancel.UseVisualStyleBackColor = False
        self._btnCancel.Click += self.BtnCancelClick
        #
        # labelNotice
        #
        self._labelNotice.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Italic,
                                                     System.Drawing.GraphicsUnit.Point, 0)
        self._labelNotice.Location = System.Drawing.Point(276, 12)
        self._labelNotice.Name = "labelNotice"
        self._labelNotice.Size = System.Drawing.Size(184, 23)
        self._labelNotice.TabIndex = 4
        self._labelNotice.Text = "@PaperEngineer"
        self._labelNotice.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        #
        # MainForm
        #
        self.AcceptButton = self._btnOk
        self.BackColor = System.Drawing.SystemColors.Control
        self.CancelButton = self._btnCancel
        self.ClientSize = System.Drawing.Size(472, 183)
        self.Controls.Add(self._labelNotice)
        self.Controls.Add(self._btnCancel)
        self.Controls.Add(self._btnOk)
        self.Controls.Add(self._labelFind)
        self.Controls.Add(self._textBox1)
        self.Controls.Add(self._listView)
        self.Name = "MainForm"
        self.Text = "Category Form"
        self.ResumeLayout(False)
        self.PerformLayout()

    def Label1Click(self, sender, e):
        pass

    def ListViewSelectedIndexChanged(self, sender, e):
        pass

    def TextBox1TextChanged(self, sender, e):
        pass

    def BtnOkClick(self, sender, e):
        pass

    def BtnCancelClick(self, sender, e):
        pass
