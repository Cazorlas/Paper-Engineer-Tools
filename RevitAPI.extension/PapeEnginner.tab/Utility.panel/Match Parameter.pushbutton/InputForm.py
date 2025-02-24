#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = 'Settings'
__author__ = "Paper Engineer"
__doc__ = """Version = 1.0
Date    = 14.02.2025
__________________________________________________________________
Description
Configure the categories to check. You need to run setting before running the script.
__________________________________________________________________
How to Use
-> Choose at least one category tag to check
-> Save the Setting
-> If there is no category tag to choose, the setting will be reset
-> You can Import or Export the Setting configuration
__________________________________________________________________
Copyright & License
© 2024 Paper Engineer.
All rights reserved. Please give proper credit if you share or use this script in your project.
"""

import clr
import System
from System import Enum
import json
from rpw.ui.forms import Alert

# Importing necessary references for Revit and Windows Forms
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitNodes")
import Revit
from pyrevit import forms, revit, script

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
from System.Windows.Forms import Application

Application.EnableVisualStyles()
# Application.SetCompatibleTextRenderingDefault(False)

import os
from System.Drawing import Icon  # Import Icon class
import System.Diagnostics  # Open Link when press Button

from System.Drawing import *
from System.Windows.Forms import *

# Adding a reference to the system to use List
clr.AddReference('System')
from System.Collections.Generic import List

"""---------------------------Get active document and view from Revit------------------------"""
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
# doc = revit.doc
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
uiviews = uidoc.GetOpenUIViews()
jsonFile = os.path.join(os.getenv("APPDATA"), "MatchParameter.json")
uiview = [x for x in uiviews if x.ViewId == view.Id][0]
"""-------------------------------------------------------------------------------------------"""



