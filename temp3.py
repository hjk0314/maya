import pandas as pd
import urllib
from sqlalchemy import *

csv_path = "C:/Users/jkhong/Desktop/ANI_Team_홍진기_data.csv"
data = pd.read_csv(csv_path)
# print(data.head(10))

cnn_str = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:/Users/jkhong/Desktop/crewPlan.accdb"
)

cnn_url = f"access+pyodbc:///?odbc_connect={urllib.parse.quote_plus(cnn_str)}"
acc_engine = create_engine(cnn_url)
data.to_sql('2022', acc_engine, if_exists='append')
print("write complete.")