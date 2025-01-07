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


# Main form class
# Main form class
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

        # Initialize components
        self._groupBox1 = GroupBox()
        self._radioButton1 = RadioButton()
        self._radioButton2 = RadioButton()
        self._groupBox2 = GroupBox()
        self._LengthInput = TextBox()
        self._label1 = Label()
        self._OKbutton = Button()
        self._Cancelbutton = Button()
        self._linkLabel1 = LinkLabel()
        self._label2 = Label()
        self._groupBox1.SuspendLayout()
        self._groupBox2.SuspendLayout()
        self.SuspendLayout()

        # groupBox1
        self._groupBox1.Controls.Add(self._radioButton2)
        self._groupBox1.Controls.Add(self._radioButton1)
        self._groupBox1.Font = System.Drawing.Font("Microsoft Sans Serif", 10, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._groupBox1.Location = System.Drawing.Point(12, 12)
        self._groupBox1.Name = "groupBox1"
        self._groupBox1.Size = System.Drawing.Size(318, 69)
        self._groupBox1.TabIndex = 0
        self._groupBox1.TabStop = False
        self._groupBox1.Text = "Select Elements"

        # radioButton1 (Auto)
        self._radioButton1.Checked = True
        self._radioButton1.FlatStyle = FlatStyle.System
        self._radioButton1.Location = System.Drawing.Point(63, 32)
        self._radioButton1.Name = "radioButton1"
        self._radioButton1.Size = System.Drawing.Size(104, 24)
        self._radioButton1.TabIndex = 0
        self._radioButton1.TabStop = True
        self._radioButton1.Text = "Auto"
        self._radioButton1.UseVisualStyleBackColor = True
        self._radioButton1.CheckedChanged += self.Autoradiobutton

        # radioButton2 (Manual)
        self._radioButton2.FlatStyle = FlatStyle.System
        self._radioButton2.Location = System.Drawing.Point(208, 32)
        self._radioButton2.Name = "radioButton2"
        self._radioButton2.Size = System.Drawing.Size(104, 24)
        self._radioButton2.TabIndex = 0
        self._radioButton2.Text = "Manual"
        self._radioButton2.UseVisualStyleBackColor = True
        self._radioButton2.CheckedChanged += self.Manualradiobutton

        # groupBox2 for length input
        self._groupBox2.Controls.Add(self._label2)
        self._groupBox2.Controls.Add(self._label1)
        self._groupBox2.Controls.Add(self._LengthInput)
        self._groupBox2.Font = System.Drawing.Font("Microsoft Sans Serif", 10, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._groupBox2.Location = System.Drawing.Point(12, 99)
        self._groupBox2.Name = "groupBox2"
        self._groupBox2.Size = System.Drawing.Size(318, 69)
        self._groupBox2.TabIndex = 0
        self._groupBox2.TabStop = False
        self._groupBox2.Text = "Input Length"

        # LengthInput (TextBox for user input)
        self._LengthInput.Location = System.Drawing.Point(15, 31)
        self._LengthInput.Name = "LengthInput"
        self._LengthInput.Size = System.Drawing.Size(128, 23)
        self._LengthInput.TabIndex = 0
        self._LengthInput.TextChanged += self.LengthInputChanged

        # Label for LengthInput
        self._label1.Location = System.Drawing.Point(199, 34)
        self._label1.Name = "label1"
        self._label1.Size = System.Drawing.Size(100, 23)
        self._label1.TabIndex = 1
        self._label1.Text = "Input Length"

        # Unit label (mm)
        self._label2.Location = System.Drawing.Point(149, 34)
        self._label2.Name = "label2"
        self._label2.Size = System.Drawing.Size(44, 23)
        self._label2.TabIndex = 1
        self._label2.Text = "mm"

        # OKbutton
        self._OKbutton.Font = System.Drawing.Font("Microsoft Sans Serif", 10, System.Drawing.FontStyle.Regular,
                                                  System.Drawing.GraphicsUnit.Point, 0)
        self._OKbutton.Location = System.Drawing.Point(150, 190)
        self._OKbutton.Name = "OKbutton"
        self._OKbutton.Size = System.Drawing.Size(78, 31)
        self._OKbutton.TabIndex = 1
        self._OKbutton.Text = "Run"
        self._OKbutton.UseVisualStyleBackColor = True
        self._OKbutton.Click += self.OKbuttonClick

        # Cancelbutton
        self._Cancelbutton.DialogResult = DialogResult.Cancel
        self._Cancelbutton.Font = System.Drawing.Font("Microsoft Sans Serif", 10, System.Drawing.FontStyle.Regular,
                                                      System.Drawing.GraphicsUnit.Point, 0)
        self._Cancelbutton.Location = System.Drawing.Point(247, 190)
        self._Cancelbutton.Name = "Cancelbutton"
        self._Cancelbutton.Size = System.Drawing.Size(83, 31)
        self._Cancelbutton.TabIndex = 2
        self._Cancelbutton.Text = "Cancel"
        self._Cancelbutton.UseVisualStyleBackColor = True
        self._Cancelbutton.Click += self.CancelbuttonClick

        # linkLabel1 (Help link)
        self._linkLabel1.Location = System.Drawing.Point(12, 243)
        self._linkLabel1.Name = "linkLabel1"
        self._linkLabel1.Size = System.Drawing.Size(100, 23)
        self._linkLabel1.TabIndex = 3
        self._linkLabel1.TabStop = True
        self._linkLabel1.Text = "Help"
        self._linkLabel1.LinkClicked += self.LinkLabel1LinkClicked

        # MainForm layout
        self.AcceptButton = self._OKbutton
        self.BackColor = System.Drawing.SystemColors.Menu
        self.CancelButton = self._Cancelbutton
        self.ClientSize = System.Drawing.Size(342, 266)
        self.Controls.Add(self._linkLabel1)
        self.Controls.Add(self._Cancelbutton)
        self.Controls.Add(self._OKbutton)
        self.Controls.Add(self._groupBox2)
        self.Controls.Add(self._groupBox1)
        self.MaximumSize = System.Drawing.Size(360, 310)
        self.MinimumSize = System.Drawing.Size(360, 310)
        self.ForeColor = System.Drawing.SystemColors.ControlText
        self.HelpButton = True
        self.Name = "MainForm"
        self.StartPosition = FormStartPosition.CenterScreen
        self.Text = "Split Ducts"
        self._groupBox1.ResumeLayout(False)
        self._groupBox2.ResumeLayout(False)
        self._groupBox2.PerformLayout()
        self.ResumeLayout(False)

    # Event handler for Auto selection
    def Autoradiobutton(self, sender, e):
        pass

    # Event handler for Manual selection
    def Manualradiobutton(self, sender, e):
        pass

    # Event handler for LengthInput text change
    def LengthInputChanged(self, sender, e):
        pass

    # Event handler for OK button click
    def OKbuttonClick(self, sender, e):
        length_input = self._LengthInput.Text.strip()  # Trim whitespace

        try:
            length_value = float(length_input)  # Try converting to float
            if length_value <= 0:
                MessageBox.Show('Please enter a length greater than 0.', 'Warning')
            else:
                # Process the input as necessary (e.g., pass length to a duct splitting function)
                self.DialogResult = System.Windows.Forms.DialogResult.OK
                self.Close()

        except ValueError:
            MessageBox.Show('Invalid input. Please enter a numeric value.', 'Warning')

    # Event handler for Cancel button click
    def CancelbuttonClick(self, sender, e):
        """Cancel Button"""
        self.Close()

    # Event handler for Help link click
    def LinkLabel1LinkClicked(self, sender, e):
        System.Diagnostics.Process.Start("https://www.youtube.com/@paper.engineer")
