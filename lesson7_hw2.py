import os
from pprint import pprint

FILE_PATH = os.path.join(os.getcwd(), 'recipes.txt')  # Get current filepath


def recipes_parse(filename, encoding='utf-8'):
    res = {}
    with open(filename, encoding=encoding) as recipes:
        line = recipes.readline()
        point = 'recipe_name'
        recipe_name = ''
        while line != '':  # while not EOF
            line = line.strip()
            if point == 'recipe_name':
                point = 'num_of_ingredients'
                recipe_name = line
                res[line] = []
                line = recipes.readline()
                continue
            if point == 'num_of_ingredients':
                point = 'ingredients'
                line = recipes.readline()
                continue
            if point == 'ingredients':
                temp_list = line.split('|')
                if len(temp_list) != 3:  # check for the number of positions in the list
                    point = 'recipe_name'
                    recipe_name = ''
                    line = recipes.readline()
                    continue
                temp_dict = dict(zip(['ingredient_name', 'quantity', 'measure'],
                                     [i.strip() for i in temp_list]))
                res[recipe_name].append(temp_dict)
            line = recipes.readline()
    return res


def get_shop_list_by_dishes(dishes, person_count, filename):
    res = {}
    for dish in dishes:
        ingredients = recipes_parse(filename)[dish]  # Get parsed cook_book
        for item in ingredients:  # And
            item_name = item['ingredient_name']
            item_search = res.setdefault(
                item_name, {'measure': item['measure'], 'quantity': 0})
            item_search['quantity'] = item_search['quantity'] + \
                int(item['quantity']) * person_count
            res[item_name] = item_search
    return res


print('\nСписок покупок:')
pprint(get_shop_list_by_dishes(['Омлет', 'Фахитос'], 2, FILE_PATH))