class InputForm(Form):
    def __init__(self, data, group, valueGroup):
        self.data = data
        self.groupKeys = group
        self.valueGroup = valueGroup

        self.allChecked = False  # Trạng thái chọn tất cả
        self.HiddenState = False  # Trạng thái ẩn
        self.HiddenItems = []  # Danh sách chứa các mục bị ẩn
        self.ListViewItems = []  # Danh sách chứa các mục ban đầu
        self.selectedParams = set()  # Lưu tên các parameter được check


        self.InitializeComponent()
        self.LoadConfig()




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
        self._btnSave = System.Windows.Forms.Button()
        self._btnImport = System.Windows.Forms.Button()
        self._btnExport = System.Windows.Forms.Button()
        self._btnImport = System.Windows.Forms.Button()
        self._btnExport = System.Windows.Forms.Button()
        self._tableLayoutPanel31 = System.Windows.Forms.TableLayoutPanel()
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
        self._panel2.Padding = System.Windows.Forms.Padding(8, 0, 8, 0)
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
        self._comboBox1.Items.Add("All")
        self._comboBox1.Items.AddRange(System.Array[System.Object](self.groupKeys))
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
        self._listView1.Columns.Add("Parameters", 600, System.Windows.Forms.HorizontalAlignment.Left)
        # Đăng ký sự kiện Resize để cột luôn chiếm toàn bộ chiều rộng của ListView
        self._listView1.Resize += self.ListViewResize

        for idx, item in enumerate(self.data):
            listItem = System.Windows.Forms.ListViewItem(str(item.Definition.Name))
            self._listView1.Items.Add(listItem)
            self.ListViewItems.append((idx, listItem))

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
        self._btnHide.Text = "Hide/Unhide Unselected"
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
        # btnImport
        #
        self._btnImport.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right
        self._btnImport.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
        self._btnImport.Location = System.Drawing.Point(8, 49)
        self._btnImport.Name = "btnImport"
        self._btnImport.Size = System.Drawing.Size(142, 33)
        self._btnImport.TabIndex = 1
        self._btnImport.Text = "Import Data"
        self._btnImport.UseVisualStyleBackColor = True
        self._btnImport.Click += self.BtnImportClick
        #
        # btnExport
        #
        self._btnExport.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right
        self._btnExport.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
        self._btnExport.Location = System.Drawing.Point(308, 49)
        self._btnExport.Name = "btnExport"
        self._btnExport.Size = System.Drawing.Size(143, 33)
        self._btnExport.TabIndex = 2
        self._btnExport.Text = "Export Data"
        self._btnExport.UseVisualStyleBackColor = True
        self._btnExport.Click += self.BtnExportClick
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
        self._tableLayoutPanel31.Controls.Add(self._btnHide, 2, 0)

        self._tableLayoutPanel31.Controls.Add(self._btnSave, 0, 1)
        # self._tableLayoutPanel31.SetColumnSpan(self._btnSave, 3)
        self._tableLayoutPanel31.Controls.Add(self._btnImport, 0, 1)
        self._tableLayoutPanel31.Controls.Add(self._btnSave, 1, 1)
        self._tableLayoutPanel31.Controls.Add(self._btnExport, 2, 1)

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
        self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
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



    def getParamKey(self, param):
        try:
            return str(param.Id.IntegerValue)
        except Exception:
            return str(id(param))




    def ComboBox1SelectedIndexChanged(self, sender, e):
        # Cập nhật trạng thái đã chọn của các item hiện tại
        for idx, listItem in self.ListViewItems:
            key = self.getParamKey(listItem.Tag)
            if listItem.Checked:
                self.selectedParams.add(key)
            else:
                self.selectedParams.discard(key)
        # Lấy group được chọn
        selectedGroup = self._comboBox1.SelectedItem
        self.LoadParameters(selectedGroup)



    def LoadParameters(self, group):
        self._listView1.BeginUpdate()
        self._listView1.Items.Clear()
        self.ListViewItems = []  # Reset danh sách các item

        if group == "All":
            params = self.data
        else:
            # valueGroup là dictionary chứa danh sách parameter theo group
            params = self.valueGroup.get(group, [])

        for idx, param in enumerate(params):
            key = self.getParamKey(param)
            listItem = System.Windows.Forms.ListViewItem(str(param.Definition.Name))
            listItem.Tag = param
            if key in self.selectedParams:
                listItem.Checked = True
            self._listView1.Items.Add(listItem)
            self.ListViewItems.append((idx, listItem))
        self._listView1.EndUpdate()



    def TextBoxFindTextChanged(self, sender, e):
            # Lấy chuỗi tìm kiếm từ ô textbox, chuyển về chữ thường để so sánh không phân biệt chữ hoa/chữ thường
            searchStr = self._textBoxFind.Text.lower().strip()

            # Tạm dừng cập nhật giao diện để tránh nháy màn hình khi thay đổi danh sách mục
            self._listView1.BeginUpdate()
            # Xoá hết các mục đang hiển thị
            self._listView1.Items.Clear()

            if searchStr == "":
                # Nếu không có chuỗi tìm kiếm (ô trống), khôi phục lại toàn bộ ListView theo thứ tự ban đầu
                for idx, item in sorted(self.ListViewItems, key=lambda x: x[0]):
                    self._listView1.Items.Add(item)
            else:
                # Nếu có chuỗi tìm kiếm, lọc các mục có chứa chuỗi đó trong thuộc tính Text của ListViewItem
                for idx, item in sorted(self.ListViewItems, key=lambda x: x[0]):
                    # Kiểm tra nếu chuỗi tìm kiếm xuất hiện trong text của item (chuyển về chữ thường để so sánh)
                    # if searchStr in item.Text.lower():
                    if item.Text.lower().startswith(searchStr):
                        self._listView1.Items.Add(item)

            # Cho phép ListView cập nhật giao diện sau khi thay đổi
            self._listView1.EndUpdate()



    def ListView1SelectedIndexChanged(self, sender, e):
        pass

    def BtnCheckUncheckClick(self, sender, e):
        """Check or uncheck all items in the ListView."""
        self.allChecked = not self.allChecked
        for item in self._listView1.Items:
            item.Checked = self.allChecked

    def BtnToggleClick(self, sender, e):
        """Toggle checked state of each individual item."""
        for item in self._listView1.Items:
            item.Checked = not item.Checked

    def BtnHideClick(self, sender, e):
        self.HiddenState = not self.HiddenState
        self._listView1.BeginUpdate()
        # Xoá toàn bộ mục hiện tại
        self._listView1.Items.Clear()
        if self.HiddenState:
            # Khi ẩn: chỉ thêm lại các mục đã được check
            for idx, item in sorted(self.ListViewItems, key=lambda x: x[0]):
                if item.Checked:
                    self._listView1.Items.Add(item)
        else:
            # Khi hiện: thêm lại tất cả các mục theo thứ tự ban đầu
            for idx, item in sorted(self.ListViewItems, key=lambda x: x[0]):
                self._listView1.Items.Add(item)
        self._listView1.EndUpdate()

    def BtnExportClick(self, sender, e):
        itemChecked = [item.Text for item in self._listView1.Items if item.Checked]
        selectedComboBoxItem = self._comboBox1.SelectedItem if self._comboBox1.SelectedItem else ""

        configData = {
            "listViewItem": itemChecked,
            "selectedComboBox": selectedComboBoxItem
        }

        if len(itemChecked) > 0:
            fileSave = forms.save_file(file_ext='json', default_name="Data", restore_dir=True, title="Export Data")

            if fileSave:
                try:
                    with open(fileSave, "w") as f:
                        json.dump(configData, f, ensure_ascii=False, indent=4)
                    Alert(title="Success", content="Data exported successfully!")
                except Exception as e:
                    Alert(title="Error", content="Failed to export data!\n{}".format(str(e)))
            else:
                return
        else:
            Alert(title="Notification", content="There is no selected category")

    def BtnImportClick(self, sender, e):
        """Chọn file JSON và cập nhật dữ liệu từ file đó vào form."""
        json_file = forms.pick_file(files_filter='Json File (*.json)|*.json', multi_file=False)

        if json_file:  # Nếu người dùng chọn một tệp
            try:
                with open(json_file, "r") as f:
                    config = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                Alert(title="Error", content="Invalid JSON file!")
                return

            # Trích xuất dữ liệu từ JSON
            checkedItems = config.get('listViewItem', [])
            selectedComboBoxItem = config.get('selectedComboBox', "")

            # Reset trạng thái form (xoá danh sách cũ và cập nhật mới)
            self._listView1.BeginUpdate()
            self._listView1.Items.Clear()
            self.ListViewItems = []  # Reset danh sách gốc

            for idx, item in enumerate(self.data):  # Load lại danh sách
                listItem = System.Windows.Forms.ListViewItem(str(item))
                listItem.Checked = item in checkedItems  # Check nếu item nằm trong JSON
                self._listView1.Items.Add(listItem)
                self.ListViewItems.append((idx, listItem))

            self._listView1.EndUpdate()

            # Cập nhật ComboBox nếu có giá trị hợp lệ
            if selectedComboBoxItem and selectedComboBoxItem in self._comboBox1.Items:
                self._comboBox1.SelectedItem = selectedComboBoxItem

            # Hiển thị thông báo hoàn tất
            Alert(title="Notification", content="Data imported successfully!")

    def ListViewResize(self, sender, e):
        sender.Columns[0].Width = sender.ClientSize.Width

    def ShowTaskDialog(self, title, mainContent, allowCancellation=True):
        """Hiển thị TaskDialog với các tham số tùy chỉnh."""
        dialog = TaskDialog(title)
        dialog.MainContent = mainContent
        dialog.TitleAutoPrefix = False
        dialog.MainIcon = TaskDialogIcon.TaskDialogIconInformation
        dialog.CommonButtons = TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel
        dialog.AllowCancellation = allowCancellation
        dialog.FooterText = '<a href="{0}">{1}</a>'.format(
            "https://www.youtube.com/@paper.engineer", "Help")

        return dialog.Show()

    def BtnSaveClick(self, sender, e):
        """Lưu tất cả các giá trị được chọn, kể cả những mục bị ẩn do bộ lọc tìm kiếm."""
        allCheckedItems = set()  # Tạo tập hợp để lưu tất cả các mục đã check

        # ✅ Duyệt qua danh sách gốc `ListViewItems` để lấy tất cả các mục
        for idx, item in self.ListViewItems:
            if item.Checked:
                allCheckedItems.add(item.Text)  # Lưu lại các mục đã được check

        selectedComboBoxItem = self._comboBox1.SelectedItem if self._comboBox1.SelectedItem else ""

        configData = {
            "listViewItem": list(allCheckedItems),  # Lưu tất cả các mục đã check
            "selectedComboBox": selectedComboBoxItem
        }

        if len(allCheckedItems) == 0:
            warning = self.ShowTaskDialog(
                "Warning",
                "The script will be reset and cannot run until you select at least one category tag."
            )
            if warning == TaskDialogResult.Cancel:
                return
            elif warning == TaskDialogResult.Ok:
                self.SaveConfigSetting(configData)
                self.Close()
        else:
            self.SaveConfigSetting(configData)
            Alert(title="Notification", content="Data was saved")
            self.Close()

    def SaveConfigSetting(self, data):
        """Lưu config vào file JSON."""
        with open(jsonFile, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def LoadConfig(self):
        """Nạp danh sách các mục đã check từ JSON."""
        if not os.path.exists(jsonFile):
            with open(jsonFile, "w") as f:
                json.dump({"listViewItem": []}, f, ensure_ascii=False, indent=4)
        elif os.path.exists(jsonFile):
            with open(jsonFile, "r") as f:
                try:
                    config = json.load(f)
                except json.JSONDecodeError:
                    config = {}

            checkedItems = config.get('listViewItem', [])
            selectedComboBoxItem = config.get('selectedComboBox', "")

            # Kiểm tra và check lại các mục trong ListView nếu chúng nằm trong danh sách đã lưu
            for item in self._listView1.Items:
                if item.Text in checkedItems:
                    item.Checked = True

            # Cập nhật giá trị ComboBox nếu có trong danh sách
            if selectedComboBoxItem and selectedComboBoxItem in self._comboBox1.Items:
                self._comboBox1.SelectedItem = selectedComboBoxItem

