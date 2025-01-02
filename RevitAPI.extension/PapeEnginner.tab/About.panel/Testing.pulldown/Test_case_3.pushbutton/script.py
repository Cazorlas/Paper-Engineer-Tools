# -*- coding: utf-8 -*-

import clr
import System
import string

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
uiapp = DocumentManager.Instance.CurrentUIApplication
uidoc = uiapp.ActiveUIDocument
doc = uidoc.Document
view = doc.ActiveView

"""-----------------------------------------------------------------------------------------"""


class MainForm(Form):
    def __init__(self):
        self.originalItems = []  # Lưu danh sách gốc

        self.InitializeComponent()

    def InitializeComponent(self):
        self._listViewTAG = System.Windows.Forms.ListView()
        self._viewType = System.Windows.Forms.ColumnHeader()
        self._viewName = System.Windows.Forms.ColumnHeader()
        self._viewId = System.Windows.Forms.ColumnHeader()
        self._textBox1 = System.Windows.Forms.TextBox()
        self._labelTAG = System.Windows.Forms.Label()
        self._groupBoxTAG = System.Windows.Forms.GroupBox()
        self._groupBoxCategory = System.Windows.Forms.GroupBox()
        self._listViewCategory = System.Windows.Forms.ListView()
        self._columnHeader1 = System.Windows.Forms.ColumnHeader()
        self._columnHeader2 = System.Windows.Forms.ColumnHeader()
        self._columnHeader3 = System.Windows.Forms.ColumnHeader()
        self._textBox2 = System.Windows.Forms.TextBox()
        self._labelCategory = System.Windows.Forms.Label()
        self._groupBoxView = System.Windows.Forms.GroupBox()
        self._listViewView = System.Windows.Forms.ListView()
        self._columnHeader4 = System.Windows.Forms.ColumnHeader()
        self._columnHeader5 = System.Windows.Forms.ColumnHeader()
        self._columnHeader6 = System.Windows.Forms.ColumnHeader()
        self._textBoxView = System.Windows.Forms.TextBox()
        self._labelView = System.Windows.Forms.Label()
        self._buttonOK = System.Windows.Forms.Button()
        self._buttonCancel = System.Windows.Forms.Button()
        self._linkLabel = System.Windows.Forms.LinkLabel()
        self._checkBoxTAG = System.Windows.Forms.CheckBox()
        self._checkBoxCategory = System.Windows.Forms.CheckBox()
        self._checkBoxView = System.Windows.Forms.CheckBox()
        self._checkBoxCurrentView = System.Windows.Forms.CheckBox()
        self._groupBoxTAG.SuspendLayout()
        self._groupBoxCategory.SuspendLayout()
        self._groupBoxView.SuspendLayout()
        self.SuspendLayout()
        #
        # listViewTAG
        #
        self._listViewTAG.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
        self._listViewTAG.BackColor = System.Drawing.SystemColors.Window
        self._listViewTAG.CheckBoxes = True
        self._listViewTAG.Columns.AddRange(System.Array[System.Windows.Forms.ColumnHeader](
            [self._viewType,
             self._viewName,
             self._viewId]))
        self._listViewTAG.FullRowSelect = True
        self._listViewTAG.GridLines = True
        self._listViewTAG.Location = System.Drawing.Point(177, 30)
        self._listViewTAG.Name = "listViewTAG"
        self._listViewTAG.ShowItemToolTips = True
        self._listViewTAG.Size = System.Drawing.Size(500, 125)
        self._listViewTAG.TabIndex = 0
        self._listViewTAG.UseCompatibleStateImageBehavior = False
        self._listViewTAG.View = System.Windows.Forms.View.Details
        self._listViewTAG.SelectedIndexChanged += self.ListViewTAGSelectedIndexChanged
        #
        # viewType
        #
        self._viewType.Text = "View Type"
        self._viewType.Width = 97
        #
        # viewName
        #
        self._viewName.Text = "View Name"
        self._viewName.Width = 194
        #
        # viewId
        #
        self._viewId.Text = "View ID"
        self._viewId.Width = 211
        #
        # textBox1
        #
        self._textBox1.Location = System.Drawing.Point(6, 56)
        self._textBox1.Name = "textBox1"
        self._textBox1.Size = System.Drawing.Size(155, 21)
        self._textBox1.TabIndex = 2
        self._textBox1.TextChanged += self.TextBox1TextChanged
        #
        # labelTAG
        #
        self._labelTAG.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                  System.Drawing.GraphicsUnit.Point, 0)
        self._labelTAG.Location = System.Drawing.Point(6, 30)
        self._labelTAG.Name = "labelTAG"
        self._labelTAG.Size = System.Drawing.Size(100, 23)
        self._labelTAG.TabIndex = 3
        self._labelTAG.Text = "Find TAG:"
        #
        # groupBoxTAG
        #
        self._groupBoxTAG.Controls.Add(self._checkBoxTAG)
        self._groupBoxTAG.Controls.Add(self._listViewTAG)
        self._groupBoxTAG.Controls.Add(self._textBox1)
        self._groupBoxTAG.Controls.Add(self._labelTAG)
        self._groupBoxTAG.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                     System.Drawing.GraphicsUnit.Point, 0)
        self._groupBoxTAG.Location = System.Drawing.Point(12, 12)
        self._groupBoxTAG.Name = "groupBoxTAG"
        self._groupBoxTAG.Size = System.Drawing.Size(683, 165)
        self._groupBoxTAG.TabIndex = 5
        self._groupBoxTAG.TabStop = False
        self._groupBoxTAG.Text = "*Select the TAG Type would like to check"
        #
        # groupBoxCategory
        #
        self._groupBoxCategory.Controls.Add(self._checkBoxCategory)
        self._groupBoxCategory.Controls.Add(self._listViewCategory)
        self._groupBoxCategory.Controls.Add(self._textBox2)
        self._groupBoxCategory.Controls.Add(self._labelCategory)
        self._groupBoxCategory.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                          System.Drawing.GraphicsUnit.Point, 0)
        self._groupBoxCategory.Location = System.Drawing.Point(12, 183)
        self._groupBoxCategory.Name = "groupBoxCategory"
        self._groupBoxCategory.Size = System.Drawing.Size(683, 167)
        self._groupBoxCategory.TabIndex = 5
        self._groupBoxCategory.TabStop = False
        self._groupBoxCategory.Text = "*Select the Category Type would like to check"
        #
        # listViewCategory
        #
        self._listViewCategory.BackColor = System.Drawing.SystemColors.Window
        self._listViewCategory.CheckBoxes = True
        self._listViewCategory.Columns.AddRange(System.Array[System.Windows.Forms.ColumnHeader](
            [self._columnHeader1,
             self._columnHeader2,
             self._columnHeader3]))
        self._listViewCategory.FullRowSelect = True
        self._listViewCategory.GridLines = True
        self._listViewCategory.Location = System.Drawing.Point(177, 30)
        self._listViewCategory.Name = "listViewCategory"
        self._listViewCategory.ShowItemToolTips = True
        self._listViewCategory.Size = System.Drawing.Size(500, 126)
        self._listViewCategory.TabIndex = 0
        self._listViewCategory.UseCompatibleStateImageBehavior = False
        self._listViewCategory.View = System.Windows.Forms.View.Details
        self._listViewCategory.SelectedIndexChanged += self.ListViewCategorySelectedIndexChanged
        #
        # columnHeader1
        #
        self._columnHeader1.Text = "View Type"
        self._columnHeader1.Width = 87
        #
        # columnHeader2
        #
        self._columnHeader2.Text = "View Name"
        self._columnHeader2.Width = 243
        #
        # columnHeader3
        #
        self._columnHeader3.Text = "View ID"
        self._columnHeader3.Width = 190
        #
        # textBox2
        #
        self._textBox2.Location = System.Drawing.Point(6, 56)
        self._textBox2.Name = "textBox2"
        self._textBox2.Size = System.Drawing.Size(155, 21)
        self._textBox2.TabIndex = 2
        self._textBox2.TextChanged += self.TextBox2TextChanged
        #
        # labelCategory
        #
        self._labelCategory.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                       System.Drawing.GraphicsUnit.Point, 0)
        self._labelCategory.Location = System.Drawing.Point(6, 30)
        self._labelCategory.Name = "labelCategory"
        self._labelCategory.Size = System.Drawing.Size(100, 23)
        self._labelCategory.TabIndex = 3
        self._labelCategory.Text = "Find Category:"
        #
        # groupBoxView
        #
        self._groupBoxView.Controls.Add(self._checkBoxCurrentView)
        self._groupBoxView.Controls.Add(self._checkBoxView)
        self._groupBoxView.Controls.Add(self._listViewView)
        self._groupBoxView.Controls.Add(self._textBoxView)
        self._groupBoxView.Controls.Add(self._labelView)
        self._groupBoxView.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                      System.Drawing.GraphicsUnit.Point, 0)
        self._groupBoxView.Location = System.Drawing.Point(12, 356)
        self._groupBoxView.Name = "groupBoxView"
        self._groupBoxView.Size = System.Drawing.Size(683, 167)
        self._groupBoxView.TabIndex = 5
        self._groupBoxView.TabStop = False
        self._groupBoxView.Text = "*Select the View would like to check"
        #
        # listViewView
        #
        self._listViewView.BackColor = System.Drawing.SystemColors.Window
        self._listViewView.CheckBoxes = True
        self._listViewView.Columns.AddRange(System.Array[System.Windows.Forms.ColumnHeader](
            [self._columnHeader4,
             self._columnHeader5,
             self._columnHeader6]))
        self._listViewView.FullRowSelect = True
        self._listViewView.GridLines = True
        self._listViewView.Location = System.Drawing.Point(177, 30)
        self._listViewView.Name = "listViewView"
        self._listViewView.ShowItemToolTips = True
        self._listViewView.Size = System.Drawing.Size(500, 126)
        self._listViewView.TabIndex = 0
        self._listViewView.UseCompatibleStateImageBehavior = False
        self._listViewView.View = System.Windows.Forms.View.Details
        self._listViewView.SelectedIndexChanged += self.ListViewViewSelectedIndexChanged
        #
        # columnHeader4
        #
        self._columnHeader4.Text = "View Type"
        self._columnHeader4.Width = 88
        #
        # columnHeader5
        #
        self._columnHeader5.Text = "View Name"
        self._columnHeader5.Width = 231
        #
        # columnHeader6
        #
        self._columnHeader6.Text = "View ID"
        self._columnHeader6.Width = 183
        #
        # textBoxView
        #
        self._textBoxView.Location = System.Drawing.Point(6, 56)
        self._textBoxView.Name = "textBoxView"
        self._textBoxView.Size = System.Drawing.Size(155, 21)
        self._textBoxView.TabIndex = 2
        self._textBoxView.TextChanged += self.TextBoxViewTextChanged
        #
        # labelView
        #
        self._labelView.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._labelView.Location = System.Drawing.Point(6, 30)
        self._labelView.Name = "labelView"
        self._labelView.Size = System.Drawing.Size(100, 23)
        self._labelView.TabIndex = 3
        self._labelView.Text = "Find View:"
        #
        # buttonOK
        #
        self._buttonOK.BackColor = System.Drawing.SystemColors.ActiveCaption
        self._buttonOK.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                  System.Drawing.GraphicsUnit.Point, 0)
        self._buttonOK.Location = System.Drawing.Point(394, 527)
        self._buttonOK.Name = "buttonOK"
        self._buttonOK.Size = System.Drawing.Size(88, 36)
        self._buttonOK.TabIndex = 6
        self._buttonOK.Text = "OK"
        self._buttonOK.UseVisualStyleBackColor = False
        self._buttonOK.Click += self.ButtonOKClick
        #
        # buttonCancel
        #
        self._buttonCancel.BackColor = System.Drawing.SystemColors.ActiveCaption
        self._buttonCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
        self._buttonCancel.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                      System.Drawing.GraphicsUnit.Point, 0)
        self._buttonCancel.Location = System.Drawing.Point(536, 527)
        self._buttonCancel.Name = "buttonCancel"
        self._buttonCancel.Size = System.Drawing.Size(88, 36)
        self._buttonCancel.TabIndex = 7
        self._buttonCancel.Text = "Cancel"
        self._buttonCancel.UseVisualStyleBackColor = False
        self._buttonCancel.Click += self.ButtonCancelClick
        #
        # linkLabel
        #
        self._linkLabel.Location = System.Drawing.Point(12, 543)
        self._linkLabel.Name = "linkLabel"
        self._linkLabel.Size = System.Drawing.Size(100, 23)
        self._linkLabel.TabIndex = 8
        self._linkLabel.TabStop = True
        self._linkLabel.Text = "Help"
        self._linkLabel.LinkClicked += self.LinkLabelLinkClicked
        #
        # checkBoxTAG
        #
        self._checkBoxTAG.Location = System.Drawing.Point(6, 83)
        self._checkBoxTAG.Name = "checkBoxTAG"
        self._checkBoxTAG.Size = System.Drawing.Size(155, 24)
        self._checkBoxTAG.TabIndex = 5
        self._checkBoxTAG.Text = "Select All"
        self._checkBoxTAG.UseVisualStyleBackColor = True
        self._checkBoxTAG.CheckedChanged += self.CheckBoxTAGCheckedChanged
        #
        # checkBoxCategory
        #
        self._checkBoxCategory.Location = System.Drawing.Point(6, 83)
        self._checkBoxCategory.Name = "checkBoxCategory"
        self._checkBoxCategory.Size = System.Drawing.Size(155, 24)
        self._checkBoxCategory.TabIndex = 5
        self._checkBoxCategory.Text = "Select All"
        self._checkBoxCategory.UseVisualStyleBackColor = True
        self._checkBoxCategory.CheckedChanged += self.CheckBoxCategoryCheckedChanged
        #
        # checkBoxView
        #
        self._checkBoxView.Location = System.Drawing.Point(6, 82)
        self._checkBoxView.Name = "checkBoxView"
        self._checkBoxView.Size = System.Drawing.Size(155, 24)
        self._checkBoxView.TabIndex = 5
        self._checkBoxView.Text = "Select All"
        self._checkBoxView.UseVisualStyleBackColor = True
        self._checkBoxView.CheckedChanged += self.CheckBoxViewCheckedChanged
        #
        # checkBoxCurrentView
        #
        self._checkBoxCurrentView.Location = System.Drawing.Point(6, 112)
        self._checkBoxCurrentView.Name = "checkBoxCurrentView"
        self._checkBoxCurrentView.Size = System.Drawing.Size(155, 24)
        self._checkBoxCurrentView.TabIndex = 5
        self._checkBoxCurrentView.Text = "Select Current View"
        self._checkBoxCurrentView.UseVisualStyleBackColor = True
        self._checkBoxCurrentView.CheckedChanged += self.CheckBoxCurrentViewCheckedChanged
        #
        # MainForm
        #
        self.AcceptButton = self._buttonOK
        self.CancelButton = self._buttonCancel
        self.ClientSize = System.Drawing.Size(702, 575)
        self.Controls.Add(self._linkLabel)
        self.Controls.Add(self._buttonCancel)
        self.Controls.Add(self._buttonOK)
        self.Controls.Add(self._groupBoxView)
        self.Controls.Add(self._groupBoxCategory)
        self.Controls.Add(self._groupBoxTAG)
        self.Name = "MainForm"
        self.Text = "Create Check TAG"
        self._groupBoxTAG.ResumeLayout(False)
        self._groupBoxTAG.PerformLayout()
        self._groupBoxCategory.ResumeLayout(False)
        self._groupBoxCategory.PerformLayout()
        self._groupBoxView.ResumeLayout(False)
        self._groupBoxView.PerformLayout()
        self.ResumeLayout(False)

    def TextBox1TextChanged(self, sender, e):
        pass

    def CheckBoxTAGCheckedChanged(self, sender, e):
        pass

    def ListViewTAGSelectedIndexChanged(self, sender, e):
        pass

    def TextBox2TextChanged(self, sender, e):
        pass

    def CheckBoxCategoryCheckedChanged(self, sender, e):
        pass

    def ListViewCategorySelectedIndexChanged(self, sender, e):
        pass

    def TextBoxViewTextChanged(self, sender, e):
        pass

    def CheckBoxViewCheckedChanged(self, sender, e):
        pass

    def CheckBoxCurrentViewCheckedChanged(self, sender, e):
        pass

    def LinkLabelLinkClicked(self, sender, e):
        pass

    def ListViewViewSelectedIndexChanged(self, sender, e):
        pass

    def ButtonOKClick(self, sender, e):
        # Save and close form

        self.DialogResult = System.Windows.Forms.DialogResult.OK
        self.Close()

    def ButtonCancelClick(self, sender, e):
        self.Close()


f = MainForm()
Application.Run(f)
