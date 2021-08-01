import requests
import json
import pandas as pd
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import select
import sqlite3


url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

headers = {
    'x-rapidapi-key': "cdcc19f7bemshcaafa6b12f20c45p1ec5eajsn982786737a25",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

def makequery(fridge,output_num):
    ing_string = ','.join(fridge)
    querystring = {"ingredients":ing_string,"number":output_num,"ignorePantry":"true","ranking":"1"}
    return querystring

def getjson(query):
    response = requests.request("GET", url, headers=headers, params=query)
    return response.json()

def getinfo(response):
    mainlis = []
    for i in response:
        dic = {}
        if int(i['missedIngredientCount'])>3:
            continue
        id = i['id']
        name = i['title']
        pic = i['image']
        dic['ID']= id
        dic['Name']= name
        dic['Picture'] = pic
        mainlis.append(dic)
    return mainlis

def dataframe(dic):
    col_names = ['ID', 'Name','Picture']
    df = pd.DataFrame.from_dict(dic)
    return df

def output(lis):
    num_of_rep = '10'
    q = makequery(lis,num_of_rep)
    r = getjson(q)
    m = getinfo(r)
    return m

def fridge_list():
    con = sqlite3.connect("sqlite:///site.db")
    df = pd.read_sql_query("SELECT * Users", con)
    print(df.head())
    
#fridge_list()
# num_of_rep = '10'
# test = ['chicken','curry','rice','beans']
# d = output(test)
# print(d)

