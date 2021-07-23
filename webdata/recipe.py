import requests
from webdata import output
from html2text import HTML2Text
from bs4 import BeautifulSoup
import mistletoe



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
        source = json['sourceUrl']
        image = json['image']
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
    info_list = [name,servings,time,summary,ingredients_list,instructions,nutrients,image,source,id]
    return(info_list)

def get_recipes(list):
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


