import json
import mysql.connector
import sys

cnx = mysql.connector.connect(user='dm565sip', database='dm565', host='karvus.com', password='zipthat')
cursor = cnx.cursor()

recipe_sql_template = 'INSERT INTO recipe (id, title, instructions, total_energy, energy_per_serving, protein, fat, carbohydrates) VALUES ({id}, "{title}", "{instructions}", {nutrients[Totalkcal]}, {nutrients[kcal]}, {nutrients[protein]}, {nutrients[fat]}, {nutrients[carbohydrates]});'
ingredient_sql_template = 'INSERT INTO ingredients (recipe_id, amount, unit, name) VALUES ({id}, {amount}, "{unit}", "{name}");'

def compute_statements(recipe_json):
    recipe_stmt = recipe_sql_template.format(**recipe_json)
    ingredient_stmts = []
    for ingredient_row in recipe_json['ingredient']:
        ingredient_row['id'] = recipe_json['id']
        ingredient_stmts.append(ingredient_sql_template.format(**ingredient_row))
    return [recipe_stmt] + ingredient_stmts

if __name__ == '__main__':
    with open(sys.argv[1]) as json_file:
        recipe_json = json.load(json_file)
    statements = compute_statements(recipe_json)
    for statement in statements:
        # print(statement)
        cursor.execute(statement)
    cnx.commit()
