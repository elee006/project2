import requests



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
    m = []
    o = []
    ingredients_list =[]
    instructions = []
    nutrients ={}
    for k,v in json.items():
        name = json['title']
        servings = json['servings']
        time = json['readyInMinutes']
        summary = json['summary']
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
    info_list = [name,servings,time,summary]
    return(info_list,ingredients_list,instructions,nutrients)

    
id = 657563
url = create_url(id)
j = getjson(url)
i,b,c,a = getinfo(j)
print(a)
        