import requests
import json
import pandas as pd
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import select

def makeSqlTable(df,USER, table_name):
    engine = db.create_engine("mysql://root:codio@localhost/Pokemon?charset=utf8")
    os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS '+database_name+';"')
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    return engine