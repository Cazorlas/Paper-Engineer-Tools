import cv2
import pytesseract
import pandas as pd
import re

# Đường dẫn đến file hình ảnh
image_path = '/mnt/data/image.png'
output_excel_path = '/mnt/data/output.xlsx'

# Đọc hình ảnh
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Tiền xử lý hình ảnh
gray = cv2.medianBlur(gray, 3)

# Trích xuất văn bản từ hình ảnh
text = pytesseract.image_to_string(gray, config='--psm 6')

# Tách các dòng văn bản
lines = text.split('\n')

# Khởi tạo danh sách dữ liệu
data = []
rows = []

# Duyệt qua từng dòng và trích xuất dữ liệu
for line in lines:
    if re.match(r'^\d+', line):  # Dòng bắt đầu bằng số
        parts = re.findall(r'(\d{3,4})', line)
        if len(parts) > 1:
            row_header = parts[0]
            for col_index, value in enumerate(parts[1:]):
                col_header = 150 + col_index * 50
                data.append([f'{row_header}x{col_header}', value])

# Chuyển dữ liệu thành DataFrame
output_df = pd.DataFrame(data, columns=['A', 'B'])

# Xuất ra file Excel
output_df.to_excel(output_excel_path, index=False)

print(f'Dữ liệu đã được xuất ra file: {output_excel_path}')
