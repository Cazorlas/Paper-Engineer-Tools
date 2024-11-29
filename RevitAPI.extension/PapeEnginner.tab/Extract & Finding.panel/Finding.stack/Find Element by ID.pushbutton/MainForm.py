# -*- coding: utf-8 -*-
from mailbox import Message

import clr
import System
import string
from rpw.ui.forms import Alert

from SubForm import *

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
comboLst = ["None"]

# Main form class
class MainForm(Form):
    def __init__(self, nameModel):
        self.nameModel = nameModel
        self.InitializeComponent()

    def InitializeComponent(self):
        # Get the directory of the running script
        script_dir = os.path.dirname(__file__)

        icon_path = os.path.join(script_dir, "icon.ico")

        # Load custom icon (if available)
        if os.path.exists(icon_path):
            self.Icon = Icon(icon_path)

        # Initialize components
        self._groupBox1 = System.Windows.Forms.GroupBox()
        self._comboBox1 = System.Windows.Forms.ComboBox()
        self._label1 = System.Windows.Forms.Label()
        self._label2 = System.Windows.Forms.Label()
        self._textBox1 = System.Windows.Forms.TextBox()
        self._okBtn = System.Windows.Forms.Button()
        self._cancelBtn = System.Windows.Forms.Button()
        self._linkLabel1 = System.Windows.Forms.LinkLabel()
        self._linkBtn = System.Windows.Forms.RadioButton()
        self._modelBtn = System.Windows.Forms.RadioButton()
        self._label3 = System.Windows.Forms.Label()
        self._groupBox1.SuspendLayout()
        self.SuspendLayout()
        #
        # groupBox1
        #
        self._groupBox1.Controls.Add(self._label3)
        self._groupBox1.Controls.Add(self._textBox1)
        self._groupBox1.Controls.Add(self._label1)
        self._groupBox1.Controls.Add(self._label2)
        self._groupBox1.Controls.Add(self._comboBox1)
        self._groupBox1.Location = System.Drawing.Point(12, 12)
        self._groupBox1.Name = "groupBox1"
        self._groupBox1.Size = System.Drawing.Size(490, 137)
        self._groupBox1.TabIndex = 0
        self._groupBox1.TabStop = False
        self._groupBox1.Text = "Data"
        #
        # comboBox1
        #
        self._comboBox1.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
        self._comboBox1.FormattingEnabled = True
        self._comboBox1.Location = System.Drawing.Point(141, 60)
        self._comboBox1.Name = "comboBox1"
        self._comboBox1.Size = System.Drawing.Size(343, 21)
        self._comboBox1.Items.AddRange(System.Array[System.Object](comboLst))
        self._comboBox1.SelectedIndex = 0
        self._comboBox1.TabIndex = 0
        self._comboBox1.SelectedIndexChanged += self.ComboBox1SelectedIndexChanged
        #
        # label1
        #
        self._label1.Location = System.Drawing.Point(6, 60)
        self._label1.Name = "label1"
        self._label1.Size = System.Drawing.Size(129, 23)
        self._label1.TabIndex = 1
        self._label1.Text = "Select Linked Model"
        #
        # label2
        #
        self._label2.Location = System.Drawing.Point(6, 31)
        self._label2.Name = "label2"
        self._label2.Size = System.Drawing.Size(129, 23)
        self._label2.TabIndex = 1
        self._label2.Text = "Type ID to Find"
        #
        # textBox1
        #
        self._textBox1.Location = System.Drawing.Point(141, 28)
        self._textBox1.Name = "textBox1"
        self._textBox1.Size = System.Drawing.Size(343, 20)
        self._textBox1.TabIndex = 2
        self._textBox1.TextChanged += self.TextBox1TextChanged
        #
        # okBtn
        #
        self._okBtn.Font = System.Drawing.Font("Microsoft Sans Serif", 10, System.Drawing.FontStyle.Regular,
                                               System.Drawing.GraphicsUnit.Point, 0)
        self._okBtn.Location = System.Drawing.Point(14, 155)
        self._okBtn.Name = "okBtn"
        self._okBtn.Size = System.Drawing.Size(97, 38)
        self._okBtn.TabIndex = 1
        self._okBtn.Text = "Find"
        self._okBtn.UseVisualStyleBackColor = True
        self._okBtn.Click += self.OkBtnClick
        #
        # cancelBtn
        #
        self._cancelBtn.DialogResult = System.Windows.Forms.DialogResult.Cancel
        self._cancelBtn.Font = System.Drawing.Font("Microsoft Sans Serif", 10, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._cancelBtn.Location = System.Drawing.Point(141, 155)
        self._cancelBtn.Name = "cancelBtn"
        self._cancelBtn.Size = System.Drawing.Size(97, 38)
        self._cancelBtn.TabIndex = 1
        self._cancelBtn.Text = "Cancel"
        self._cancelBtn.UseVisualStyleBackColor = True
        self._cancelBtn.Click += self.CancelBtnClick
        #
        # linkLabel1
        #
        self._linkLabel1.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Italic,
                                                    System.Drawing.GraphicsUnit.Point, 0)
        self._linkLabel1.Location = System.Drawing.Point(21, 209)
        self._linkLabel1.Name = "linkLabel1"
        self._linkLabel1.Size = System.Drawing.Size(140, 40)
        self._linkLabel1.TabIndex = 2
        self._linkLabel1.TabStop = True
        self._linkLabel1.Text = "Help"
        self._linkLabel1.LinkClicked += self.LinkLabel1LinkClicked
        #
        # linkBtn
        #

        self._linkBtn.Font = System.Drawing.Font("Microsoft Sans Serif", 10, System.Drawing.FontStyle.Regular,
                                                 System.Drawing.GraphicsUnit.Point, 0)
        self._linkBtn.Location = System.Drawing.Point(274, 159)
        self._linkBtn.Name = "linkBtn"
        self._linkBtn.Size = System.Drawing.Size(111, 31)
        self._linkBtn.TabIndex = 3

        self._linkBtn.Text = "Link File"
        self._linkBtn.UseVisualStyleBackColor = True
        self._linkBtn.CheckedChanged += self.LinkBtnCheckedChanged
        #
        # modelBtn
        #
        self._modelBtn.Checked = True
        self._modelBtn.Font = System.Drawing.Font("Microsoft Sans Serif", 10, System.Drawing.FontStyle.Regular,
                                                  System.Drawing.GraphicsUnit.Point, 0)
        self._modelBtn.Location = System.Drawing.Point(391, 159)
        self._modelBtn.Name = "modelBtn"
        self._modelBtn.Size = System.Drawing.Size(111, 31)
        self._modelBtn.TabIndex = 3
        self._modelBtn.TabStop = True
        self._modelBtn.Text = "In Model"
        self._modelBtn.UseVisualStyleBackColor = True
        self._modelBtn.CheckedChanged += self.ModelBtnCheckedChanged
        #
        # label3
        #
        self._label3.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                System.Drawing.GraphicsUnit.Point, 0)
        self._label3.Location = System.Drawing.Point(141, 103)
        self._label3.Name = "label3"
        self._label3.Size = System.Drawing.Size(343, 17)
        self._label3.TabIndex = 3
        self._label3.Text = '*ID need to be fiiled and can be separated by comma ","'
        #
        # MainForm
        #
        self.AcceptButton = self._okBtn
        self.CancelButton = self._cancelBtn
        self.ClientSize = System.Drawing.Size(515, 236)
        self.Controls.Add(self._modelBtn)
        self.Controls.Add(self._linkBtn)
        self.Controls.Add(self._linkLabel1)
        self.Controls.Add(self._cancelBtn)
        self.Controls.Add(self._okBtn)
        self.Controls.Add(self._groupBox1)
        self.HelpButton = True
        self.MaximumSize = System.Drawing.Size(530, 275)
        self.MinimumSize = System.Drawing.Size(530, 275)
        self.Name = "MainForm"
        self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
        self.Text = "Finding Element by ID"
        self._groupBox1.ResumeLayout(False)
        self._groupBox1.PerformLayout()
        self.ResumeLayout(False)

    def TextBox1TextChanged(self, sender, e):
        pass

    def ComboBox1SelectedIndexChanged(self, sender, e):
        pass

    def OkBtnClick(self, sender, e):
        lstId = self._textBox1.Text.strip()

        try:
            # Check List Id is empty or not
            if not lstId:
                ShowNotification("Warning", "Please enter a valid ID.")
                return

            # Check Id is valid or not
            id = [int(id.strip()) for id in lstId.split(",") if id.strip().isdigit()]
            if not id:
                ShowNotification("Warning", "Vui lòng nhập ít nhất một ID hợp lệ.")
                return

            # Check ComboList is valid or not
            if self._comboBox1.SelectedIndex < 0:
                ShowNotification("Warning", "Vui lòng chọn một mô hình từ danh sách.")
                return

            # Save and close form
            self.DialogResult = System.Windows.Forms.DialogResult.OK
            self.Close()



        except Exception as ex:
            ShowNotification("Error", "An error occurred: {}".format(ex))

    def CancelBtnClick(self, sender, e):
        self.Close()

    def LinkLabel1LinkClicked(self, sender, e):
        System.Diagnostics.Process.Start("https://www.youtube.com/@paper.engineer")

    def LinkBtnCheckedChanged(self, sender, e):
        self._comboBox1.Items.Clear()
        self._comboBox1.Items.AddRange(System.Array[System.Object](self.nameModel))
        self._comboBox1.SelectedIndex = 0

    def ModelBtnCheckedChanged(self, sender, e):
        self._comboBox1.Items.Clear()
        self._comboBox1.Items.AddRange(System.Array[System.Object](comboLst))
        self._comboBox1.SelectedIndex = 0
