import sqlite3
import pandas as pd
from tabulate import tabulate


dbconn = sqlite3.connect(r"D:\automation\slack_bot\seslack\db.sqlite3")

df = pd.read_sql("SELECT * FROM customer_customerlist", dbconn, index_col=None)

print(df)

print(type(tabulate(df, headers='keys', tablefmt='psql', showindex=True)))
