from webdata.recipe import *
from webdata.prices_walmart import *
from webdata.search import search_recipes
import pandas as pd
import time

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

test = ["turkey", "bacon", "toast", "cheese"]
t1 = time.perf_counter()
info = get_recipes(test)
df = get_data(info)
# t2 = time.perf_counter()
# print(f"Functions took {t2 - t1:0.4f} seconds")
# tic = time.perf_counter()
# Calories(df)
# Proteins(df)
# Carbs(df)
# toc = time.perf_counter()
# print(f"Functions took {toc - tic:0.4f} seconds")
