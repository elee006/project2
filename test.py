from webdata.recipe import *
from webdata.prices_walmart import *
from webdata.search import search_recipes
import pandas as pd

# test = ['eggs,']
# r = get_recipes(test)
# # for stiff in content:
# #     #i[0] = recipe name
# #     #i[1] = serving 
# #     #i[2] = time to cook
# #     #i[3] = summary
# #     #i[4] = ingredient list
# #     #i[5] = instructions
# #     #i[6] = nutrients
# #     #i[7] = image
# #     #i[8] = source
# #     #i[9] = id
# #     print(i[6].key())
# #     print()
# test2 = 479101
# b = getrecipe(test2)
# # print(b)

test = ["flour", "rice","sugar"]
info = get_recipes(test)
df = get_data(info)
print(df)
Calories(df)
# Proteins(df)
# Carbs(df)
# prices(df)
