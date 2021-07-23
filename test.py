from webdata.recipe import get_recipes

test = ['nothing']
r = get_recipes(test)
# for i in r:
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
print(r)