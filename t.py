import pandas as pd

def excel_to_dict(file_path, sheet_name):
    # Đọc file Excel vào DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Tạo từ điển từ cột A và cột B sau khi loại bỏ khoảng trống ở đầu và cuối
    excel_dict = {}
    for key, value in zip(df['MATERIAL CODE'], df['STANDARD CODE 1']):
        key_stripped = str(key).strip()
        value_stripped = str(value).strip()
        if key_stripped not in excel_dict:
            excel_dict[key_stripped] = [value_stripped]  # Tạo danh sách mới nếu key chưa tồn tại
        else:
            excel_dict[key_stripped].append(value_stripped)  # Nếu key đã tồn tại, thêm giá trị vào danh sách

    return excel_dict

file_path = 'a.xlsx'
sheet_name = 'LAM'  # Thay thế 'Tên của sheet' bằng tên sheet thực tế

result_dict = excel_to_dict(file_path, sheet_name)

# In kết quả
print(result_dict)
