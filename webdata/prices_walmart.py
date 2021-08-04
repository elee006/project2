import pandas as pd
import os
from sqlalchemy import create_engine
import json
import requests
import string
import re

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = remove(cleantext)
    return cleantext

def remove(string):
        escapes = ''.join([chr(char) for char in range(1, 32)])
        translator = str.maketrans('', '', escapes)
        t = string.translate(translator)
        return t

def meal_Price(ingredients):
    total_price = 0
    for ingredient in ingredients:
        cost = new_price(str(ingredient))
        total_price += cost
    return round(total_price,2)

def new_price(text):

    splt = text.split()
    new = ""
    for i in splt[0:-1]:
        i = i + "%20"
        new += i
    new += splt[-1]


    url = "https://webknox-recipes.p.rapidapi.com/recipes/visualizePriceEstimator"

    payload = "ingredientList="+new+"&servings=2&defaultCss=checked&mode=1"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': "02bb765496msh3d0c8b2dd4df115p112802jsna7217edf12e7",
        'x-rapidapi-host': "webknox-recipes.p.rapidapi.com",
        'charset':'utf-8'
        }

    response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)
    clean = cleanhtml(response.text)
    try:
        clean = float(clean.split("$")[2])
    except:
        clean = 3.00
    return round(clean,2)

# food = ["lettuce","cheese", "onions"]
# print(meal_Price(food))