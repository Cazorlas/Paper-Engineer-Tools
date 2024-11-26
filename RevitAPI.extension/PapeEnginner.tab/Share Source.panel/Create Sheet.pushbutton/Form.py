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
clr.AddReference('System.Windows.Forms.DataVisualization')

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
combolst = ["Prefix", "Suffix"]


class MainForm(Form):
    def __init__(self, titleblocks_name):
        self.titleblocks = titleblocks_name  # Score data
        self.InitializeComponent()

    def InitializeComponent(self):
        # Get the directory of the running script
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "icon.ico")  # Assuming icon.ico is in the same folder as Form.py

        # Load custom icon
        self.Icon = Icon(icon_path)
        resources = System.Resources.ResourceManager("Create_Sheets.MainForm",
                                                     System.Reflection.Assembly.GetExecutingAssembly())
        self._label1 = System.Windows.Forms.Label()
        self._textBox1 = System.Windows.Forms.TextBox()
        self._label2 = System.Windows.Forms.Label()
        self._textBox2 = System.Windows.Forms.TextBox()
        self._comboBox1 = System.Windows.Forms.ComboBox()
        self._textBox3 = System.Windows.Forms.TextBox()
        self._checkBox1 = System.Windows.Forms.CheckBox()
        self._checkBox2 = System.Windows.Forms.CheckBox()
        self._textBox4 = System.Windows.Forms.TextBox()
        self._comboBox2 = System.Windows.Forms.ComboBox()
        self._checkBox3 = System.Windows.Forms.CheckBox()
        self._checkBox4 = System.Windows.Forms.CheckBox()
        self._button1 = System.Windows.Forms.Button()
        self._button2 = System.Windows.Forms.Button()
        self._linkLabel1 = System.Windows.Forms.LinkLabel()
        self._checkedListBox1 = System.Windows.Forms.CheckedListBox()
        self._label3 = System.Windows.Forms.Label()
        self._label4 = System.Windows.Forms.Label()
        self._textBox5 = System.Windows.Forms.TextBox()
        self.SuspendLayout()
        #
        # label1
        #
        self._label1.Location = System.Drawing.Point(12, 159)
        self._label1.Name = "label1"
        self._label1.Size = System.Drawing.Size(90, 24)
        self._label1.TabIndex = 0
        self._label1.Text = "Sheet Number:*"
        self._label1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        #
        # textBox1
        #
        self._textBox1.Location = System.Drawing.Point(108, 162)
        self._textBox1.Name = "textBox1"
        self._textBox1.Size = System.Drawing.Size(263, 20)
        self._textBox1.TabIndex = 1
        self._textBox1.TextChanged += self.TextBox1TextChanged
        #
        # label2
        #
        self._label2.Location = System.Drawing.Point(12, 235)
        self._label2.Name = "label2"
        self._label2.Size = System.Drawing.Size(90, 24)
        self._label2.TabIndex = 0
        self._label2.Text = "Sheet Name:*"
        self._label2.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        #
        # textBox2
        #
        self._textBox2.Location = System.Drawing.Point(108, 238)
        self._textBox2.Name = "textBox2"
        self._textBox2.Size = System.Drawing.Size(263, 20)
        self._textBox2.TabIndex = 1
        self._textBox2.TextChanged += self.TextBox2TextChanged
        #
        # comboBox1
        #
        self._comboBox1.FormattingEnabled = True
        self._comboBox1.Location = System.Drawing.Point(12, 199)
        self._comboBox1.Name = "comboBox1"
        self._comboBox1.Size = System.Drawing.Size(90, 21)
        self._comboBox1.TabIndex = 2
        self._comboBox1.Items.AddRange(System.Array[System.Object](combolst))
        self._comboBox1.SelectedIndex = 0
        self._comboBox1.SelectedIndexChanged += self.ComboBox1SelectedIndexChanged
        #
        # textBox3
        #
        self._textBox3.Location = System.Drawing.Point(108, 199)
        self._textBox3.Name = "textBox3"
        self._textBox3.Size = System.Drawing.Size(263, 20)
        self._textBox3.TabIndex = 1
        self._textBox3.TextChanged += self.TextBox3TextChanged
        #
        # checkBox1
        #
        self._checkBox1.Location = System.Drawing.Point(402, 199)
        self._checkBox1.Name = "checkBox1"
        self._checkBox1.Size = System.Drawing.Size(48, 21)
        self._checkBox1.TabIndex = 3
        self._checkBox1.Text = "ASC"
        self._checkBox1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        self._checkBox1.UseVisualStyleBackColor = True
        self._checkBox1.Checked = True
        self._checkBox1.CheckedChanged += self.CheckBox1CheckedChanged
        #
        # checkBox2
        #
        self._checkBox2.Location = System.Drawing.Point(456, 199)
        self._checkBox2.Name = "checkBox2"
        self._checkBox2.Size = System.Drawing.Size(48, 21)
        self._checkBox2.TabIndex = 3
        self._checkBox2.Text = "DSC"
        self._checkBox2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        self._checkBox2.UseVisualStyleBackColor = True
        self._checkBox2.CheckedChanged += self.CheckBox2CheckedChanged
        #
        # textBox4
        #
        self._textBox4.Location = System.Drawing.Point(108, 275)
        self._textBox4.Name = "textBox4"
        self._textBox4.Size = System.Drawing.Size(263, 20)
        self._textBox4.TabIndex = 1
        self._textBox4.TextChanged += self.TextBox4TextChanged
        #
        # comboBox2
        #
        self._comboBox2.FormattingEnabled = True
        self._comboBox2.Location = System.Drawing.Point(12, 275)
        self._comboBox2.Name = "comboBox2"
        self._comboBox2.Size = System.Drawing.Size(90, 21)
        self._comboBox2.TabIndex = 2
        self._comboBox2.Items.AddRange(System.Array[System.Object](combolst))
        self._comboBox2.SelectedIndex = 0
        self._comboBox2.SelectedIndexChanged += self.ComboBox2SelectedIndexChanged
        #
        # checkBox3
        #
        self._checkBox3.Location = System.Drawing.Point(402, 275)
        self._checkBox3.Name = "checkBox3"
        self._checkBox3.Size = System.Drawing.Size(48, 21)
        self._checkBox3.TabIndex = 3
        self._checkBox3.Text = "ASC"
        self._checkBox3.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        self._checkBox3.UseVisualStyleBackColor = True
        self._checkBox3.Checked = True
        self._checkBox3.CheckedChanged += self.CheckBox3CheckedChanged
        #
        # checkBox4
        #
        self._checkBox4.Location = System.Drawing.Point(456, 275)
        self._checkBox4.Name = "checkBox4"
        self._checkBox4.Size = System.Drawing.Size(48, 21)
        self._checkBox4.TabIndex = 3
        self._checkBox4.Text = "DSC"
        self._checkBox4.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        self._checkBox4.UseVisualStyleBackColor = True
        self._checkBox4.CheckedChanged += self.CheckBox4CheckedChanged
        #
        # button1
        #
        self._button1.BackColor = System.Drawing.Color.FromArgb(255, 255, 128)
        self._button1.ForeColor = System.Drawing.SystemColors.Desktop
        self._button1.Location = System.Drawing.Point(108, 316)
        self._button1.Name = "button1"
        self._button1.Size = System.Drawing.Size(97, 31)
        self._button1.TabIndex = 4
        self._button1.Text = "OK"
        self._button1.UseVisualStyleBackColor = False
        self._button1.Click += self.Button1Click
        #
        # button2
        #
        self._button2.BackColor = System.Drawing.Color.FromArgb(192, 255, 255)
        self._button2.DialogResult = System.Windows.Forms.DialogResult.Cancel
        self._button2.Location = System.Drawing.Point(260, 316)
        self._button2.Name = "button2"
        self._button2.Size = System.Drawing.Size(111, 31)
        self._button2.TabIndex = 4
        self._button2.Text = "Cancel"
        self._button2.UseVisualStyleBackColor = False
        self._button2.Click += self.Button2Click
        #
        # linkLabel1
        #
        self._linkLabel1.Location = System.Drawing.Point(12, 368)
        self._linkLabel1.Name = "linkLabel1"
        self._linkLabel1.Size = System.Drawing.Size(100, 23)
        self._linkLabel1.TabIndex = 5
        self._linkLabel1.TabStop = True
        self._linkLabel1.Text = "Help"
        self._linkLabel1.LinkClicked += self.LinkLabel1LinkClicked
        #
        # checkedListBox1
        #
        self._checkedListBox1.AccessibleDescription = "Select Title Blocks"
        self._checkedListBox1.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left
        self._checkedListBox1.CheckOnClick = True
        self._checkedListBox1.FormattingEnabled = True
        self._checkedListBox1.HorizontalScrollbar = True
        self._checkedListBox1.ImeMode = System.Windows.Forms.ImeMode.NoControl

        # Bind data to CheckedListBox1
        for i in self.titleblocks:
            self._checkedListBox1.Items.Add(i)

        self._checkedListBox1.Location = System.Drawing.Point(19, 12)
        self._checkedListBox1.Name = "checkedListBox1"
        self._checkedListBox1.RightToLeft = System.Windows.Forms.RightToLeft.No
        # self._checkedListBox1.SelectionMode = System.Windows.Forms.SelectionMode.One
        self._checkedListBox1.Size = System.Drawing.Size(352, 94)
        self._checkedListBox1.TabIndex = 6
        self._checkedListBox1.ItemCheck += self.CheckedListBox1SelectedIndexChanged
        #
        # label3
        #
        self._label3.Font = System.Drawing.Font("Microsoft Sans Serif", 12, System.Drawing.FontStyle.Regular,
                                                System.Drawing.GraphicsUnit.Point, 0)
        self._label3.ForeColor = System.Drawing.Color.DarkSlateGray
        self._label3.Location = System.Drawing.Point(402, 9)
        self._label3.Name = "label3"
        self._label3.Size = System.Drawing.Size(114, 57)
        self._label3.TabIndex = 7
        self._label3.Text = "Select Tittle Blocks*"
        self._label3.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        #
        # label4
        #
        self._label4.Location = System.Drawing.Point(12, 117)
        self._label4.Name = "label4"
        self._label4.Size = System.Drawing.Size(90, 36)
        self._label4.TabIndex = 0
        self._label4.Text = "Enter Quantity Sheets:*"
        self._label4.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        #
        # textBox5
        #
        self._textBox5.Location = System.Drawing.Point(108, 126)
        self._textBox5.Name = "textBox5"
        self._textBox5.Size = System.Drawing.Size(263, 20)
        self._textBox5.TabIndex = 1
        self._textBox5.Text = "1"
        self._textBox5.TextChanged += self.TextBox5TextChanged
        #
        # MainForm
        #
        self.AcceptButton = self._button1
        self.AutoSize = True
        self.CancelButton = self._button2
        self.ClientSize = System.Drawing.Size(536, 411)
        self.Controls.Add(self._label3)
        self.Controls.Add(self._checkedListBox1)
        self.Controls.Add(self._linkLabel1)
        self.Controls.Add(self._button2)
        self.Controls.Add(self._button1)
        self.Controls.Add(self._checkBox4)
        self.Controls.Add(self._checkBox2)
        self.Controls.Add(self._checkBox3)
        self.Controls.Add(self._checkBox1)
        self.Controls.Add(self._comboBox2)
        self.Controls.Add(self._comboBox1)
        self.Controls.Add(self._textBox2)
        self.Controls.Add(self._label2)
        self.Controls.Add(self._textBox4)
        self.Controls.Add(self._textBox3)
        self.Controls.Add(self._textBox5)
        self.Controls.Add(self._label4)
        self.Controls.Add(self._textBox1)
        self.Controls.Add(self._label1)
        self.HelpButton = True
        # self.Icon = resources.GetObject("$this.Icon")
        self.MaximumSize = System.Drawing.Size(552, 450)
        self.MinimumSize = System.Drawing.Size(552, 450)
        self.Name = "MainForm"
        self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
        self.Text = "Create Sheets"
        self.TransparencyKey = System.Drawing.Color.FromArgb(255, 128, 128)
        self.ResumeLayout(False)
        self.PerformLayout()

    def TextBox1TextChanged(self, sender, e):
        pass

    def ComboBox1SelectedIndexChanged(self, sender, e):
        pass

    def TextBox3TextChanged(self, sender, e):
        pass

    def CheckBox1CheckedChanged(self, sender, event):
        """ASC_check1"""
        if self._checkBox1.Checked:
            self._checkBox2.Checked = False
        else:
            self._checkBox2.Checked = True

    def CheckBox2CheckedChanged(self, sender, event):
        """DSC_check2"""
        if self._checkBox2.Checked:
            self._checkBox1.Checked = False
        else:
            self._checkBox1.Checked = True

    def CheckBox3CheckedChanged(self, sender, event):
        """ASC_check3"""
        if self._checkBox3.Checked:
            self._checkBox4.Checked = False
        else:
            self._checkBox4.Checked = True

    def CheckBox4CheckedChanged(self, sender, event):
        """DSC_check4"""
        if self._checkBox4.Checked:
            self._checkBox3.Checked = False
        else:
            self._checkBox3.Checked = True

    def TextBox2TextChanged(self, sender, e):
        pass

    def ComboBox2SelectedIndexChanged(self, sender, e):
        pass

    def TextBox4TextChanged(self, sender, e):
        pass

    def TextBox5TextChanged(self, sender, e):
        """Quantity Sheets"""
        pass

    def Button1Click(self, sender, e):
        """OK Button"""
        # Value from Textbox
        sheet_number = self._textBox1.Text
        sheet_name = self._textBox2.Text
        quantity_sheet = self._textBox5.Text
        index_number = self._textBox3.Text
        index_name = self._textBox4.Text

        # Value from ComboBox
        combo_number = self._comboBox1.SelectedItem
        combo_name = self._comboBox2.SelectedItem

        # CheckBox values
        asc_check1 = self._checkBox1.Checked
        dsc_check2 = self._checkBox2.Checked
        asc_check3 = self._checkBox3.Checked
        dsc_check4 = self._checkBox4.Checked

        # Value from CheckedListBox
        selected_titleblocks = self._checkedListBox1.CheckedItems

        try:
            # Check if quantity_sheet is not empty and can be converted to integer
            try:
                quantity_sheet = int(quantity_sheet)  # Try to convert to integer
            except ValueError:
                TaskDialog.Show("Warning", "Yêu cầu nhập số nguyên hợp lệ")
                return  # Stop further execution if invalid integer

            # Now check if the integer is greater than 0
            if quantity_sheet <= 0:
                TaskDialog.Show("Warning", "Yêu cầu nhập số nguyên dương lớn hơn 0")
                return  # Stop further execution if it's not a positive integer

            # Ensure all required fields are filled
            if not sheet_number or not sheet_name or not index_number or selected_titleblocks.Count == 0:
                TaskDialog.Show("Warning", "Vui lòng điền vào các giá trị có *")
                return

            # Ensure Index include number and alpha
            for i in index_number:
                if i.isspace():
                    continue
                if not i.isdigit() and not i.isalpha():
                    TaskDialog.Show("Warning", "Giá trị index number chỉ có chữ hoặc số")
                    return  # Stop further execution

            for i in index_name:
                if i.isspace():
                    continue

                if not i.isdigit() and not i.isalpha():
                    TaskDialog.Show("Warning", "Giá trị index name chỉ có chữ hoặc số")
                    return  # Stop further execution

            else:
                # Proceed with the data (You can handle Revit sheet creation here)
                self.DialogResult = System.Windows.Forms.DialogResult.OK
                self.Close()

        except Exception as ex:
            TaskDialog.Show("Error", "An error occurred: {}".format(ex))

    def Button2Click(self, sender, e):
        """Cancel Button"""
        self.Close()

    def LinkLabel1LinkClicked(self, sender, event):
        System.Diagnostics.Process.Start("https://www.youtube.com/@paper.engineer")

    def CheckedListBox1SelectedIndexChanged(self, sender, e):
        """Select Title Block"""
        if e.NewValue == CheckState.Checked:
            # Uncheck all other items
            for i in range(self._checkedListBox1.Items.Count):
                if i != e.Index:
                    self._checkedListBox1.SetItemChecked(i, False)
