import requests

url = ""

headers = {
    'x-rapidapi-key': "cdcc19f7bemshcaafa6b12f20c45p1ec5eajsn982786737a25",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

def get_ans(choice):
    if choice == "trivia":
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/trivia/random"
    if choice == "joke":
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/jokes/random"
    response = requests.request("GET", url, headers=headers)
    r = response.json()
    return(r['text'])

choice = "joke"
print(get_ans(choice))
    
