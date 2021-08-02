from webdata.recipe import get_recipes,getrecipe
from webdata.prices_walmart import *

test = ['eggs,']
r = get_recipes(test)
# for stiff in content:
#     #i[0] = recipe name
#     #i[1] = serving 
#     #i[2] = time to cook
#     #i[3] = summary
#     #i[4] = ingredient list
#     #i[5] = instructions
#     #i[6] = nutrients
#     #i[7] = image
#     #i[8] = source
#     #i[9] = id
#     print(i[6].key())
#     print()
test2 = 479101
b = getrecipe(test2)
print(b)

test = ["lettuce","broccoli", "cheese"]
print(get_recipes(test))