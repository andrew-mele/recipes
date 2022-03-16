from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']


    @classmethod
    def new_recipe(cls,data):
        query = "INSERT INTO recipes (name, description, instructions, user_id) VALUES (%(name)s,%(description)s,%(instructions)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_recipes(cls,data):
        query = 'SELECT * FROM recipes (name, description, instructions) VALUES (%(name)s,%(description)s,%(instructions)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def one_recipe(cls,data):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;)'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update_recipe(cls,data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL("recipes").query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            is_valid = False
            flash('Name must be at least 3 characters','recipe')
        if len(recipe['instructions']) < 3:
            is_valid = False
            flash('Instructions must be at least 3 characters','recipe')
        if len(recipe['description']) < 3:
            is_valid = False
            flash('Description must be at least 3 characters','recipe')
        return is_valid