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

def get_price_df(item):
    url = "https://axesso-walmart-data-service.p.rapidapi.com/wlm/walmart-search-by-keyword"
    col_names = ['Walmart Detail', 'Price in ($)', 'Price Per Quantity']
    df = pd.DataFrame(columns=col_names)

    querystring = {"type":"text","keyword":item,"page":"1","sortBy":"best_match"}

    headers = {
        'x-rapidapi-key': "02bb765496msh3d0c8b2dd4df115p112802jsna7217edf12e7",
        'x-rapidapi-host': "axesso-walmart-data-service.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()["productDetails"][0]
    print(response["primaryOffer"].keys())
    if "offerPrice" in response["primaryOffer"].keys():        
        offer_price = response["primaryOffer"]["offerPrice"]
    elif "minPrice" in response["primaryOffer"].keys():
        offer_price = response["primaryOffer"]["minPrice"]
    else:
        offer_price = 0
    if "unitPricePerQuantity" in response["primaryOffer"].keys():
        PriceperQuantity = response["primaryOffer"]["unitPricePerQuantity"]
    elif "unitPriceDisplayCondition" in response["primaryOffer"].keys():
        PriceperQuantity = response["primaryOffer"]["unitPriceDisplayCondition"]
    else:
        PriceperQuantity = "Not Found"
    info = {'Walmart Details': cleanhtml(response.get('title', "no title found")),
                     'Price in ($)': offer_price,
                     'Price Per Quantity': PriceperQuantity}
    df.loc[len(df.index)] = [info['Walmart Details'], info['Price in ($)'], info['Price Per Quantity']]
    print(df)
    
def Price(item):
    url = "https://axesso-walmart-data-service.p.rapidapi.com/wlm/walmart-search-by-keyword"
    querystring = {"type":"text","keyword":item,"page":"1","sortBy":"best_match"}

    headers = {
        'x-rapidapi-key': "02bb765496msh3d0c8b2dd4df115p112802jsna7217edf12e7",
        'x-rapidapi-host': "axesso-walmart-data-service.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()["productDetails"][0]
    if "offerPrice" in response["primaryOffer"].keys():        
        offer_price = int(response["primaryOffer"]["offerPrice"])
    elif "minPrice" in response["primaryOffer"].keys():
        offer_price = int(response["primaryOffer"]["minPrice"])
    else:
        offer_price = 0
    return offer_price

def meal_Price(ingredients):
    total_price = 0
    for ingredient in ingredients:
        cost = new_price(str(ingredient))
        total_price += cost
    print(total_price)
    return total_price

# food = ["lettuce","cheese", "onions"]
# meal_Price(food)

def new_price(text):

    if len(text) > 1:
        for i in text[0:-1]:
            i = i + "20%"
    url = "https://webknox-recipes.p.rapidapi.com/recipes/visualizePriceEstimator"

    payload = "ingredientList=" +text+ "&servings=2&defaultCss=checked&mode=1"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': "02bb765496msh3d0c8b2dd4df115p112802jsna7217edf12e7",
        'x-rapidapi-host': "webknox-recipes.p.rapidapi.com"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    clean = cleanhtml(response.text)
    clean = clean.split("$")[2]
    return float(clean)

# new_price("brocoli")

