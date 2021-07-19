import requests


url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

headers = {
    'x-rapidapi-key': "cdcc19f7bemshcaafa6b12f20c45p1ec5eajsn982786737a25",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

def makequery(ingredients,output_num):
    ing_string = ','.join(ingredients)
    querystring = {"ingredients":ing_string,"number":output_num,"ignorePantry":"true","ranking":"1"}
    return querystring

def getjson(query):
    response = requests.request("GET", url, headers=headers, params=query)
    return response.json()

def getinfo(response):
    maindic = {}
    for i in response:
        id = i['id']
        name = i['title']
        pic = i['image']
        maindic[id] = [name, pic]
    return maindic
    
ing = ['apples','flour','sugar']
num_of_rep = '5'

q = makequery(ing,num_of_rep)
r = getjson(q)

