import sqlite3
import pandas as pd
import tabulate as tb
from tabulate import tabulate
tabulate.WIDE_CHARS_MODE = True
tb.WIDE_CHARS_MODE = True


class DatabaseAccessor():
    def __init__(self):
        self.db_path = "/home/stealien/slackbot/seslack/db.sqlite3"

    def get_options(self, column, table_name, option1=None, option2=None):
        dbconn = sqlite3.connect(self.db_path)
        cursor = dbconn.cursor()
        if option1:
            cursor.execute(f"select {column} from {table_name} where {option1}")
            if option2:
                cursor.execute(f"select {column} from {table_name} where {option1} and {option2}")
        else:
            cursor.execute(f"select {column} from {table_name}")
        result = cursor.fetchall()
        dbconn.close()
        result = [name[0] for name in result]
        return result

    def get_manager_name(self, user_id):
        dbconn = sqlite3.connect(self.db_path)
        cursor = dbconn.cursor()
        cursor.execute(f"select name from Manager where user_id='{user_id}'")
        result = cursor.fetchone()
        dbconn.close()
        return result[0]

    def get_table(self, table_name):
        dbconn = sqlite3.connect(self.db_path)
        df = pd.read_sql(f"SELECT * FROM {table_name}", dbconn, index_col=None)
        df = df.drop(columns=['id'])
        dbconn.close()
        header_list = df.columns.to_list()
        print(header_list)
        fixed_width_headers = [header.center(17) for header in header_list]
        result = tabulate(df, fixed_width_headers, tablefmt='heavy_grid', showindex=False)
        return result
