from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
from flask_app.models import user

class Student:
    def __init__(self,data):
        self.id = data['id']
        self.student_first_name = data['student_first_name']
        self.student_last_name = data['student_last_name']
        self.grade = data['grade']
        self.description = data['description']
        self.address = data['address']
        self.email = data['email']
        self.birthday = data['birthday']

    #! Functions create
    @classmethod
    def create_student(cls, data):
        query = "INSERT INTO students (user_id, student_first_name, student_last_name, grade, description, address, email, birthday)\
        VALUES (%(user_id)s,%(student_first_name)s,%(student_last_name)s,%(grade)s,%(description)s,%(address)s,%(email)s,%(birthday)s)"
        return connectToMySQL('python_project').query_db(query, data)

    #! Functions Get all
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM students"
        results = connectToMySQL('python_project').query_db(query)
        students = []
        for student in results:
            students.append(cls(student))
        return students
    
    #! Functions delete
    @classmethod
    def delete_a_student(cls, data):
        query = "DELETE FROM students WHERE id = %(student_id)s;"
        results = connectToMySQL('python_project').query_db(query,data)
        return
    
    #! Functions edit
    @classmethod
    def update_student_info(cls,data):
        query = "UPDATE students SET student_first_name = %(student_first_name)s, student_last_name = %(student_last_name)s, grade = %(grade)s, description = %(description)s, address = %(address)s, email = %(email)s, birthday = %(birthday)s WHERE id = %(student_id)s;"
        results = connectToMySQL('python_project').query_db(query, data)
        return

    #! Functions get by id
    @classmethod
    def get_student_by_id(cls,data):
        query = "SELECT * FROM students WHERE students.id = %(student_id)s;"
        results = connectToMySQL('python_project').query_db(query,data)
        student = cls(results[0])
        return student

    #! Validations
    @staticmethod
    def validate_student(data):
        is_valid = True

        if len(data['student_first_name']) < 3:
            flash('Name must be greater than 3 characters')
            is_valid= False
        if len(data['student_last_name']) < 2:
            flash('Last Name must be greater than 2 characters')
            is_valid= False
        if len(data['grade']) <= 1:
            flash('Grade must be at least 1')
            is_valid= False
        if len(data['description']) < 2:
            flash('Description must be greater than 2 characters characters')
            is_valid= False
        if len(data['address']) < 2:
            flash('Address must be greater than 2 characters characters')
            is_valid= False
        if len(data['email']) < 2:
            flash('Email must be greater than 2 characters characters')
            is_valid= False
        if len(data['birthday']) < 2:
            flash('Birthday must be greater than 2 characters characters')
            is_valid= False

        return is_valid