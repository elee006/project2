import requests
from webdata.recipe import getrecipe

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/mealplans/generate"


headers = {
    'x-rapidapi-key': "cdcc19f7bemshcaafa6b12f20c45p1ec5eajsn982786737a25",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }


ex = {'Calories':"2000", 'Exclude':"salt, butter", 'Option': ""}
def get_meals(dic):
    res = []
    rep = []
    ids = []
    nutrients = {}
    querystring = {"timeFrame":"day","targetCalories":dic['Calories'],"diet":"","exclude":dic['Exclude']}
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    data = response.json()
    for k,v in data.items():
        if k == "meals":
            for items in v:
                ids.append(items['id'])
        if k == 'nutrients':
            nutrients = v
    
    for id in ids:
        recipe = getrecipe(id)
        rep.append(recipe)
        
    res = [rep,nutrients]
    return res

