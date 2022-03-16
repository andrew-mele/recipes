from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


class User:
    db = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_email(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(User.db).query_db(query, user)
        print(result)
        if len(user['first_name']) < 3:
            flash('First name must be at least 2 characters.','register')
            is_valid = False
        if len(user['last_name']) < 3:
            flash('Last name must be at least 3 characters.','register')
            is_valid = False
        if len(result) >= 1:
            flash('Email has already been registered. Please use another Email address.','register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email.')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password does not meet length requirement of 8 characters.','register')
            is_valid = False
        if not any(char.isdigit() for char in user['password']):
            flash('Password must contain a digit.','register')
        if not any(char.isupper() for char in user['password']):
            flash('Password must contain a capitalized letter.','register')
            is_valid = False
        return is_valid
