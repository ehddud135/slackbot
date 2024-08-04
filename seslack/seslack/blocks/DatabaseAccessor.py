import sqlite3
import pandas as pd
import tabulate as tb
from tabulate import tabulate

tabulate.WIDE_CHARS_MODE = True


class DatabaseAccessor():
    def __init__(self):
        self.db_path = "/home/stealien/slackbot/seslack/db.sqlite3"

    def get_options(self, column, table_name):
        dbconn = sqlite3.connect(self.db_path)
        cursor = dbconn.cursor()
        cursor.execute(f"select {column} from {table_name}")
        result = cursor.fetchall()
        dbconn.close()
        return result

    def get_manager_name(self, user_id):
        dbconn = sqlite3.connect(self.db_path)
        cursor = dbconn.cursor()
        cursor.execute(f"select manager_name from ManagerList where user_id='{user_id}'")
        result = cursor.fetchall()
        dbconn.close()
        return result

    def get_table(self, table_name):
        dbconn = sqlite3.connect(self.db_path)
        df = pd.read_sql(f"SELECT * FROM {table_name}", dbconn, index_col=None)
        dbconn.close()
        header_list = df.columns.to_list()
        fixed_width_headers = [header.center(17) for header in header_list]
        result = tabulate(df, fixed_width_headers, tablefmt='pretty', showindex=False)
        return result
