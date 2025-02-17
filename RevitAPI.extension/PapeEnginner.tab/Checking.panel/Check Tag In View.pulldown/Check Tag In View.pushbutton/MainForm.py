# -*- coding: utf-8 -*-
from mailbox import Message

import clr
import System
import string
import os
import random
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
selection = uidoc.Selection
uiview = [x for x in uiviews if x.ViewId == view.Id][0]
"""-------------------------------------------------------------------------------------------"""


class MainForm(Form):
    def __init__(self, category, familyName, typeName, Id, processCateTag, selectCateName, notTaggedCategoryGroup,
                 data):
        self.category = category
        self.familyName = familyName
        self.typeName = typeName
        self.Id = Id

        self.processCateTag = processCateTag
        self.selectCateName = selectCateName
        self.sheetsTitle = notTaggedCategoryGroup
        self.data = data

        self.imageList = [
            os.path.join(__commandpath__, "image1.jpg"),
            os.path.join(__commandpath__, "image2.jpg"),
            os.path.join(__commandpath__, "image3.jpg"),
            os.path.join(__commandpath__, "image4.jpg"),
        ]

        self.InitializeComponent()
        self.LoadData()
        self.LoadCategoryFilterItems()
        self.LoadFamilyFilterItems()

    def InitializeComponent(self):
        # Get the directory of the running script
        # script_dir = os.path.dirname(__file__)
        image_path = os.path.join(__commandpath__, "image.jpg")
        icon_path = os.path.join(__commandpath__, "icon.ico")
        # Load custom icon (if available)
        if os.path.exists(icon_path):
            self.Icon = Icon(icon_path)

        self._splitContainer1 = System.Windows.Forms.SplitContainer()
        self._splitContainer2 = System.Windows.Forms.SplitContainer()
        self._exportExcelBtn = System.Windows.Forms.Button()
        self._noTagBtn = System.Windows.Forms.Button()
        self._closeBtn = System.Windows.Forms.Button()
        self._pictureBox = System.Windows.Forms.PictureBox()
        self._dataGridView1 = System.Windows.Forms.DataGridView()
        self._Column1 = System.Windows.Forms.DataGridViewCheckBoxColumn()
        self._Column2 = System.Windows.Forms.DataGridViewTextBoxColumn()
        self._Column3 = System.Windows.Forms.DataGridViewTextBoxColumn()
        self._Column4 = System.Windows.Forms.DataGridViewTextBoxColumn()
        self._Column5 = System.Windows.Forms.DataGridViewTextBoxColumn()
        self._Column6 = System.Windows.Forms.DataGridViewButtonColumn()
        self._toolStrip1 = System.Windows.Forms.ToolStrip()
        self._panel1 = System.Windows.Forms.Panel()
        self._splitContainer1.BeginInit()
        self._splitContainer1.Panel1.SuspendLayout()
        self._splitContainer1.Panel2.SuspendLayout()
        self._splitContainer1.SuspendLayout()
        self._splitContainer2.BeginInit()
        self._splitContainer2.Panel1.SuspendLayout()
        self._splitContainer2.Panel2.SuspendLayout()
        self._splitContainer2.SuspendLayout()
        self._pictureBox.BeginInit()
        self._dataGridView1.BeginInit()
        self._panel1.SuspendLayout()
        self.SuspendLayout()
        #
        # ✅ Thêm padding cho các container
        #
        self.Padding = System.Windows.Forms.Padding(10)
        #
        # splitContainer1
        #
        self._splitContainer1.Dock = System.Windows.Forms.DockStyle.Fill
        self._splitContainer1.Location = System.Drawing.Point(0, 0)
        self._splitContainer1.Name = "splitContainer1"
        self._splitContainer1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        self._splitContainer1.SplitterWidth = 2  # Độ dày đường viền
        self._splitContainer1.Margin = System.Windows.Forms.Padding(5)
        #
        # ✅ Tạo khoảng cách bên trong SplitContainer
        #
        self._splitContainer1.Panel1.Padding = System.Windows.Forms.Padding(5)
        self._splitContainer1.Panel2.Padding = System.Windows.Forms.Padding(0)
        #
        # splitContainer1.Panel1
        #
        self._splitContainer1.Panel1.Controls.Add(self._panel1)
        self._splitContainer1.Panel1.Controls.Add(self._toolStrip1)
        #
        # splitContainer1.Panel2
        #
        self._splitContainer1.Panel2.Controls.Add(self._splitContainer2)
        self._splitContainer1.Size = System.Drawing.Size(561, 475)
        self._splitContainer1.SplitterDistance = 441
        self._splitContainer1.TabIndex = 0
        #
        # splitContainer2
        #
        self._splitContainer2.Dock = System.Windows.Forms.DockStyle.Fill
        self._splitContainer2.Location = System.Drawing.Point(0, 0)
        self._splitContainer2.Name = "splitContainer2"
        self._splitContainer2.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        self._splitContainer2.SplitterWidth = 2  # Độ dày đường viền
        self._splitContainer2.Orientation = System.Windows.Forms.Orientation.Horizontal
        self._splitContainer2.Panel1.Padding = System.Windows.Forms.Padding(5)
        self._splitContainer2.Panel2.Padding = System.Windows.Forms.Padding(5)
        #
        # splitContainer2.Panel1
        #
        self._splitContainer2.Panel1.Controls.Add(self._pictureBox)
        #
        # splitContainer2.Panel2
        #
        self._splitContainer2.Panel2.Controls.Add(self._closeBtn)
        self._splitContainer2.Panel2.Controls.Add(self._noTagBtn)
        self._splitContainer2.Panel2.Controls.Add(self._exportExcelBtn)
        self._splitContainer2.Size = System.Drawing.Size(116, 475)
        self._splitContainer2.SplitterDistance = 104
        self._splitContainer2.TabIndex = 1
        #
        # noTagBtn
        #
        self._noTagBtn.Location = System.Drawing.Point(13, 80)
        self._noTagBtn.Margin = System.Windows.Forms.Padding(3, 10, 3, 10)
        self._noTagBtn.Name = "noTagBtn"
        self._noTagBtn.Size = System.Drawing.Size(84, 34)
        self._noTagBtn.TabIndex = 3
        self._noTagBtn.Text = "Export No Tagged"
        self._noTagBtn.UseVisualStyleBackColor = True
        self._noTagBtn.Click += self.NoTagBtnClick

        #
        # exportExcelBtn
        #
        self._exportExcelBtn.Location = System.Drawing.Point(13, 12)
        self._exportExcelBtn.Name = "exportExcelBtn"
        self._exportExcelBtn.Size = System.Drawing.Size(84, 34)
        self._exportExcelBtn.TabIndex = 0
        self._exportExcelBtn.Text = "Export Excel"
        self._exportExcelBtn.UseVisualStyleBackColor = True
        self._exportExcelBtn.Click += self.ExportExcelBtnClick
        self._exportExcelBtn.Margin = System.Windows.Forms.Padding(0, 10, 0, 10)
        # ✅ Thêm Anchor để căn giữa khi kéo dãn
        self._noTagBtn.Anchor = System.Windows.Forms.AnchorStyles.Top
        #
        # closeBtn
        #
        self._closeBtn.DialogResult = System.Windows.Forms.DialogResult.Cancel
        self._closeBtn.Location = System.Drawing.Point(13, 321)
        self._closeBtn.Name = "closeBtn"
        self._closeBtn.Size = System.Drawing.Size(84, 34)
        self._closeBtn.TabIndex = 2
        self._closeBtn.Text = "Close"
        self._closeBtn.UseVisualStyleBackColor = True
        self._closeBtn.Click += self.CloseBtnClick
        self._closeBtn.Margin = System.Windows.Forms.Padding(0, 10, 0, 10)
        #
        # pictureBox
        #
        self._pictureBox.Image = Image.FromFile(image_path)
        self._pictureBox.Dock = System.Windows.Forms.DockStyle.Fill
        self._pictureBox.Location = System.Drawing.Point(0, 0)
        self._pictureBox.Name = "pictureBox"
        self._pictureBox.Size = System.Drawing.Size(116, 104)
        self._pictureBox.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
        self._pictureBox.TabIndex = 0
        self._pictureBox.TabStop = False
        self._pictureBox.Click += self.PictureBoxClick
        self._pictureBox.Margin = System.Windows.Forms.Padding(5)
        #
        # dataGridView1
        #
        self._dataGridView1.AllowUserToAddRows = False
        self._dataGridView1.AllowUserToDeleteRows = False
        self._dataGridView1.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize
        self._dataGridView1.Columns.AddRange(System.Array[System.Windows.Forms.DataGridViewColumn](
            [self._Column1,
             self._Column2,
             self._Column3,
             self._Column4,
             self._Column5,
             self._Column6]))
        self._dataGridView1.Dock = System.Windows.Forms.DockStyle.Fill
        self._dataGridView1.Location = System.Drawing.Point(0, 0)
        self._dataGridView1.Margin = System.Windows.Forms.Padding(3, 10, 3, 3)
        self._dataGridView1.Name = "dataGridView1"
        self._dataGridView1.RowHeadersVisible = False
        self._dataGridView1.Size = System.Drawing.Size(441, 450)
        self._dataGridView1.TabIndex = 1
        self._dataGridView1.Margin = System.Windows.Forms.Padding(5)
        self._dataGridView1.CellContentClick += self.DataGridView1CellContentClick  # Bind click event
        #
        # Column1
        #
        self._Column1.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.ColumnHeader
        self._Column1.HeaderText = "Done"
        self._Column1.Name = "Column1"
        self._Column5.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.ColumnHeader
        self._Column1.ToolTipText = "Check this when you've resolved"
        self._Column1.Width = 39
        #
        # Column2
        #
        self._Column2.HeaderText = "Category"
        self._Column2.Name = "Column2"
        self._Column5.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.Fill
        #
        # Column3
        #
        self._Column3.HeaderText = "Family Name"
        self._Column3.Name = "Column3"
        #
        # Column4
        #
        self._Column4.HeaderText = "Type Name"
        self._Column4.Name = "Column4"
        #
        # Column5
        #
        self._Column5.HeaderText = "ID"
        self._Column5.Name = "Column5"
        self._Column5.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.Fill
        self._Column5.SortMode = System.Windows.Forms.DataGridViewColumnSortMode.NotSortable
        #
        # Column6
        #
        self._Column6.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.DisplayedCells
        self._Column6.HeaderText = "Find"
        self._Column6.Name = "Column6"
        self._Column5.AutoSizeMode = System.Windows.Forms.DataGridViewAutoSizeColumnMode.Fill
        self._Column6.Text = "Zoom into Element"
        self._Column6.Width = 33
        #
        # toolStrip1
        #
        self._toolStrip1.Location = System.Drawing.Point(0, 0)
        self._toolStrip1.Name = "toolStrip1"
        self._toolStrip1.Size = System.Drawing.Size(441, 25)
        self._toolStrip1.TabIndex = 2
        self._toolStrip1.Text = "toolStrip1"
        self._toolStrip1.Padding = System.Windows.Forms.Padding(5)

        self._toolStrip1.AutoSize = True
        self._toolStrip1.Dock = System.Windows.Forms.DockStyle.Top

        # Dropdown lọc theo Category
        self._categoryFilterDropdown = System.Windows.Forms.ToolStripDropDownButton("Category Filter")
        self._allCategoryItem = System.Windows.Forms.ToolStripMenuItem("All", CheckOnClick=True)
        self._allCategoryItem.Checked = True
        self._allCategoryItem.Click += self.CategoryFilterChanged
        self._categoryFilterDropdown.DropDownItems.Add(self._allCategoryItem)
        self._toolStrip1.Items.Add(self._categoryFilterDropdown)
        # Dropdown lọc theo FamilyName
        self._familyFilterDropdown = System.Windows.Forms.ToolStripDropDownButton("Family Name Filter")
        self._allFamilyItem = System.Windows.Forms.ToolStripMenuItem("All", CheckOnClick=True)
        self._allFamilyItem.Checked = True
        self._allFamilyItem.Click += self.FamilyFilterChanged
        self._familyFilterDropdown.DropDownItems.Add(self._allFamilyItem)
        self._toolStrip1.Items.Add(self._familyFilterDropdown)

        self.LoadCategoryFilterItems()
        self.LoadFamilyFilterItems()
        #
        # panel1
        #
        self._panel1.Controls.Add(self._dataGridView1)
        self._panel1.Dock = System.Windows.Forms.DockStyle.Fill
        self._panel1.Location = System.Drawing.Point(0, 25)
        self._panel1.Name = "panel1"
        self._panel1.Size = System.Drawing.Size(441, 450)
        self._panel1.TabIndex = 3
        #
        # MainForm
        #
        # self.AcceptButton = self._closeBtn
        self.CancelButton = self._closeBtn
        self.BackColor = System.Drawing.SystemColors.ControlLightLight
        self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
        self.ClientSize = System.Drawing.Size(561, 475)
        self.MinimumSize = self.Size  # Lấy kích thước hiện tại làm MinimumSize
        self.Controls.Add(self._splitContainer1)
        self.Name = "MainForm"
        self.Text = "Export Data"
        self._splitContainer1.Panel1.ResumeLayout(False)
        self._splitContainer1.Panel1.PerformLayout()
        self._splitContainer1.Panel2.ResumeLayout(False)
        self._splitContainer1.EndInit()
        self._splitContainer1.ResumeLayout(False)
        self._splitContainer2.Panel1.ResumeLayout(False)
        self._splitContainer2.Panel1.PerformLayout()
        self._splitContainer2.Panel2.ResumeLayout(False)
        self._splitContainer2.EndInit()
        self._splitContainer2.ResumeLayout(False)
        self._pictureBox.EndInit()
        self._dataGridView1.EndInit()
        self._panel1.ResumeLayout(False)
        self._splitContainer1.Panel2.Resize += self.AdjustButtonPositions
        self._splitContainer2.Panel2.Resize += self.AdjustButtonPositions
        self.ResumeLayout(False)

    def LoadData(self):
        self._dataGridView1.Rows.Clear()
        for category, family, type_name, element_id in zip(self.category, self.familyName, self.typeName, self.Id):
            self._dataGridView1.Rows.Add(False, category, family, type_name, element_id, "Find")
        self.ApplyFilters()  # Áp dụng bộ lọc ngay khi load dữ liệu

    def LoadCategoryFilterItems(self):
        existing_categories = sorted(set(self.category))
        current_items = [item.Text for item in self._categoryFilterDropdown.DropDownItems if
                         isinstance(item, ToolStripMenuItem)]
        if current_items == ["All"] + existing_categories:
            return
        for i in range(len(self._categoryFilterDropdown.DropDownItems) - 1, 0, -1):
            self._categoryFilterDropdown.DropDownItems.RemoveAt(i)
        for cat in existing_categories:
            item = System.Windows.Forms.ToolStripMenuItem(cat, CheckOnClick=True)
            item.Checked = True
            item.Click += self.CategoryFilterChanged
            self._categoryFilterDropdown.DropDownItems.Add(item)

    def LoadFamilyFilterItems(self):
        existing_families = sorted(set(self.familyName))
        current_items = [item.Text for item in self._familyFilterDropdown.DropDownItems if
                         isinstance(item, ToolStripMenuItem)]
        if current_items == ["All"] + existing_families:
            return
        for i in range(len(self._familyFilterDropdown.DropDownItems) - 1, 0, -1):
            self._familyFilterDropdown.DropDownItems.RemoveAt(i)
        for fam in existing_families:
            item = System.Windows.Forms.ToolStripMenuItem(fam, CheckOnClick=True)
            item.Checked = True
            item.Click += self.FamilyFilterChanged
            self._familyFilterDropdown.DropDownItems.Add(item)

    def CategoryFilterChanged(self, sender, e):
        if sender.Text == "All":
            for item in self._categoryFilterDropdown.DropDownItems:
                if isinstance(item, System.Windows.Forms.ToolStripMenuItem):
                    item.Checked = sender.Checked
        self.ApplyFilters()

    def FamilyFilterChanged(self, sender, e):
        if sender.Text == "All":
            for item in self._familyFilterDropdown.DropDownItems:
                if isinstance(item, System.Windows.Forms.ToolStripMenuItem):
                    item.Checked = sender.Checked
        self.ApplyFilters()

    def ApplyFilters(self):
        selected_categories = [item.Text for item in self._categoryFilterDropdown.DropDownItems if
                               isinstance(item, System.Windows.Forms.ToolStripMenuItem) and item.Checked]
        selected_families = [item.Text for item in self._familyFilterDropdown.DropDownItems if
                             isinstance(item, System.Windows.Forms.ToolStripMenuItem) and item.Checked]
        for row in self._dataGridView1.Rows:
            category_value = str(row.Cells[1].Value)
            family_value = str(row.Cells[2].Value)
            row.Visible = (category_value in selected_categories or "All" in selected_categories) and (
                    family_value in selected_families or "All" in selected_families)

    def AdjustButtonPositions(self, sender=None, e=None):
        """ Cập nhật vị trí các nút khi thay đổi kích thước """
        panel_width = self._splitContainer2.Panel2.ClientSize.Width
        panel_height = self._splitContainer2.Panel2.ClientSize.Height

        # ✅ Căn giữa Export Excel
        self._exportExcelBtn.Left = (panel_width - self._exportExcelBtn.Width) // 2
        self._exportExcelBtn.Top = 20  # Cách trên cùng 20px

        # ✅ Căn giữa Export No Tagged
        self._noTagBtn.Left = (panel_width - self._noTagBtn.Width) // 2
        self._noTagBtn.Top = self._exportExcelBtn.Bottom + 10  # Cách Export Excel 10px

        # ✅ Căn giữa Close Button
        self._closeBtn.Left = (panel_width - self._closeBtn.Width) // 2
        self._closeBtn.Top = panel_height - self._closeBtn.Height - 20  # Cách dưới cùng 20px

    def ListView1SelectedIndexChanged(self, sender, e):
        pass

    def Transpose(self, data):
        cleaned_data = []
        for sheet_data in data:
            sheet_rows = []
            for row in sheet_data:
                if isinstance(row, tuple):  # Nếu là tuple thì giữ nguyên
                    sheet_rows.append(list(row))
                elif isinstance(row, list):  # Nếu là list thì mở rộng từng hàng
                    for sub_row in row:
                        sheet_rows.append(list(sub_row))
            cleaned_data.append(sheet_rows)

        return cleaned_data

    def ExportExcelBtnClick(self, sender, e):
        """
        Xuất dữ liệu ra file Excel với nhiều sheet.

        Args:
            self.sheetsTitle (list): Danh sách tên các sheet.
            self.data (list): Danh sách dữ liệu cấp 3.
        """
        # Kiểm tra nếu không có dữ liệu
        if not self.sheetsTitle or not self.data:
            Alert("Không có dữ liệu để xuất!")
            return

        # Chuyển vị dữ liệu trước khi xuất
        transposeData = self.Transpose(self.data)
        start_row = 1
        start_column = 1

        # Chọn nơi lưu file Excel
        file_path = forms.save_file(
            file_ext='xlsx',
            title='Chọn nơi lưu file Excel',
            default_name='ExportedData.xlsx'
        )

        if not file_path:
            Alert("No Input File Path. Cancel")
            return

        # Tạo ứng dụng Excel
        excel_app = Excel.ApplicationClass()
        excel_app.Visible = False  # Không hiển thị Excel để tăng tốc độ xử lý
        # excel_app.DisplayAlerts = False  # Tắt cảnh báo

        # Tạo workbook mới
        workbook = excel_app.Workbooks.Add()

        # Kiểm tra số lượng sheet có khớp với dữ liệu không
        if len(self.sheetsTitle) != len(transposeData):
            Alert("Data not match")
            return

        # Xóa các sheet mặc định
        while workbook.Sheets.Count > 1:
            workbook.Sheets(1).Delete()

        # Duyệt qua từng sheet
        for sheet_index, sheet_name in enumerate(self.sheetsTitle):
            # Tạo sheet mới nếu cần
            if sheet_index >= workbook.Sheets.Count:
                worksheet = workbook.Sheets.Add(After=workbook.Sheets(workbook.Sheets.Count))
            else:
                worksheet = workbook.Sheets(sheet_index + 1)

            # Đặt tên sheet (giới hạn 31 ký tự)
            worksheet.Name = sheet_name[:31]

            # Lấy dữ liệu cho sheet hiện tại
            sheet_data = transposeData[sheet_index]

            # ✅ Kiểm tra dữ liệu trước khi ghi vào Excel
            if not sheet_data or not isinstance(sheet_data, list):
                continue

            # Ghi tiêu đề cột
            worksheet.Cells(start_row, start_column).Value2 = "Family"
            worksheet.Cells(start_row, start_column + 1).Value2 = "Type"
            worksheet.Cells(start_row, start_column + 2).Value2 = "ID"

            # Ghi dữ liệu vào từng hàng & cột
            for row_idx, row_data in enumerate(sheet_data, start=start_row + 1):
                if not isinstance(row_data, list):  # Đảm bảo dữ liệu dạng list
                    continue
                for col_idx, value in enumerate(row_data):
                    worksheet.Cells(row_idx, start_column + col_idx).Value2 = value

        # Lưu workbook
        workbook.SaveAs(file_path)

        # Đóng workbook và Excel để giải phóng bộ nhớ
        workbook.Close(SaveChanges=False)
        excel_app.Quit()

        # Giải phóng bộ nhớ
        del workbook
        del excel_app

        Alert("Export Done, Please Check!")

    def NoTagBtnClick(self, sender, e):

        if self.processCateTag:
            raw = ""
            for bool, cate in zip(self.processCateTag, self.selectCateName):
                if bool == False:
                    if raw == "":
                        raw += cate
                    else:
                        raw += ", " + cate
            if raw == "":
                Alert("Nothing to export")
            else:
                Alert('Can not find any {} in view.'.format(raw))
        else:
            Alert('Do not find any not tagged categories')

    def PictureBoxClick(self, sender, e):
        imagePath = os.path.join(__commandpath__, "image.jpg")
        os.startfile(imagePath)

    def DataGridView1CellContentClick(self, sender, e):
        """Handles button clicks in the Find column."""
        if sender.Columns[e.ColumnIndex].HeaderText == "Find":  # Kiểm tra đúng cột "Find"
            selectedRow = sender.Rows[e.RowIndex]
            try:
                elementId = int(selectedRow.Cells[4].Value)  # Lấy giá trị từ cột ID
                element = doc.GetElement(ElementId(elementId))  # Lấy element từ Revit

                if element:
                    selection.SetElementIds(List[ElementId]([element.Id]))  # Chọn đối tượng
                    if isinstance(element, RevitLinkInstance):
                        # Nếu là Revit Link, cần lấy document liên kết
                        linkDoc = element.GetLinkDocument()
                        transform = element.GetTransform()
                        linkElementId = ElementId(int(selectedRow.Cells[1].Value))
                        linkElement = linkDoc.GetElement(linkElementId)

                        if linkElement and hasattr(linkElement, "get_BoundingBox"):
                            bbox = linkElement.get_BoundingBox(None)
                            if bbox:
                                # Biến đổi bounding box theo transform của link
                                pt1 = transform.OfPoint(bbox.Min)
                                pt2 = transform.OfPoint(bbox.Max)
                                uiview.ZoomAndCenterRectangle(pt1, pt2)
                    elif hasattr(element, "get_BoundingBox"):
                        # Nếu là element bình thường
                        bbox = element.get_BoundingBox(None)
                        if bbox:
                            pt1 = bbox.Min
                            pt2 = bbox.Max
                            uiview.ZoomAndCenterRectangle(pt1, pt2)
                else:
                    Alert("No found Elenent in Revit")
            except Exception as ex:
                Alert("Error: {}".format(str(ex)))

    def CloseBtnClick(self, sender, e):
        self.Close()

