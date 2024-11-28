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

        self._groupBox1 = System.Windows.Forms.GroupBox()
        self._label1 = System.Windows.Forms.Label()
        self._textBoxData = System.Windows.Forms.TextBox()
        self._groupBox2 = System.Windows.Forms.GroupBox()
        self._radioButtonModel = System.Windows.Forms.RadioButton()
        self._radioButtonLink = System.Windows.Forms.RadioButton()
        self._helpLabel = System.Windows.Forms.LinkLabel()
        self._btnOk = System.Windows.Forms.Button()
        self._btnCancel = System.Windows.Forms.Button()
        self._btnShow = System.Windows.Forms.Button()
        self._groupBox1.SuspendLayout()
        self._groupBox2.SuspendLayout()
        self.SuspendLayout()
        #
        # groupBox1
        #
        self._groupBox1.Controls.Add(self._textBoxData)
        self._groupBox1.Controls.Add(self._label1)
        self._groupBox1.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._groupBox1.Location = System.Drawing.Point(12, 12)
        self._groupBox1.Name = "groupBox1"
        self._groupBox1.Size = System.Drawing.Size(409, 90)
        self._groupBox1.TabIndex = 0
        self._groupBox1.TabStop = False
        self._groupBox1.Text = "Input Data"
        #
        # label1
        #
        self._label1.Location = System.Drawing.Point(6, 28)
        self._label1.Name = "label1"
        self._label1.Size = System.Drawing.Size(397, 23)
        self._label1.TabIndex = 0
        self._label1.Text = "ID - (use semicolon for multiple IDs):"
        #
        # textBoxData
        #
        self._textBoxData.Location = System.Drawing.Point(6, 54)
        self._textBoxData.Name = "textBoxData"
        self._textBoxData.ScrollBars = System.Windows.Forms.ScrollBars.Horizontal
        self._textBoxData.Size = System.Drawing.Size(397, 21)
        self._textBoxData.TabIndex = 1
        self._textBoxData.TextChanged += self.TextBoxDataTextChanged
        #
        # groupBox2
        #
        self._groupBox2.Controls.Add(self._radioButtonLink)
        self._groupBox2.Controls.Add(self._radioButtonModel)
        self._groupBox2.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._groupBox2.Location = System.Drawing.Point(12, 108)
        self._groupBox2.Name = "groupBox2"
        self._groupBox2.Size = System.Drawing.Size(409, 52)
        self._groupBox2.TabIndex = 1
        self._groupBox2.TabStop = False
        self._groupBox2.Text = "Mode"
        #
        # radioButtonModel
        #
        self._radioButtonModel.Checked = True
        self._radioButtonModel.Location = System.Drawing.Point(106, 20)
        self._radioButtonModel.Name = "radioButtonModel"
        self._radioButtonModel.Size = System.Drawing.Size(104, 24)
        self._radioButtonModel.TabIndex = 0
        self._radioButtonModel.TabStop = True
        self._radioButtonModel.Text = "In Model"
        self._radioButtonModel.UseVisualStyleBackColor = True
        self._radioButtonModel.CheckedChanged += self.RadioButtonModelCheckedChanged
        #
        # radioButtonLink
        #
        self._radioButtonLink.Location = System.Drawing.Point(235, 20)
        self._radioButtonLink.Name = "radioButtonLink"
        self._radioButtonLink.Size = System.Drawing.Size(104, 24)
        self._radioButtonLink.TabIndex = 0
        self._radioButtonLink.Text = "Link Model"
        self._radioButtonLink.UseVisualStyleBackColor = True
        self._radioButtonLink.CheckedChanged += self.RadioButtonLinkCheckedChanged
        #
        # helpLabel
        #
        self._helpLabel.Font = System.Drawing.Font("Microsoft Sans Serif", 8.25, System.Drawing.FontStyle.Italic,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._helpLabel.Location = System.Drawing.Point(12, 171)
        self._helpLabel.Name = "helpLabel"
        self._helpLabel.Size = System.Drawing.Size(100, 23)
        self._helpLabel.TabIndex = 2
        self._helpLabel.TabStop = True
        self._helpLabel.Text = "Help"
        self._helpLabel.TextAlign = System.Drawing.ContentAlignment.BottomLeft
        self._helpLabel.LinkClicked += self.HelpLabelLinkClicked
        #
        # btnOk
        #
        self._btnOk.Location = System.Drawing.Point(247, 166)
        self._btnOk.Name = "btnOk"
        self._btnOk.Size = System.Drawing.Size(75, 27)
        self._btnOk.TabIndex = 3
        self._btnOk.Text = "OK"
        self._btnOk.UseVisualStyleBackColor = True
        self._btnOk.Click += self.BtnOkClick
        #
        # btnCancel
        #
        self._btnCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
        self._btnCancel.Location = System.Drawing.Point(340, 166)
        self._btnCancel.Name = "btnCancel"
        self._btnCancel.Size = System.Drawing.Size(75, 27)
        self._btnCancel.TabIndex = 3
        self._btnCancel.Text = "Cancel"
        self._btnCancel.UseVisualStyleBackColor = True
        self._btnCancel.Click += self.BtnCancelClick
        #
        # btnShow
        #
        self._btnShow.Location = System.Drawing.Point(80, 167)
        self._btnShow.Name = "btnShow"
        self._btnShow.Size = System.Drawing.Size(75, 27)
        self._btnShow.TabIndex = 3
        self._btnShow.Text = "Show 3D"
        self._btnShow.UseVisualStyleBackColor = True
        self._btnShow.Click += self.BtnShowClick

        #
        # MainForm
        #
        self.AcceptButton = self._btnOk
        self.CancelButton = self._btnCancel
        self.ClientSize = System.Drawing.Size(428, 205)
        self.Controls.Add(self._btnCancel)
        self.Controls.Add(self._btnShow)
        self.Controls.Add(self._btnOk)
        self.Controls.Add(self._helpLabel)
        self.Controls.Add(self._groupBox2)
        self.Controls.Add(self._groupBox1)
        self.MaximumSize = System.Drawing.Size(444, 244)
        self.MinimumSize = System.Drawing.Size(444, 244)
        self.Name = "MainForm"
        self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
        self.Text = "Select Elements by ID"
        self._groupBox1.ResumeLayout(False)
        self._groupBox1.PerformLayout()
        self._groupBox2.ResumeLayout(False)
        self.ResumeLayout(False)


    def TextBoxDataTextChanged(self, sender, e):
        pass


    def RadioButtonModelCheckedChanged(self, sender, e):
        pass


    def RadioButtonLinkCheckedChanged(self, sender, e):
        pass


    def HelpLabelLinkClicked(self, sender, e):
        System.Diagnostics.Process.Start("https://www.youtube.com/@paper.engineer")


    def BtnShowClick(self, sender, e):
        pass


    def BtnOkClick(self, sender, e):
        lstId = self._textBoxData.Text.strip()

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

            # Save and close form
            self.DialogResult = System.Windows.Forms.DialogResult.OK
            self.Close()

        except Exception as ex:
            ShowNotification("Error", "An error occurred: {}".format(ex))


    def BtnCancelClick(self, sender, e):
        self.Close()
