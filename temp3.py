import pandas as pd
import pyodbc
import urllib
from sqlalchemy import create_engine


conn_str = (
    r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\jkhong\Desktop\crewPlan.accdb;'
)
# conn = pyodbc.connect(conn_str)
# cursor = conn.cursor()
# cursor.execute('select * from 2022')
query = 'select * from 2022'
conn_url = f"access+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_str)}"
acc_engine = create_engine(conn_url)

csv_path = r"W:\SP팀\크루플랜\2022\ART_Team_민청식_data.csv"
csv_data = pd.read_csv(csv_path)

csv_data.to_sql('2022', acc_engine, if_exists='append', index=False)
print('done')


# df = pd.read_sql(query, conn)
# df.to_sql('2022', cursor, if_exists='append')
# print(df.head())

# for row in cursor.fetchall():
#     print (row)




# conn = (
#     r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
#     r'DBQ=C:\Users\jkhong\Desktop\crewPlan.accdb;'
# )
# print([i for i in pyodbc.drivers() if i.startswith('MS Access Driver')])
# cursor = conn.cursor()
# cursor.excute('select * from 2022')

# for i in cursor.fetchall():
#     print(i)



# csv_path = "C:/Users/jkhong/Desktop/ANI_Team_홍진기_data.csv"
# data = pd.read_csv(csv_path)
# # # print(data.head(10))
# # # print(data['날짜'])
# # wDate  = [str(i) for i in data['날짜'] if str(i).startswith('2022-05')]
# # print(wDate)


# # pd.DataFrame({"날짜": classes})
# cnn_str = (
#     r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
#     r"DBQ=C:/Users/jkhong/Desktop/crewPlan.accdb"
# )

# cnn_url = f"access+pyodbc:///?odbc_connect={urllib.parse.quote_plus(cnn_str)}"
# acc_engine = create_engine(cnn_url)
# data.to_sql('2022', acc_engine, if_exists='append')
# print("write complete.")