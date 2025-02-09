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
from pyrevit import forms, revit, script, EXEC_PARAMS

# Excel Libraary
clr.AddReference('Microsoft.Office.Interop.Excel')
from Microsoft.Office.Interop import Excel

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

lstSelect = ["Annotation Categories"]


class InputForm(Form):
    def __init__(self,data):
        self.data = data


        self.InitializeComponent()

    def InitializeComponent(self):
        # Get the directory of the running script
        # script_dir = os.path.dirname(__file__)
        image_path = os.path.join(__commandpath__, "image.jpg")
        icon_path = os.path.join(__commandpath__, "icon.ico")
        # Load custom icon (if available)
        if os.path.exists(icon_path):
            self.Icon = Icon(icon_path)

        self._panel1 = System.Windows.Forms.Panel()
        self._labelFind = System.Windows.Forms.Label()
        self._panel3 = System.Windows.Forms.Panel()
        self._panel2 = System.Windows.Forms.Panel()
        self._textBoxFind = System.Windows.Forms.TextBox()
        self._labelSelect = System.Windows.Forms.Label()
        self._comboBox1 = System.Windows.Forms.ComboBox()
        self._listView1 = System.Windows.Forms.ListView()
        self._btnCheckUncheck = System.Windows.Forms.Button()
        self._btnToggle = System.Windows.Forms.Button()
        self._btnHide = System.Windows.Forms.Button()
        self._tableLayoutPanel31 = System.Windows.Forms.TableLayoutPanel()
        self._btnSave = System.Windows.Forms.Button()
        self._panel1.SuspendLayout()
        self._panel3.SuspendLayout()
        self._panel2.SuspendLayout()
        self._tableLayoutPanel31.SuspendLayout()
        self.SuspendLayout()
        #
        # panel1
        #
        # self._panel1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        self._panel1.Controls.Add(self._comboBox1)
        self._panel1.Controls.Add(self._labelSelect)
        self._panel1.Controls.Add(self._textBoxFind)
        self._panel1.Controls.Add(self._labelFind)
        self._panel1.Dock = System.Windows.Forms.DockStyle.Top
        self._panel1.Location = System.Drawing.Point(0, 0)
        self._panel1.Name = "panel1"
        self._panel1.Size = System.Drawing.Size(507, 82)
        self._panel1.TabIndex = 0
        #
        # panel2
        #
        # self._panel2.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        self._panel2.Padding = System.Windows.Forms.Padding(8,0,8,0)
        self._panel2.Controls.Add(self._listView1)
        self._panel2.Dock = System.Windows.Forms.DockStyle.Fill
        self._panel2.Location = System.Drawing.Point(0, 82)
        self._panel2.Name = "panel2"
        self._panel2.Size = System.Drawing.Size(507, 292)
        self._panel2.TabIndex = 3
        #
        # panel3
        #
        # self._panel3.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        self._panel3.Controls.Add(self._tableLayoutPanel31)
        self._panel3.Dock = System.Windows.Forms.DockStyle.Bottom
        self._panel3.Location = System.Drawing.Point(0, 374)
        self._panel3.Name = "panel3"
        self._panel3.Size = System.Drawing.Size(507, 95)
        self._panel3.TabIndex = 2
        #
        # labelFind
        #
        self._labelFind.Font = System.Drawing.Font("Microsoft Sans Serif", 10, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._labelFind.Location = System.Drawing.Point(12, 12)
        self._labelFind.Name = "labelFind"
        self._labelFind.Size = System.Drawing.Size(60, 23)
        self._labelFind.TabIndex = 0
        self._labelFind.Text = "Find:"
        #
        # textBoxFind
        #
        self._textBoxFind.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
        self._textBoxFind.Font = System.Drawing.Font("Microsoft Sans Serif", 10, System.Drawing.FontStyle.Regular,
                                                     System.Drawing.GraphicsUnit.Point, 0)
        self._textBoxFind.Location = System.Drawing.Point(78, 12)
        self._textBoxFind.Name = "textBoxFind"
        self._textBoxFind.ScrollBars = System.Windows.Forms.ScrollBars.Both
        self._textBoxFind.Size = System.Drawing.Size(416, 23)
        self._textBoxFind.TabIndex = 1
        self._textBoxFind.TextChanged += self.TextBoxFindTextChanged
        #
        # labelSelect
        #
        self._labelSelect.Font = System.Drawing.Font("Microsoft Sans Serif", 10, System.Drawing.FontStyle.Regular,
                                                     System.Drawing.GraphicsUnit.Point, 0)
        self._labelSelect.Location = System.Drawing.Point(12, 41)
        self._labelSelect.Name = "labelSelect"
        self._labelSelect.Size = System.Drawing.Size(58, 15)
        self._labelSelect.TabIndex = 0
        self._labelSelect.Text = "Select:"
        #
        # comboBox1
        #
        self._comboBox1.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
        self._comboBox1.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
        self._comboBox1.FormattingEnabled = True
        self._comboBox1.Location = System.Drawing.Point(78, 40)
        self._comboBox1.Name = "comboBox1"
        self._comboBox1.Size = System.Drawing.Size(416, 24)
        self._comboBox1.Items.AddRange(System.Array[System.Object](lstSelect))
        self._comboBox1.TabIndex = 2
        self._comboBox1.SelectedIndexChanged += self.ComboBox1SelectedIndexChanged
        #
        # listView1
        #
        self._listView1.CheckBoxes = True
        self._listView1.Dock = System.Windows.Forms.DockStyle.Fill
        self._listView1.FullRowSelect = True
        self._listView1.HeaderStyle = System.Windows.Forms.ColumnHeaderStyle.None
        self._listView1.Location = System.Drawing.Point(8, 8)
        self._listView1.Margin = System.Windows.Forms.Padding(5)
        self._listView1.Name = "listView1"
        self._listView1.ShowItemToolTips = True
        self._listView1.Size = System.Drawing.Size(489, 274)
        self._listView1.TabIndex = 0
        self._listView1.UseCompatibleStateImageBehavior = False
        self._listView1.View = System.Windows.Forms.View.Details

        # Sau khi thêm cột vào ListView
        self._listView1.Columns.Add("Data", 600, System.Windows.Forms.HorizontalAlignment.Left)
        # Đăng ký sự kiện Resize để cột luôn chiếm toàn bộ chiều rộng của ListView
        self._listView1.Resize += self.ListViewResize

        for item in self.data:
            self._listView1.Items.Add(ListViewItem(str(item)))

        self._listView1.SelectedIndexChanged += self.ListView1SelectedIndexChanged
        #
        # btnCheckUncheck
        #
        self._btnCheckUncheck.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right
        self._btnCheckUncheck.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
        self._btnCheckUncheck.Location = System.Drawing.Point(8, 8)
        self._btnCheckUncheck.Name = "btnCheckUncheck"
        self._btnCheckUncheck.Size = System.Drawing.Size(157, 35)
        self._btnCheckUncheck.TabIndex = 0
        self._btnCheckUncheck.Text = "Check/Uncheck All"
        self._btnCheckUncheck.UseVisualStyleBackColor = True
        self._btnCheckUncheck.Click += self.BtnCheckUncheckClick
        #
        # btnToggle
        #
        self._btnToggle.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right
        self._btnToggle.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
        self._btnToggle.Location = System.Drawing.Point(171, 8)
        self._btnToggle.Name = "btnToggle"
        self._btnToggle.Size = System.Drawing.Size(162, 35)
        self._btnToggle.TabIndex = 0
        self._btnToggle.Text = "Toggle All"
        self._btnToggle.UseVisualStyleBackColor = True
        self._btnToggle.Click += self.BtnToggleClick
        #
        # btnHide
        #
        self._btnHide.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right
        self._btnHide.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
        self._btnHide.Location = System.Drawing.Point(339, 8)
        self._btnHide.Name = "btnHide"
        self._btnHide.Size = System.Drawing.Size(158, 35)
        self._btnHide.TabIndex = 0
        self._btnHide.Text = "Hide Unselected"
        self._btnHide.UseVisualStyleBackColor = True
        self._btnHide.Click += self.BtnHideClick
        #
        # btnSave
        #
        self._btnSave.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right
        self._btnSave.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
        self._btnSave.Location = System.Drawing.Point(171, 49)
        self._btnSave.Name = "btnSave"
        self._btnSave.Size = System.Drawing.Size(162, 35)
        self._btnSave.TabIndex = 0
        self._btnSave.Text = "Save"
        self._btnSave.UseVisualStyleBackColor = True
        self._btnSave.Click += self.BtnSaveClick
        #
        # tableLayoutPanel31
        #
        self._tableLayoutPanel31.ColumnCount = 3
        self._tableLayoutPanel31.ColumnStyles.Add(
            System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33))
        self._tableLayoutPanel31.ColumnStyles.Add(
            System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 34))
        self._tableLayoutPanel31.ColumnStyles.Add(
            System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 33))
        self._tableLayoutPanel31.Controls.Add(self._btnToggle, 1, 0)
        self._tableLayoutPanel31.Controls.Add(self._btnCheckUncheck, 0, 0)
        self._tableLayoutPanel31.Controls.Add(self._btnHide, 3, 0)
        self._tableLayoutPanel31.Controls.Add(self._btnSave, 0, 1)
        self._tableLayoutPanel31.SetColumnSpan(self._btnSave, 3)
        self._tableLayoutPanel31.Dock = System.Windows.Forms.DockStyle.Fill
        self._tableLayoutPanel31.Location = System.Drawing.Point(0, 0)
        self._tableLayoutPanel31.Name = "tableLayoutPanel31"
        self._tableLayoutPanel31.Padding = System.Windows.Forms.Padding(5)
        self._tableLayoutPanel31.RowCount = 2
        self._tableLayoutPanel31.RowStyles.Add(System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50))
        self._tableLayoutPanel31.RowStyles.Add(System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50))
        self._tableLayoutPanel31.Size = System.Drawing.Size(505, 93)
        self._tableLayoutPanel31.TabIndex = 0
        #
        # InputForm
        #
        self.AcceptButton = self._btnSave
        self.BackColor = System.Drawing.SystemColors.ControlLightLight
        self.ClientSize = System.Drawing.Size(507, 469)
        self.MinimumSize = self.Size
        self.Controls.Add(self._panel2)
        self.Controls.Add(self._panel3)
        self.Controls.Add(self._panel1)
        self.Font = System.Drawing.Font("Microsoft Sans Serif", 10, System.Drawing.FontStyle.Regular,
                                        System.Drawing.GraphicsUnit.Point, 0)
        self.KeyPreview = True
        self.Name = "InputForm"
        self.Text = "Setting Check Tag"
        self._panel1.ResumeLayout(False)
        self._panel1.PerformLayout()
        self._panel3.ResumeLayout(False)
        self._panel2.ResumeLayout(False)
        self._tableLayoutPanel31.ResumeLayout(False)
        self.ResumeLayout(False)

    def TextBoxFindTextChanged(self, sender, e):
        pass

    def ComboBox1SelectedIndexChanged(self, sender, e):
        pass

    def ListView1SelectedIndexChanged(self, sender, e):
        pass

    def BtnCheckUncheckClick(self, sender, e):
        pass

    def BtnToggleClick(self, sender, e):
        pass

    def BtnHideClick(self, sender, e):
        pass

    def BtnSaveClick(self, sender, e):
        pass

    def TextBoxFindTextChanged(self, sender, e):
        pass

    def ComboBox1SelectedIndexChanged(self, sender, e):
        pass

    def ListView1SelectedIndexChanged(self, sender, e):
        pass

    def BtnCheckUncheckClick(self, sender, e):
        pass

    def BtnToggleClick(self, sender, e):
        pass

    def BtnHideClick(self, sender, e):
        pass

    def BtnSaveClick(self, sender, e):
        pass

    def ListViewResize(self, sender, e):
        sender.Columns[0].Width = sender.ClientSize.Width
