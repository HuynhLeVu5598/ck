# chỉ lấy cột PROCESS
# import pandas as pd
# df = pd.read_csv('excel/Order.csv')
# column_c = df['MATERIAL']
# new_df = pd.DataFrame({'MATERIAL': column_c})
# new_df.to_excel('excel/vatlie.xlsx', index=False)


# xóa giá trị trùng lặp
# import pandas as pd
# df = pd.read_excel('excel/vatlieu2.xlsx')
# df = df.drop_duplicates(subset='name', keep='first')
# df.to_excel('excel/vatlieu2.xlsx', index=False)


# chỉ lấy 3 cột
import pandas as pd
df = pd.read_excel('excel/Order.xlsx')
selected_columns = ['sno', 'type_s', 'specification']
new_df = df[selected_columns]
new_df.to_excel('excel/Order.xlsx', index=False)
