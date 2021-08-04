from webdata.recipe import get_recipes,getrecipe,get_recipes_search
from webdata.prices_walmart import *
from webdata.meal import get_meals


test = ['flour', 'rice']
r = get_recipes(test)
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
#       #i[10]= vegan
#       #i[11] = vegetarian
#       #i[12] = gluten
#       #i[13] = dairy
# #     print(i[6].key())
# #     print()
# test2 = 479101
# b = getrecipe(test2)
# 
# # print(b)

ex = {'Calories':"2000", 'Exclude':"salt, butter", 'Option': ""}
print(get_meals(ex))


    
    
