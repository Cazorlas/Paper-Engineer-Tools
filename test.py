from rembg import remove
from PIL import Image
import os

# Đường dẫn tệp đầu vào
input_path = r'D:\meo.jpg'

# Tạo đường dẫn tệp đầu ra trong cùng thư mục
output_path = os.path.join(os.path.dirname(input_path), 'meo_output.png')

# Mở hình ảnh đầu vào và xử lý
with open(input_path, 'rb') as inp_file:
    inp_image = inp_file.read()

output_image = remove(inp_image)

# Lưu hình ảnh kết quả vào tệp đầu ra
with open(output_path, 'wb') as out_file:
    out_file.write(output_image)

print("Hoàn tất! Ảnh đã được lưu tại:", output_path)
