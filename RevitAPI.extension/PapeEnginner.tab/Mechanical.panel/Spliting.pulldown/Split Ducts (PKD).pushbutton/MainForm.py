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

from SubForm import ShowNotification

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
from System.Windows.Forms import ToolTip
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
    def __init__(self, links):
        self.links = links
        self.InitializeComponent()

    def InitializeComponent(self):
        # Get the directory of the running script
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "icon.ico")

        # Load custom icon (if available)
        if os.path.exists(icon_path):
            self.Icon = Icon(icon_path)

        self._groupBoxMode = System.Windows.Forms.GroupBox()
        self._groupBoxModeSelect = System.Windows.Forms.GroupBox()
        self._radioButtonAuto = System.Windows.Forms.RadioButton()
        self._radioButtonManual = System.Windows.Forms.RadioButton()
        self._radioButtonPlan = System.Windows.Forms.RadioButton()
        self._radioButtonVertical = System.Windows.Forms.RadioButton()
        self._radioButtonAll = System.Windows.Forms.RadioButton()
        self._groupBoxLength = System.Windows.Forms.GroupBox()
        self._textBoxWall = System.Windows.Forms.TextBox()
        self._labelWalls = System.Windows.Forms.Label()
        self._labelStep = System.Windows.Forms.Label()
        self._textBoxStep = System.Windows.Forms.TextBox()
        self._buttonOK = System.Windows.Forms.Button()
        self._buttonCancel = System.Windows.Forms.Button()
        self._linkLabelHelp = System.Windows.Forms.LinkLabel()
        self._groupBoxLink = System.Windows.Forms.GroupBox()
        self._comboBoxLink = System.Windows.Forms.ComboBox()
        self._groupBoxMode.SuspendLayout()
        self._groupBoxModeSelect.SuspendLayout()
        self._groupBoxLength.SuspendLayout()
        self._groupBoxLink.SuspendLayout()
        self.SuspendLayout()
        #
        # groupBoxMode
        #
        self._groupBoxMode.Controls.Add(self._radioButtonManual)
        self._groupBoxMode.Controls.Add(self._radioButtonAuto)
        self._groupBoxMode.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                      System.Drawing.GraphicsUnit.Point, 0)
        self._groupBoxMode.Location = System.Drawing.Point(12, 12)
        self._groupBoxMode.Name = "groupBoxMode"
        self._groupBoxMode.Size = System.Drawing.Size(294, 69)
        self._groupBoxMode.TabIndex = 0
        self._groupBoxMode.TabStop = False
        self._groupBoxMode.Text = "Mode"
        #
        # groupBoxModeSelect
        #
        self._groupBoxModeSelect.Controls.Add(self._radioButtonAll)
        self._groupBoxModeSelect.Controls.Add(self._radioButtonVertical)
        self._groupBoxModeSelect.Controls.Add(self._radioButtonPlan)
        self._groupBoxModeSelect.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                            System.Drawing.GraphicsUnit.Point, 0)
        self._groupBoxModeSelect.Location = System.Drawing.Point(12, 87)
        self._groupBoxModeSelect.Name = "groupBoxModeSelect"
        self._groupBoxModeSelect.Size = System.Drawing.Size(294, 70)
        self._groupBoxModeSelect.TabIndex = 1
        self._groupBoxModeSelect.TabStop = False
        self._groupBoxModeSelect.Enabled = False
        self._groupBoxModeSelect.Text = "Select (Work when you choose Auto Mode)"
        #
        # radioButtonAuto
        #
        self._radioButtonAuto.Location = System.Drawing.Point(67, 30)
        self._radioButtonAuto.Name = "radioButtonAuto"
        self._radioButtonAuto.Size = System.Drawing.Size(104, 24)
        self._radioButtonAuto.TabIndex = 0
        self._radioButtonAuto.Text = "Auto"
        self._radioButtonAuto.UseVisualStyleBackColor = True
        self._radioButtonAuto.CheckedChanged += self.RadioButtonAuto
        self._radioButtonAuto.CheckedChanged += self.RadioButtonCheckedChanged
        #
        # radioButtonManual
        #
        self._radioButtonManual.Checked = True
        self._radioButtonManual.Location = System.Drawing.Point(162, 30)
        self._radioButtonManual.Name = "radioButtonManual"
        self._radioButtonManual.Size = System.Drawing.Size(104, 24)
        self._radioButtonManual.TabIndex = 1
        self._radioButtonManual.TabStop = True
        self._radioButtonManual.Text = "Manual"
        self._radioButtonManual.UseVisualStyleBackColor = True
        self._radioButtonManual.CheckedChanged += self.RadioButtonManual
        self._radioButtonManual.CheckedChanged += self.RadioButtonCheckedChanged
        #
        # radioButtonPlan
        #
        self._radioButtonPlan.Checked = True
        self._radioButtonPlan.Location = System.Drawing.Point(29, 31)
        self._radioButtonPlan.Name = "radioButtonPlan"
        self._radioButtonPlan.Size = System.Drawing.Size(104, 24)
        self._radioButtonPlan.TabIndex = 0
        self._radioButtonPlan.TabStop = True
        self._radioButtonPlan.Text = "Plan"
        self._radioButtonPlan.UseVisualStyleBackColor = True
        self._radioButtonPlan.CheckedChanged += self.RadioButtonPlan
        #
        # radioButtonVertical
        #
        self._radioButtonVertical.Location = System.Drawing.Point(108, 31)
        self._radioButtonVertical.Name = "radioButtonVertical"
        self._radioButtonVertical.Size = System.Drawing.Size(104, 24)
        self._radioButtonVertical.TabIndex = 1
        self._radioButtonVertical.Text = "Vertical"
        self._radioButtonVertical.UseVisualStyleBackColor = True
        self._radioButtonVertical.CheckedChanged += self.RadioButtonVertical
        #
        # radioButtonAll
        #
        self._radioButtonAll.Location = System.Drawing.Point(218, 31)
        self._radioButtonAll.Name = "radioButtonAll"
        self._radioButtonAll.Size = System.Drawing.Size(104, 24)
        self._radioButtonAll.TabIndex = 2
        self._radioButtonAll.Text = "All"
        self._radioButtonAll.UseVisualStyleBackColor = True
        self._radioButtonAll.CheckedChanged += self.RadioButtonAll
        #
        # groupBoxLength
        #
        self._groupBoxLength.Controls.Add(self._labelStep)
        self._groupBoxLength.Controls.Add(self._labelWalls)
        self._groupBoxLength.Controls.Add(self._textBoxStep)
        self._groupBoxLength.Controls.Add(self._textBoxWall)
        self._groupBoxLength.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                        System.Drawing.GraphicsUnit.Point, 0)
        self._groupBoxLength.Location = System.Drawing.Point(12, 239)
        self._groupBoxLength.Name = "groupBoxLength"
        self._groupBoxLength.Size = System.Drawing.Size(294, 92)
        self._groupBoxLength.TabIndex = 2
        self._groupBoxLength.TabStop = False
        self._groupBoxLength.Text = "Step Length"
        #
        # textBoxWall
        #
        self._textBoxWall.Location = System.Drawing.Point(6, 30)
        self._textBoxWall.Name = "textBoxWall"
        self._textBoxWall.ScrollBars = System.Windows.Forms.ScrollBars.Horizontal
        self._textBoxWall.Size = System.Drawing.Size(173, 21)
        self._textBoxWall.TabIndex = 0
        self._textBoxWall.TextChanged += self.TextBoxWallTextChanged
        #
        # labelWalls
        #
        self._labelWalls.Location = System.Drawing.Point(188, 28)
        self._labelWalls.Name = "labelWalls"
        self._labelWalls.Size = System.Drawing.Size(100, 23)
        self._labelWalls.TabIndex = 1
        self._labelWalls.Text = "Offset Walls"
        self._labelWalls.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        #
        # labelStep
        #
        self._labelStep.Location = System.Drawing.Point(188, 55)
        self._labelStep.Name = "labelStep"
        self._textBoxStep.ScrollBars = System.Windows.Forms.ScrollBars.Horizontal
        self._labelStep.Size = System.Drawing.Size(100, 23)
        self._labelStep.TabIndex = 4
        self._labelStep.Text = "Step Duct Length"
        self._labelStep.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        #
        # textBoxStep
        #
        self._textBoxStep.Location = System.Drawing.Point(6, 57)
        self._textBoxStep.Name = "textBoxStep"
        self._textBoxStep.Size = System.Drawing.Size(173, 21)
        self._textBoxStep.TabIndex = 3
        self._textBoxStep.TextChanged += self.TextBoxStepTextChanged
        #
        # groupBoxLink
        #
        self._groupBoxLink.Controls.Add(self._comboBoxLink)
        self._groupBoxLink.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                      System.Drawing.GraphicsUnit.Point, 0)
        self._groupBoxLink.Location = System.Drawing.Point(12, 163)
        self._groupBoxLink.Name = "groupBoxLink"
        self._groupBoxLink.Size = System.Drawing.Size(294, 70)
        self._groupBoxLink.TabIndex = 6
        self._groupBoxLink.TabStop = False
        self._groupBoxLink.Text = "Select Link"
        #
        # comboBoxLink
        #
        self._comboBoxLink.FormattingEnabled = True
        self._comboBoxLink.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
        self._comboBoxLink.Location = System.Drawing.Point(12, 29)
        self._comboBoxLink.Name = "comboBoxLink"
        self._comboBoxLink.Size = System.Drawing.Size(276, 23)
        self._comboBoxLink.Items.AddRange(System.Array[System.Object](self.links))
        self._comboBoxLink.TabIndex = 0
        self._comboBoxLink.SelectedIndex = 0
        self._comboBoxLink.SelectedIndexChanged += self.ComboBoxLinkChanged
        #
        # buttonOK
        #
        self._buttonOK.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                  System.Drawing.GraphicsUnit.Point, 0)
        self._buttonOK.Location = System.Drawing.Point(149, 337)
        self._buttonOK.Name = "buttonOK"
        self._buttonOK.Size = System.Drawing.Size(75, 29)
        self._buttonOK.TabIndex = 3
        self._buttonOK.Text = "OK"
        self._buttonOK.UseVisualStyleBackColor = True
        self._buttonOK.Click += self.ButtonOKClick
        #
        # buttonCancel
        #
        self._buttonCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
        self._buttonCancel.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                      System.Drawing.GraphicsUnit.Point, 0)
        self._buttonCancel.Location = System.Drawing.Point(231, 337)
        self._buttonCancel.Name = "buttonCancel"
        self._buttonCancel.Size = System.Drawing.Size(75, 29)
        self._buttonCancel.TabIndex = 4
        self._buttonCancel.Text = "Cancel"
        self._buttonCancel.UseVisualStyleBackColor = True
        self._buttonCancel.Click += self.ButtonCancelClick
        #
        # linkLabelHelp
        #
        self._linkLabelHelp.Location = System.Drawing.Point(12, 341)
        self._linkLabelHelp.Name = "linkLabelHelp"
        self._linkLabelHelp.Size = System.Drawing.Size(100, 23)
        self._linkLabelHelp.TabIndex = 5
        self._linkLabelHelp.TabStop = True
        self._linkLabelHelp.Text = "Help"
        self._linkLabelHelp.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        self._linkLabelHelp.LinkClicked += self.LinkLabelHelpLinkClicked
        #
        # Tooltip
        #
        self._tooltip = ToolTip()
        self._tooltip.SetToolTip(self._textBoxWall, "Enter the wall length in milimeters.")
        self._tooltip.SetToolTip(self._textBoxStep, "Enter the step length in milimeters.")
        self._tooltip.SetToolTip(self._radioButtonAuto, "Select all ducts in view as per Select Mode")
        self._tooltip.SetToolTip(self._radioButtonManual, "Select ducts by picking")
        self._tooltip.SetToolTip(self._radioButtonPlan, "Select all ducts in view but vertical ducts")
        self._tooltip.SetToolTip(self._radioButtonVertical, "Select all ducts in view but horizontal ducts")
        self._tooltip.SetToolTip(self._radioButtonAll, "Select all ducts in view")
        self._tooltip.SetToolTip(self._comboBoxLink, "Select Link")

        #
        # MainForm
        #
        self.AcceptButton = self._buttonOK
        self.CancelButton = self._buttonCancel
        self.ClientSize = System.Drawing.Size(318, 376)
        self.Controls.Add(self._groupBoxLink)
        self.Controls.Add(self._linkLabelHelp)
        self.Controls.Add(self._buttonCancel)
        self.Controls.Add(self._buttonOK)
        self.Controls.Add(self._groupBoxLength)
        self.Controls.Add(self._groupBoxModeSelect)
        self.Controls.Add(self._groupBoxMode)
        self.HelpButton = True
        self.MaximumSize = System.Drawing.Size(334, 415)
        self.MinimumSize = System.Drawing.Size(334, 415)
        self.Name = "MainForm"
        self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
        self.Text = "Split Ducts (PKD)"
        self._groupBoxMode.ResumeLayout(False)
        self._groupBoxModeSelect.ResumeLayout(False)
        self._groupBoxLength.ResumeLayout(False)
        self._groupBoxLength.PerformLayout()
        self._groupBoxLink.ResumeLayout(False)
        self.ResumeLayout(False)

    def RadioButtonAuto(self, sender, e):
        pass

    def RadioButtonPlan(self, sender, e):
        pass

    def RadioButtonManual(self, sender, e):
        pass

    def RadioButtonVertical(self, sender, e):
        pass

    def RadioButtonAll(self, sender, e):
        pass

    def RadioButtonCheckedChanged(self, sender, e):
        if sender == self._radioButtonAuto:
            self._groupBoxModeSelect.Enabled = True
        elif sender == self._radioButtonManual:
            self._groupBoxModeSelect.Enabled = False

    def TextBoxWallTextChanged(self, sender, e):
        pass

    def TextBoxStepTextChanged(self, sender, e):
        pass

    def ComboBoxLinkChanged(self, sender, e):
        pass

    def LinkLabelHelpLinkClicked(self, sender, e):
        System.Diagnostics.Process.Start("https://www.youtube.com/@paper.engineer")

    def ButtonOKClick(self, sender, e):

        lengthInput = self._textBoxStep.Text.strip()  # Trim whitespace
        wallInput = self._textBoxWall.Text.strip()

        try:

            lengthValue = float(lengthInput)  # Try converting to float
            wallValue = float(wallInput)
            if lengthValue <= 0 or wallValue <= 0:
                ShowNotification('Warning', 'Please enter a valid input Length.')
            else:
                # Process the input as necessary (e.g., pass length to a duct splitting function)
                self.DialogResult = System.Windows.Forms.DialogResult.OK
                self.Close()

        except ValueError:
            ShowNotification('Warning', 'Invalid input. Please enter a numeric value.')

    def ButtonCancelClick(self, sender, e):
        """Cancel Button"""
        self.Close()
