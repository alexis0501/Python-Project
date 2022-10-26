from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
from flask_app.models.student import Student
import re 

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
#user class info
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.students = []
    
    #grab email
    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('python_project').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    #user id
    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        results = connectToMySQL('python_project').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    #save data
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) \
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s ,NOW(),NOW());"
        return connectToMySQL('python_project').query_db(query,data)
    #Get all users 
    @classmethod
    def get_all_users(cls):
        query ="SELECT * FROM users"
        results = connectToMySQL('python_project').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    #!Here we are going to have the joining of the tables  
    @classmethod
    def get_instructor_with_student(cls,data):
        query = "SELECT * FROM users LEFT JOIN students ON students.user_id = users.id WHERE users.id = %(id)s"
        results = connectToMySQL('python_project').query_db(query,data)
        print(results)
        user = cls(results[0])
        for line in results:
            data = {
                "id" : line['students.id'],
                "student_first_name" : line['student_first_name'],
                "student_last_name" : line['student_last_name'],
                "grade" : line['grade'],
                "description" : line['description'],
                "address" : line['address'],
                "email" : line['email'],
                "birthday" : line['birthday'],
                "created_at" : line['created_at'],
                "updated_at" : line['updated_at'],
            }
            user.students.append(Student(data))
        return user

    #reg valid
    @staticmethod
    def register_validation(user):
        is_valid = True
        
        if len(user['first_name']) < 2:
            flash('First name needs to be 2 characters minimum')
            is_valid = False

        if len(user['last_name']) < 2:
            flash('Last name needs to be 2 characters minimum')
            is_valid = False
        #email valid
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(user['email']):
            flash('Email Address Invalid')
            is_valid = False
        else:
            if User.get_user_by_email({'email': user['email']}):
                flash('Email Address taken')
                is_valid = False

        if len(user['password']) < 8:
                flash('Password needs to be 8 characters minimum')
                is_valid = False
        #conf email
        if user['password'] != request.form['confirm_password']:
            flash("Passwords don't match")
            is_valid = False
    
        return is_valid
    #login valid
    @staticmethod
    def login_validation(user,password):
        if not user:
            flash("Invalid login")
            return False
        if not bcrypt.check_password_hash(user.password, password):
            flash("Invalid login")
            return False

        return True 