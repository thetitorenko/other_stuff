import pandas as pd


income_table = pd.read_excel('table.xlsx', sheet_name='Бланк Заказа', header=4)
new_table = income_table.groupby('Подгруппа товара')['Артикул'].agg(', '.join)
new_table.to_excel('new_table.xlsx')
