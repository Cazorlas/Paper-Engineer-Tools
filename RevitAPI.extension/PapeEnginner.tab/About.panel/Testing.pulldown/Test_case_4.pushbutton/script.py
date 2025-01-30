import json
from pyrevit import forms

# Đường dẫn tới file lưu trữ lựa chọn
options_file = 'selected_options.json'


# Định nghĩa lớp MyOption để tạo các tùy chọn
class MyOption(forms.TemplateListItem):
    @property
    def name(self):
        return "Option: {}".format(self.item)


# Đọc các lựa chọn đã chọn trước đó từ file
def load_selected_options():
    try:
        with open(options_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# Lưu các lựa chọn vào file
def save_selected_options(selected):
    with open(options_file, 'w') as f:
        json.dump(selected, f)


# Lấy danh sách các tùy chọn và đánh dấu các tùy chọn đã chọn
ops = [MyOption('op1'), MyOption('op2'), MyOption('op3')]

# Đọc các tùy chọn đã chọn từ file (nếu có)
selected_options = load_selected_options()
for option in ops:
    if option.item in selected_options:
        option.checked = True

# Hiển thị hộp thoại chọn từ danh sách
res = forms.SelectFromList.show(ops,
                                multiselect=True,
                                button_name='Select Item')

# Nếu người dùng chọn, lưu lại lựa chọn
if res:
    save_selected_options([item.item for item in res])

# In kết quả lựa chọn
print('Selected items: {}'.format(res))
