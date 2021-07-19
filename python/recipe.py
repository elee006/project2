import requests
"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/479101/information"


headers = {
    'x-rapidapi-key': "cdcc19f7bemshcaafa6b12f20c45p1ec5eajsn982786737a25",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

def create_url(id):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"+id+"/information"
    return url
response = requests.request("GET", url, headers=headers)

print(response.text)