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
"""-------------------------------------------------------------------------------------------"""
comboLst = ["None"]


class MainForm(Form):
    def __init__(self, linkName, status, savedPath, linkWorkset, worksetName):
        self.linkName = linkName
        self.status = status
        self.savedPath = savedPath
        self.linkWorkset = linkWorkset
        self.worksetName = list(worksetName)

        self.originalItems = []  # Lưu danh sách gốc
        self.browseFolder = None
        self.addRVTFile = None

        self.InitializeComponent()

    def InitializeComponent(self):
        # Get the directory of the running script
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "icon.ico")
        # Load custom icon (if available)
        if os.path.exists(icon_path):
            self.Icon = Icon(icon_path)

        self._listView = System.Windows.Forms.ListView()
        self._linkName = System.Windows.Forms.ColumnHeader()
        self._linkStatus = System.Windows.Forms.ColumnHeader()
        self._checkBoxSelectAll = System.Windows.Forms.CheckBox()
        self._labelFind = System.Windows.Forms.Label()
        self._textBoxFind = System.Windows.Forms.TextBox()
        self._labelBrowse = System.Windows.Forms.Label()
        self._groupBoxData = System.Windows.Forms.GroupBox()
        self._btnBrowse = System.Windows.Forms.Button()
        self._labelWorkset = System.Windows.Forms.Label()
        self._comboBoxWorkset = System.Windows.Forms.ComboBox()
        self._groupBoxPosition = System.Windows.Forms.GroupBox()
        self._radioButtonOrigin = System.Windows.Forms.RadioButton()
        self._radioButtonShared = System.Windows.Forms.RadioButton()
        self._btnReloadFrom = System.Windows.Forms.Button()
        self._btnAddLinks = System.Windows.Forms.Button()
        self._btnUnload = System.Windows.Forms.Button()
        self._btnReload = System.Windows.Forms.Button()
        self._btnSetWorkset = System.Windows.Forms.Button()
        self._btnRemove = System.Windows.Forms.Button()
        self._buttonClose = System.Windows.Forms.Button()
        self._btnOK = System.Windows.Forms.Button()
        self._linkHelp = System.Windows.Forms.LinkLabel()
        self._labelAuthor = System.Windows.Forms.Label()
        self._headerLinkName = System.Windows.Forms.ColumnHeader()
        self._headerStatus = System.Windows.Forms.ColumnHeader()
        self._headerSavePath = System.Windows.Forms.ColumnHeader()
        self._headerWorkset = System.Windows.Forms.ColumnHeader()
        self._headerNewPath = System.Windows.Forms.ColumnHeader()
        self._groupBoxData.SuspendLayout()
        self._groupBoxPosition.SuspendLayout()
        self.SuspendLayout()
        #
        # listView
        #
        self._listView.CheckBoxes = True
        self._listView.MultiSelect = True
        self._listView.FullRowSelect = True
        self._listView.Columns.AddRange(System.Array[System.Windows.Forms.ColumnHeader](
            [self._headerLinkName,
             self._headerStatus,
             self._headerSavePath,
             self._headerNewPath,
             self._headerWorkset]))
        self._listView.GridLines = True
        self._listView.LabelWrap = False
        self._listView.Location = System.Drawing.Point(12, 50)
        self._listView.Name = "listView"
        self._listView.ShowItemToolTips = True
        self._listView.Size = System.Drawing.Size(430, 341)
        self._listView.TabIndex = 0
        self._listView.UseCompatibleStateImageBehavior = False
        self._listView.View = System.Windows.Forms.View.Details
        self._listView.Resize += self.ListViewResize
        self._listView.SelectedIndexChanged += self.ListViewSelectedIndexChanged

        # Gắn dữ liệu vào ListView
        for i in range(len(self.linkName)):
            item = System.Windows.Forms.ListViewItem(self.linkName[i])  # Cột đầu tiên (Link Name)
            item.SubItems.Add(self.status[i])  # Cột thứ hai (Status)
            item.SubItems.Add(self.savedPath[i])  # Cột thứ ba (Saved Path)
            item.SubItems.Add(self.linkWorkset[i])  # Cột thứ tư (Workset)
            self._listView.Items.Add(item)
            self.originalItems.append(item) # Lưu item gốc

        #
        # checkBoxSelectAll
        #
        self._checkBoxSelectAll.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                           System.Drawing.GraphicsUnit.Point, 0)
        self._checkBoxSelectAll.Location = System.Drawing.Point(12, 14)
        self._checkBoxSelectAll.Name = "checkBoxSelectAll"
        self._checkBoxSelectAll.Size = System.Drawing.Size(104, 24)
        self._checkBoxSelectAll.TabIndex = 1
        self._checkBoxSelectAll.Text = "Select All"
        self._checkBoxSelectAll.UseVisualStyleBackColor = True
        self._checkBoxSelectAll.CheckedChanged += self.CheckBoxSelectAllCheckedChanged
        #
        # labelFind
        #
        self._labelFind.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._labelFind.Location = System.Drawing.Point(122, 13)
        self._labelFind.Name = "labelFind"
        self._labelFind.Size = System.Drawing.Size(100, 23)
        self._labelFind.TabIndex = 2
        self._labelFind.Text = "Find"
        self._labelFind.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        #
        # textBoxFind
        #
        self._textBoxFind.Location = System.Drawing.Point(162, 16)
        self._textBoxFind.Name = "textBoxFind"
        self._textBoxFind.Size = System.Drawing.Size(279, 20)
        self._textBoxFind.TabIndex = 3
        self._textBoxFind.TextChanged += self.TextBoxFindTextChanged
        #
        # labelBrowse
        #
        self._labelBrowse.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                     System.Drawing.GraphicsUnit.Point, 0)
        self._labelBrowse.Location = System.Drawing.Point(6, 26)
        self._labelBrowse.Name = "labelBrowse"
        self._labelBrowse.Size = System.Drawing.Size(74, 23)
        self._labelBrowse.TabIndex = 4
        self._labelBrowse.Text = "Browse:"
        #
        # groupBoxData
        #
        self._groupBoxData.Controls.Add(self._comboBoxWorkset)
        self._groupBoxData.Controls.Add(self._btnBrowse)
        self._groupBoxData.Controls.Add(self._labelWorkset)
        self._groupBoxData.Controls.Add(self._labelBrowse)
        self._groupBoxData.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                      System.Drawing.GraphicsUnit.Point, 0)
        self._groupBoxData.Location = System.Drawing.Point(448, 50)
        self._groupBoxData.Name = "groupBoxData"
        self._groupBoxData.Size = System.Drawing.Size(194, 126)
        self._groupBoxData.TabIndex = 5
        self._groupBoxData.TabStop = False
        self._groupBoxData.Text = "Data"
        #
        # btnBrowse
        #
        self._btnBrowse.Location = System.Drawing.Point(86, 20)
        self._btnBrowse.Name = "btnBrowse"
        self._btnBrowse.Size = System.Drawing.Size(77, 27)
        self._btnBrowse.TabIndex = 5
        self._btnBrowse.Text = "...."
        self._btnBrowse.UseVisualStyleBackColor = True
        self._btnBrowse.Click += self.BtnBrowseClick
        #
        # labelWorkset
        #
        self._labelWorkset.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                      System.Drawing.GraphicsUnit.Point, 0)
        self._labelWorkset.Location = System.Drawing.Point(6, 61)
        self._labelWorkset.Name = "labelWorkset"
        self._labelWorkset.Size = System.Drawing.Size(74, 23)
        self._labelWorkset.TabIndex = 4
        self._labelWorkset.Text = "Workset:"
        #
        # comboBoxWorkset
        #
        self._comboBoxWorkset.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
        self._comboBoxWorkset.FormattingEnabled = True
        self._comboBoxWorkset.Items.AddRange(System.Array[System.Object](self.worksetName))

        self._comboBoxWorkset.Location = System.Drawing.Point(6, 87)
        self._comboBoxWorkset.Name = "comboBoxWorkset"
        self._comboBoxWorkset.Size = System.Drawing.Size(182, 23)
        self._comboBoxWorkset.TabIndex = 6
        self._comboBoxWorkset.SelectedIndexChanged += self.ComboBoxWorksetSelectedIndexChanged
        #
        # groupBoxPosition
        #
        self._groupBoxPosition.Controls.Add(self._radioButtonShared)
        self._groupBoxPosition.Controls.Add(self._radioButtonOrigin)
        self._groupBoxPosition.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                          System.Drawing.GraphicsUnit.Point, 0)
        self._groupBoxPosition.Location = System.Drawing.Point(448, 182)
        self._groupBoxPosition.Name = "groupBoxPosition"
        self._groupBoxPosition.Size = System.Drawing.Size(194, 57)
        self._groupBoxPosition.TabIndex = 5
        self._groupBoxPosition.TabStop = False
        self._groupBoxPosition.Text = "Position"
        #
        # radioButtonOrigin
        #
        self._radioButtonOrigin.Checked = True
        self._radioButtonOrigin.Location = System.Drawing.Point(18, 20)
        self._radioButtonOrigin.Name = "radioButtonOrigin"
        self._radioButtonOrigin.Size = System.Drawing.Size(88, 24)
        self._radioButtonOrigin.TabIndex = 0
        self._radioButtonOrigin.TabStop = True
        self._radioButtonOrigin.Text = "Origin"
        self._radioButtonOrigin.UseVisualStyleBackColor = True
        self._radioButtonOrigin.CheckedChanged += self.RadioButtonOriginCheckedChanged
        #
        # radioButtonShared
        #
        self._radioButtonShared.Location = System.Drawing.Point(97, 20)
        self._radioButtonShared.Name = "radioButtonShared"
        self._radioButtonShared.Size = System.Drawing.Size(91, 24)
        self._radioButtonShared.TabIndex = 1
        self._radioButtonShared.Text = "Shared"
        self._radioButtonShared.UseVisualStyleBackColor = True
        self._radioButtonShared.CheckedChanged += self.RadioButtonSharedCheckedChanged
        #
        # btnReloadFrom
        #
        self._btnReloadFrom.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                       System.Drawing.GraphicsUnit.Point, 0)
        self._btnReloadFrom.Location = System.Drawing.Point(548, 245)
        self._btnReloadFrom.Name = "btnReloadFrom"
        self._btnReloadFrom.Size = System.Drawing.Size(94, 32)
        self._btnReloadFrom.TabIndex = 6
        self._btnReloadFrom.Text = "Reload From"
        self._btnReloadFrom.UseVisualStyleBackColor = True
        self._btnReloadFrom.Click += self.BtnReloadFromClick
        #
        # btnAddLinks
        #
        self._btnAddLinks.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                     System.Drawing.GraphicsUnit.Point, 0)
        self._btnAddLinks.Location = System.Drawing.Point(448, 245)
        self._btnAddLinks.Name = "btnAddLinks"
        self._btnAddLinks.Size = System.Drawing.Size(94, 32)
        self._btnAddLinks.TabIndex = 6
        self._btnAddLinks.Text = "Add Links"
        self._btnAddLinks.UseVisualStyleBackColor = True
        self._btnAddLinks.Click += self.BtnAddLinksClick
        #
        # btnUnload
        #
        self._btnUnload.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._btnUnload.Location = System.Drawing.Point(548, 283)
        self._btnUnload.Name = "btnUnload"
        self._btnUnload.Size = System.Drawing.Size(94, 32)
        self._btnUnload.TabIndex = 6
        self._btnUnload.Text = "Unload"
        self._btnUnload.UseVisualStyleBackColor = True
        self._btnUnload.Click += self.BtnUnloadClick
        #
        # btnReload
        #
        self._btnReload.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._btnReload.Location = System.Drawing.Point(448, 283)
        self._btnReload.Name = "btnReload"
        self._btnReload.Size = System.Drawing.Size(94, 32)
        self._btnReload.TabIndex = 6
        self._btnReload.Text = "Reload"
        self._btnReload.UseVisualStyleBackColor = True
        self._btnReload.Click += self.BtnReloadClick
        #
        # btnSetWorkset
        #
        self._btnSetWorkset.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                       System.Drawing.GraphicsUnit.Point, 0)
        self._btnSetWorkset.Location = System.Drawing.Point(548, 321)
        self._btnSetWorkset.Name = "btnSetWorkset"
        self._btnSetWorkset.Size = System.Drawing.Size(94, 32)
        self._btnSetWorkset.TabIndex = 6
        self._btnSetWorkset.Text = "Set Workset"
        self._btnSetWorkset.UseVisualStyleBackColor = True
        self._btnSetWorkset.Click += self.BtnSetWorksetClick
        #
        # btnRemove
        #
        self._btnRemove.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                   System.Drawing.GraphicsUnit.Point, 0)
        self._btnRemove.Location = System.Drawing.Point(448, 321)
        self._btnRemove.Name = "btnRemove"
        self._btnRemove.Size = System.Drawing.Size(94, 32)
        self._btnRemove.TabIndex = 6
        self._btnRemove.Text = "Remove"
        self._btnRemove.UseVisualStyleBackColor = True
        self._btnRemove.Click += self.BtnRemoveClick
        #
        # buttonClose
        #
        self._buttonClose.DialogResult = System.Windows.Forms.DialogResult.Cancel
        self._buttonClose.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                                     System.Drawing.GraphicsUnit.Point, 0)
        self._buttonClose.Location = System.Drawing.Point(548, 359)
        self._buttonClose.Name = "buttonClose"
        self._buttonClose.Size = System.Drawing.Size(94, 32)
        self._buttonClose.TabIndex = 6
        self._buttonClose.Text = "Close"
        self._buttonClose.UseVisualStyleBackColor = True
        self._buttonClose.Click += self.ButtonCloseClick
        #
        # btnOK
        #
        self._btnOK.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular,
                                               System.Drawing.GraphicsUnit.Point, 0)
        self._btnOK.Location = System.Drawing.Point(448, 359)
        self._btnOK.Name = "btnOK"
        self._btnOK.Size = System.Drawing.Size(94, 32)
        self._btnOK.TabIndex = 6
        self._btnOK.Text = "OK"
        self._btnOK.UseVisualStyleBackColor = True
        self._btnOK.Click += self.BtnOKClick
        #
        # linkHelp
        #
        self._linkHelp.Font = System.Drawing.Font("Microsoft Sans Serif", 8.25, System.Drawing.FontStyle.Italic,
                                                  System.Drawing.GraphicsUnit.Point, 0)
        self._linkHelp.Location = System.Drawing.Point(454, 14)
        self._linkHelp.Name = "linkHelp"
        self._linkHelp.Size = System.Drawing.Size(100, 23)
        self._linkHelp.TabIndex = 7
        self._linkHelp.TabStop = True
        self._linkHelp.Text = "Help"
        self._linkHelp.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        self._linkHelp.LinkClicked += self.LinkHelpLinkClicked
        #
        # labelAuthor
        #
        self._labelAuthor.Font = System.Drawing.Font("Microsoft Sans Serif", 8.25, System.Drawing.FontStyle.Italic,
                                                     System.Drawing.GraphicsUnit.Point, 0)
        self._labelAuthor.Location = System.Drawing.Point(497, 16)
        self._labelAuthor.Name = "labelAuthor"
        self._labelAuthor.Size = System.Drawing.Size(100, 23)
        self._labelAuthor.TabIndex = 8
        self._labelAuthor.Text = "@PaperEngineer"
        self._labelAuthor.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        #
        # headerLinkName
        #
        self._headerLinkName.Text = "Link Name"
        self._headerLinkName.Width = 99
        #
        # headerStatus
        #
        self._headerStatus.Text = "Status"
        self._headerStatus.Width = 70
        #
        # headerSavePath
        #
        self._headerSavePath.Text = "Saved Path"
        self._headerSavePath.Width = 182
        #
        # headerWorkset
        #
        self._headerWorkset.Text = "Workset"
        self._headerWorkset.Width = 119
        # headerNewPath
        #
        self._headerNewPath.Text = "New Path"
        self._headerNewPath.Width = 89
        #

        # Anchor listView
        #
        self._listView.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right
        self._listView.Location = System.Drawing.Point(12, 50)
        self._listView.Size = System.Drawing.Size(430, 341)
        #
        # Anchor groupBoxData
        #
        self._groupBoxData.Anchor = AnchorStyles.Top | AnchorStyles.Right
        self._groupBoxData.Location = System.Drawing.Point(448, 50)
        #
        # Anchor groupBoxPosition
        #
        self._groupBoxPosition.Anchor = AnchorStyles.Top | AnchorStyles.Right
        self._groupBoxPosition.Location = System.Drawing.Point(448, 182)
        #
        # Anchor Buttons
        #
        self._btnReloadFrom.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        self._btnAddLinks.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        self._btnUnload.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        self._btnReload.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        self._btnSetWorkset.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        self._btnRemove.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        self._buttonClose.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        self._btnOK.Anchor = AnchorStyles.Bottom | AnchorStyles.Right
        #
        # MainForm
        #
        self.AcceptButton = self._btnOK
        self.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
        self.BackColor = System.Drawing.SystemColors.Control
        self.CancelButton = self._buttonClose
        self.ClientSize = System.Drawing.Size(654, 403)
        self.Controls.Add(self._labelAuthor)
        self.Controls.Add(self._linkHelp)
        self.Controls.Add(self._btnOK)
        self.Controls.Add(self._btnRemove)
        self.Controls.Add(self._btnReload)
        self.Controls.Add(self._buttonClose)
        self.Controls.Add(self._btnAddLinks)
        self.Controls.Add(self._btnSetWorkset)
        self.Controls.Add(self._btnUnload)
        self.Controls.Add(self._btnReloadFrom)
        self.Controls.Add(self._groupBoxPosition)
        self.Controls.Add(self._groupBoxData)
        self.Controls.Add(self._textBoxFind)
        self.Controls.Add(self._labelFind)
        self.Controls.Add(self._checkBoxSelectAll)
        self.Controls.Add(self._listView)
        self.MinimumSize = System.Drawing.Size(670, 442)
        self.Name = "MainForm"
        self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
        self.Text = "Manange Links"
        self._groupBoxData.ResumeLayout(False)
        self._groupBoxPosition.ResumeLayout(False)
        self.ResumeLayout(False)
        self.PerformLayout()

    def CheckBoxSelectAllCheckedChanged(self, sender, e):
        """List View"""
        # Status of checkbox
        isChecked = self._checkBoxSelectAll.Checked

        # Lặp qua tất cả các item trong ListView và thay đổi trạng thái checkbox
        for item in self._listView.Items:
            item.Checked = isChecked  # Đánh dấu hoặc bỏ đánh dấu các checkbox

    def TextBoxFindTextChanged(self, sender, e):
        # Lấy giá trị tìm kiếm từ TextBox
        searchText = self._textBoxFind.Text.strip().lower()

        # Xóa tất cả các mục hiện tại trong ListView
        self._listView.Items.Clear()

        if not searchText:  # Nếu TextBox trống, khôi phục lại toàn bộ danh sách
            for item in self.originalItems:
                self._listView.Items.Add(item)
        else:  # Chỉ hiển thị các mục khớp với điều kiện
            for item in self.originalItems:
                if item.Text.lower().startswith(searchText):
                    self._listView.Items.Add(item)

    def ListViewSelectedIndexChanged(self, sender, e):
        pass

    def ListViewResize(self, sender, e):
        """Ensure al the column will be fulfilled in the list view"""
        # Calculate the width of each column
        totalWidth = self._listView.ClientSize.Width
        colCount = len(self._listView.Columns)
        if colCount > 0:
            colWidth = totalWidth // colCount
            # Set width for each column
            for column in self._listView.Columns:
                column.Width = colWidth

    def LinkHelpLinkClicked(self, sender, e):
        System.Diagnostics.Process.Start("https://www.youtube.com/@paper.engineer")

    def BtnBrowseClick(self, sender, e):
        self.browseFolder = forms.pick_folder()

        return self.browseFolder

    def ComboBoxWorksetSelectedIndexChanged(self, sender, e):
        pass

    def RadioButtonOriginCheckedChanged(self, sender, e):
        pass

    def RadioButtonSharedCheckedChanged(self, sender, e):
        pass

    def BtnAddLinksClick(self, sender, e):
        # addFolder = forms.pick_file(files_filter='(*.rvt)''(*.dwg)',multi_file=True)
        # addFolder = forms.pick_file(
        #     files_filter='All Files (*.*)|*.*|'
        #                  'Excel Workbook (*.xlsx)|*.xlsx|'
        #                  'Excel 97-2003 Workbook (*.xls)|*.xls|'
        #                  'RVT Files (*.rvt)|*.rvt',
        #     multi_file=True
        # )

        self.addRVTFile = forms.pick_file(
            files_filter='RVT Files (*.rvt)|*.rvt',
            multi_file=True
        )

        return self.addRVTFile

    def BtnReloadFromClick(self, sender, e):
        pass

    def BtnReloadClick(self, sender, e):
        selectedItems = [item for item in self._listView.Items if item.Checked]

        if not selectedItems:
            return

        with Transaction(doc, "Reload Links") as t:
            t.Start()


    def BtnUnloadClick(self, sender, e):
        pass

    def BtnRemoveClick(self, sender, e):
        pass

    def BtnSetWorksetClick(self, sender, e):
        pass

    def BtnOKClick(self, sender, e):
        pass

    def ButtonCloseClick(self, sender, e):
        pass
