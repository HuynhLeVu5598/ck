import pandas as pd
from nobarcode.models import Order

def import_data_from_excel(file_path):
    # Đọc dữ liệu từ Excel bằng pandas
    df = pd.read_excel(file_path)

    # Lặp qua từng dòng trong dataframe và thêm vào mô hình Django
    for index, row in df.iterrows():
        # Tạo một đối tượng mô hình mới từ dữ liệu Excel
        new_object = Order(
            field1=row['sno'],
            field2=row['type_s'],
            field3=row['materials'],
            field4=row['specification'],
            # ...Thêm các trường khác tương ứng
        )

        # Lưu đối tượng vào cơ sở dữ liệu
        new_object.save()

# Gọi hàm với đường dẫn đến tệp Excel
file_path = "D:/ckv2/cokhi/excel/Order.xlsx"
import_data_from_excel(file_path)
