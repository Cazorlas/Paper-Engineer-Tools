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
    def __init__(self, categoryName):
        self.categoryName = categoryName
        self.checkedItems = {}  # Lưu trạng thái checkbox
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
        self._btnSelectNone = System.Windows.Forms.Button()
        self._labelNotice = System.Windows.Forms.Label()
        self.SuspendLayout()

        # listView
        self._listView.CheckBoxes = True
        self._listView.Columns.AddRange(System.Array[System.Windows.Forms.ColumnHeader]([self._categoryHeader]))
        self._listView.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                  System.Drawing.GraphicsUnit.Point, 0)
        # self._listView.HoverSelection = True
        self._listView.Location = System.Drawing.Point(4, 12)
        self._listView.Name = "listView"
        self._listView.Size = System.Drawing.Size(252, 203)
        self._listView.TabIndex = 0
        self._listView.UseCompatibleStateImageBehavior = False
        self._listView.View = System.Windows.Forms.View.Details
        self._listView.Resize += self.ListViewResize

        for name in self.categoryName:
            item = System.Windows.Forms.ListViewItem(name)
            self._listView.Items.Add(item)
            # self.originalItems.append(item)

        self._listView.Anchor = (AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Bottom | AnchorStyles.Right)

        # categoryHeader
        self._categoryHeader.Text = "Category"
        self._categoryHeader.Width = 250

        # textBox1
        self._textBox1.Location = System.Drawing.Point(276, 58)
        self._textBox1.Name = "textBox1"
        self._textBox1.Size = System.Drawing.Size(149, 20)
        self._textBox1.TabIndex = 1
        self._textBox1.TextChanged += self.TextBox1TextChanged
        self._textBox1.Anchor = (AnchorStyles.Top | AnchorStyles.Right)

        # labelFind
        self._labelFind.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._labelFind.Location = System.Drawing.Point(431, 52)
        self._labelFind.Name = "labelFind"
        self._labelFind.Size = System.Drawing.Size(45, 29)
        self._labelFind.TabIndex = 2
        self._labelFind.Text = "Find"
        self._labelFind.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        self._labelFind.Anchor = (AnchorStyles.Top | AnchorStyles.Right)

        # btnOk
        self._btnOk.BackColor = System.Drawing.SystemColors.ActiveCaption
        self._btnOk.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                               System.Drawing.GraphicsUnit.Point, 0)
        self._btnOk.Location = System.Drawing.Point(276, 144)
        self._btnOk.Name = "btnOk"
        self._btnOk.Size = System.Drawing.Size(137, 28)
        self._btnOk.TabIndex = 3
        self._btnOk.Text = "Select"
        self._btnOk.UseVisualStyleBackColor = False
        self._btnOk.Click += self.BtnOkClick
        self._btnOk.Anchor = (AnchorStyles.Bottom | AnchorStyles.Right)

        # btnCancel
        self._btnCancel.BackColor = System.Drawing.SystemColors.ActiveCaption
        self._btnCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
        self._btnCancel.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._btnCancel.Location = System.Drawing.Point(276, 187)
        self._btnCancel.Name = "btnCancel"
        self._btnCancel.Size = System.Drawing.Size(137, 28)
        self._btnCancel.TabIndex = 3
        self._btnCancel.Text = "Cancel"
        self._btnCancel.UseVisualStyleBackColor = False
        self._btnCancel.Click += self.BtnCancelClick
        self._btnCancel.Anchor = (AnchorStyles.Bottom | AnchorStyles.Right)

        # labelNotice
        self._labelNotice.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Italic,
                                                     System.Drawing.GraphicsUnit.Point, 0)
        self._labelNotice.Location = System.Drawing.Point(276, 12)
        self._labelNotice.Name = "labelNotice"
        self._labelNotice.Size = System.Drawing.Size(184, 23)
        self._labelNotice.TabIndex = 4
        self._labelNotice.Text = "@PaperEngineer"
        self._labelNotice.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        self._labelNotice.Anchor = (AnchorStyles.Top | AnchorStyles.Right)

        # btnSelectNone
        self._btnSelectNone.BackColor = System.Drawing.SystemColors.ActiveCaption
        self._btnSelectNone.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                       System.Drawing.GraphicsUnit.Point, 0)
        self._btnSelectNone.Location = System.Drawing.Point(276, 97)
        self._btnSelectNone.Name = "btnSelectNone"
        self._btnSelectNone.Size = System.Drawing.Size(137, 28)
        self._btnSelectNone.TabIndex = 3
        self._btnSelectNone.Text = "Select None"
        self._btnSelectNone.UseVisualStyleBackColor = False
        # Đảm bảo nút di chuyển đúng theo cửa sổ
        self._btnSelectNone.Anchor = (AnchorStyles.Bottom | AnchorStyles.Right)
        self._btnSelectNone.Click += self.BtnSelectNone

        # MainForm
        self.ClientSize = System.Drawing.Size(472, 227)
        self.Controls.Add(self._labelNotice)
        self.Controls.Add(self._btnCancel)
        self.Controls.Add(self._btnOk)
        self.Controls.Add(self._btnSelectNone)
        self.Controls.Add(self._labelFind)
        self.Controls.Add(self._textBox1)
        self.Controls.Add(self._listView)
        self.MinimumSize = System.Drawing.Size(472, 270)
        self.Text = "Select by Categories (current view)"
        self.ResumeLayout(False)
        self.PerformLayout()

    def Label1Click(self, sender, e):
        pass

    def ListViewResize(self, sender, e):
        """
        Đảm bảo rằng cột 'Category' sẽ chiếm toàn bộ chiều rộng của ListView
        """
        # Lấy kích thước chiều rộng của ListView
        totalWidth = self._listView.ClientSize.Width

        # Kiểm tra nếu có ít nhất một cột
        if self._listView.Columns.Count > 0:
            # Đặt chiều rộng của cột 'Category' bằng với chiều rộng của ListView
            self._listView.Columns[0].Width = totalWidth

    def TextBox1TextChanged(self, sender, e):
        """
        Lọc danh sách trong ListView dựa trên ký tự nhập vào ô Find.
        Nếu không có ký tự nào, khôi phục danh sách ban đầu và giữ trạng thái tick.
        """
        searchText = self._textBox1.Text.strip().lower()

        # Lưu trạng thái Checked hiện tại
        for item in self._listView.Items:
            self.checkedItems[item.Text] = item.Checked

        # Xóa tất cả các mục hiện tại trong ListView
        self._listView.Items.Clear()

        if not searchText:  # Nếu TextBox trống, khôi phục toàn bộ danh sách
            for name in self.categoryName:
                item = System.Windows.Forms.ListViewItem(name)
                # Khôi phục trạng thái Checked từ dictionary
                if name in self.checkedItems:
                    item.Checked = self.checkedItems[name]
                self._listView.Items.Add(item)
        else:  # Chỉ hiển thị các mục khớp với từ khóa
            for name in self.categoryName:
                if searchText in name.lower():
                    item = System.Windows.Forms.ListViewItem(name)
                    # Khôi phục trạng thái Checked từ dictionary
                    if name in self.checkedItems:
                        item.Checked = self.checkedItems[name]
                    self._listView.Items.Add(item)

    def ListViewSelectedIndexChanged(self, sender, e):
        pass

    def BtnOkClick(self, sender, e):
        # Save and close form

        selectedCategories = [item for item in self._listView.Items if item.Checked]

        if len(selectedCategories) == 0:
            ShowNotification("Error", "No choose any categories")
            return
        else:
            self.DialogResult = System.Windows.Forms.DialogResult.OK
            self.Close()

    def BtnSelectNone(self, sender, e):
        """
        Bỏ chọn tất cả các mục trong ListView.
        """
        for item in self._listView.Items:
            item.Checked = False

        # Cập nhật lại dictionary trạng thái checkbox
        for name in self.categoryName:
            self.checkedItems[name] = False

    def BtnCancelClick(self, sender, e):
        self.Close()
