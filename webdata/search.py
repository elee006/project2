import requests

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/site/search"

headers = {
    'x-rapidapi-key': "cdcc19f7bemshcaafa6b12f20c45p1ec5eajsn982786737a25",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }



def search_recipes(query):
    output_lis =[]
    querystring = {"query":query}
    response = requests.request("GET", url, headers=headers, params=querystring)
    dict = response.json()
    for k,v in dict.items():
        if k=="Recipes":
            for i in v:
                link = i['link'].split('-')
                id =link[-1]
                output_lis.append(id)
    
    return output_lis