from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models import user

class Recipe:
    db = "recipes"
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = ""
        self.select = data['select']
        self.posted_by = data['user_id']

    @classmethod
    def get_all_recipes(cls):
        query = '''SELECT * FROM recipes;
                JOIN users ON recipes.user_id = users.id;
        '''
        recipes = connectToMySQL(cls.db).query_db(query)
        print(recipes)
        return recipes

# validate recipe
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("First name must be at least 3 characters",'recipe')
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters",'recipe')
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters",'recipe')
            is_valid = False
        return is_valid
    
    # GET BY ID
    @classmethod
    def get_by_id(cls, data):
        query = '''
            SELECT * FROM recipes
            JOIN users
            ON recipes.user_id = users.id
            WHERE recipes.id = %(id)s;
        '''
        results = connectToMySQL(cls.db).query_db(query, data)
        one_listing = cls(results[0])
        for row in results:
            user_data= {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'instructions': row['instructions'],
                    'date_made': row['date_made']
                }
        one_listing = user.User(user_data)
        return one_listing
    # add recipe
    @classmethod
    def add_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions,date_made, user_id) VALUES (%(name)s, %(description)s,%(instructions)s,%(date_made)s,%(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            flash("Recipe added",'recipe')
        return results
    
    # get one recipe with user
    @classmethod
    def get_one_recipe(cls, data):
        query = '''
            SELECT * FROM recipes
            JOIN users
            ON recipes.user_id = users.id
            WHERE recipes.id = %(id)s;
        '''
        results = connectToMySQL(cls.db).query_db(query, data)
        one_listing = cls(results[0])
        for row in results:
            user_data= {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'instructions': row['instructions'],
                    'date_made': row['date_made'],
                }
            one_listing = user.User(user_data)
        return one_listing
    
    # update recipe
    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO recipes (name,description,instructions,date_made,under_30,user_id)
                VALUES (%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(under_30)s,%(user_id)s);
                """
        return connectToMySQL(cls.db).query_db(query,form_data)
            
    # delete recipe
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            flash("Recipe deleted",'recipe')
        return results
    