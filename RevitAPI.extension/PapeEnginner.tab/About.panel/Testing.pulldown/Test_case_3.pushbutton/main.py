from PIL import Image, ImageDraw

# Tạo một hình ảnh trắng với kích thước 200x200
img = Image.new('RGB', (200, 200), color='white')
draw = ImageDraw.Draw(img)

# Vẽ đầu mèo
draw.ellipse((50, 50, 150, 150), outline='black', fill='gray')

# Vẽ tai mèo
draw.polygon([(60, 60), (40, 100), (80, 100)], fill='gray')  # Tai trái
draw.polygon([(140, 60), (160, 100), (120, 100)], fill='gray')  # Tai phải

# Vẽ mắt mèo
draw.ellipse((80, 90, 90, 100), fill='black')  # Mắt trái
draw.ellipse((110, 90, 120, 100), fill='black')  # Mắt phải

# Vẽ miệng mèo
draw.arc((85, 110, 115, 130), start=0, end=180, fill='black')

# Lưu hình ảnh
img.save('cute_cat.png')
img.show()  # Hiển thị hình ảnh