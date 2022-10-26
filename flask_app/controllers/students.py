from flask_app import app
from flask import render_template, flash, redirect, request, session 
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.student import Student

#* Takes you to the create page for a student
@app.route('/student/new')
def student_navigate():
    if 'user' not in session:
        return redirect('/')
        flash("Please Login")
    return render_template('studentCreate.html', user = User.get_user_by_id({'id':session['user']}))

#*Create route that goes to models file to create a student
@app.route('/create_student', methods=["POST"])
def create():
    if not Student.validate_student(request.form):
        return redirect('/student/new')
    data = {
        'student_first_name': request.form['student_first_name'],
        'student_last_name' : request.form['student_last_name'],
        'grade': request.form['grade'],
        'description': request.form['description'],
        'address': request.form['address'],
        'email': request.form['email'],
        'birthday': request.form['birthday'],
        'user_id': session['user'],
    } 
    Student.create_student(data)  
    return redirect('/home')

#*Shows one student !whichever student is clicked!
@app.route('/student/<int:student_id>')
def show_student_info_navigate(student_id):
    data = {
        "student_id" : student_id
    }
    student = Student.get_student_by_id(data)
    return render_template('studentShow.html', student = student, user = User.get_user_by_id({'id':session['user']}))

#*Edit a student
@app.route("/student/<int:student_id>/edit")
def edit_student_navigate(student_id):
    if 'user' not in session:
        return redirect('/')
        flash("Please Login")

    data = {
        "student_id" : student_id
    }
    student = Student.get_student_by_id(data)
    return render_template("studentEdit.html", student= student, user = User.get_user_by_id({'id':session['user']}))

@app.route("/student/<int:student_id>/update", methods=["POST"])
def update_a_student(student_id):
    data = {
        "student_first_name" : request.form["student_first_name"],
        "student_last_name" : request.form["student_last_name"],
        "grade" : request.form["grade"],
        "description" : request.form["description"],
        "address" : request.form["address"],
        "email" : request.form["email"],
        "birthday" : request.form["birthday"],
        "student_id" : student_id
    }

    if not Student.validate_student(data):
        return redirect(f"/student/{student_id}/edit")

    Student.update_student_info(data)

    return redirect("/home")

@app.route("/student/<int:student_id>/delete")
def delete_student(student_id):
    
    data = {
        "student_id" : student_id
    }
    Student.delete_a_student(data)
    
    return redirect('/home ')

@app.route("/student/grade")
def grade():
    if 'user' not in session:
        return redirect('/')
        flash("Please Login")
    return render_template('gradeScale.html', user = User.get_user_by_id({'id':session['user']}))