import requests
from webdata import output
from html2text import HTML2Text
from bs4 import BeautifulSoup
from webdata.search import search_recipes
import mistletoe
import pandas as pd
import numpy as np
import plotly.express as px
from webdata.prices_walmart import *
import time


headers = {
    'x-rapidapi-key': "cdcc19f7bemshcaafa6b12f20c45p1ec5eajsn982786737a25",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
querystring = {"includeNutrition":"true"}

def create_url(id):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"+str(id)+"/information"
    return url

def getjson(url):
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

def getinfo(json):
    name = ''
    servings = ''
    time = ''
    summary = ''
    vegan = ''
    vegetarian = ''
    dairy = ''
    gluten = ''
    m = []
    o = []
    ingredients_list =[]
    instructions = []
    nutrients ={}
    for k,v in json.items():
        name = json['title']
        vegan = json['vegan']
        vegetarian = json['vegetarian']
        dairy = json['dairyFree']
        gluten = json['glutenFree']
        servings = json['servings']
        time = json['readyInMinutes']
        source = json['sourceUrl']
        if 'image' in json:
            image = json['image']
        else:
            image = 'https://i.postimg.cc/htCvg6qH/No-Image-Found-400x264.png'
        id = json['id']
        summary = BeautifulSoup(json['summary']).getText()
        m = json["extendedIngredients"]
        o = json['analyzedInstructions']
        if k == 'nutrition':
            for s in v["nutrients"]:
                nutrients[s['name']]=[s['amount'],s['unit']]
    for item in m:
        r = item["originalString"]
        ingredients_list.append(r)
    
    for item in o:
        for key,val in item.items():
            if key == 'steps':
                for num in val:
                    for key,val in num.items():
                        if key == 'step':
                            instructions.append(val)
    info_list = [name,servings,time,summary,ingredients_list,instructions,nutrients,image,source,id, vegan, vegetarian,gluten,dairy]
    return(info_list)

    
def get_recipes(list, option = None):
    res = []    
    run = output(list)
    ids = []
    for i in run:
        ids.append(i['ID'])
    for id in ids:
        url = create_url(id)
        j = getjson(url)
        i = getinfo(j)
        res.append(i)
    return res

def get_data(test):
    
    new_list = []
    calories = []
    carbs = []
    proteins = []
    food_names = []
    dictionary = {}
    col_names = ['Recipe Name', 'Recipe Price', 'Calories', 'Carbs (g)', 'Proteins (g)']
    for i in test:
        print(i[3])
        print("")
        new_list.append(i[4])
        calories.append(i[6]['Calories'][0])
        carbs.append(i[6]['Carbohydrates'][0])
        proteins.append(i[6]['Protein'][0])
        food_names.append(i[0])    
    text = []
    for o in new_list:
        string = []
        for words in o:
            if "," in words:
                replace = words.split(",")
                words = replace[0]
                if words[-1].isalpha() == False:
                    words = words[:-2]
            elif "I" in words:
                replace = words.split("I")
                words = replace[0]
                if words[-1].isalpha() == False:
                    words = words[:-2]
            string.append(words)
        text.append(string)
    t1 = time.perf_counter()
    t2 = time.perf_counter()
    df = pd.DataFrame(columns = col_names)
    df['Recipe Name'] = food_names
    df['Calories'] = calories
    df['Carbs (g)'] = carbs
    df['Proteins (g)'] = proteins    
    return df

def Calories(df):
    fig = px.scatter(df, x=df['Recipe Name'], y= df['Calories'], color=df['Calories'], title = 'Calories', size = df["Calories"])
    fig.update_traces(mode="markers+lines")
    fig.write_html('templates/Calories.html')

def Proteins(df):
    fig = px.scatter(df, x=df['Recipe Name'], y= df['Proteins (g)'], title = 'Proteins', color=df['Calories'], size = df["Calories"])
    fig.update_traces(mode="markers+lines")
    fig.write_html('templates/proteins.html')
    
def Carbs(df):
    fig = px.scatter(df, x=df['Recipe Name'], y= df['Carbs (g)'], title = 'Carbs', color=df['Calories'], size = df["Calories"])
    fig.update_traces(mode="markers+lines")
    fig.write_html('templates/carbs.html')
    
# def prices(df):
#     fig = px.scatter(df, x=df['Recipe Name'], y= df['Recipe Price'], title = 'Recipe Prices', color=df['Calories'], size = df["Recipe Price"])
#     fig.update_traces(mode="markers+lines")
#     fig.write_html('templates/prices.html')
    
def get_recipes_search(query):
    ids = search_recipes(query)
    res=[]
    for id in ids:
        url = create_url(id)
        j = getjson(url)
        i = getinfo(j)
        res.append(i)
    return res
    

def html2md(html):
    parser = HTML2Text()
    parser.ignore_images = True
    parser.ignore_anchors = True
    parser.body_width = 0
    md = parser.handle(html)
    return md

def html2plain(html):
    # HTML to Markdown
    md = html2md(html)
    # Normalise custom lists
    md = re.sub(r'(^|\n) ? ? ?\\?[•·–-—-*]( \w)', r'\1  *\2', md)
    # Convert back into HTML
    html_simple = mistletoe.markdown(md)
    # Convert to plain text
    soup = BeautifulSoup(html_simple, features = "html.parser")
    text = soup.getText()
    # Strip off table formatting
    text = re.sub(r'(^|\n)\|\s*', r'\1', text)
    # Strip off extra emphasis
    text = re.sub(r'\*\*', '', text)
    # Remove trailing whitespace and leading newlines
    text = re.sub(r' *$', '', text)
    text = re.sub(r'\n\n+', r'\n\n', text)
    text = re.sub(r'^\n+', '', text)
    return text

def getrecipe(id):
    if id == '':
        return "none"
    name = ''
    pic = ''
    summary = ''
    link = ''
    servings = ''
    time = ''
    url = create_url(id)
    j = getjson(url)
    for k,v in j.items():
        name = j['title']
        pic = j['image']
        link = j['sourceUrl']
        summary = BeautifulSoup(j['summary']).getText()
    fix_name = (name[:25] + '...') if len(name) > 25 else name
    fix_sum = (summary[:102] + '...') if len(summary) > 102 else summary
    out = [fix_name,pic,fix_sum,link]
    return out
    



