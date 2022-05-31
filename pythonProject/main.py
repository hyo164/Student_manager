from app import app
from config import mysql
from flask import jsonify, request, make_response, redirect, url_for, session, Flask, flash
import pandas as pd
import io
import pymysql
from passlib.hash import sha256_crypt
from functools import wraps



def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Please Login :)', 'danger')
			return redirect(url_for('login'))
	return wrap

def is_student(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['prof'] == 1:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized. Student only', 'danger')
			return redirect(url_for('login'))
	return wrap

def is_teacher(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['prof'] == 2:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized. Teacher only', 'danger')
			return redirect(url_for('login'))
	return wrap

def is_admin(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['prof'] == 3:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized. Admin only', 'danger')
			return redirect(url_for('login'))
	return wrap


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_user = request.form['password']

        cursor = mysql.connect().cursor(pymysql.cursors.DictCursor)

        query = 'SELECT * FROM user WHERE username = %s'
        result = cursor.execute(query,[username])
        if result>0:
            data = cursor.fetchone()
            password = sha256_crypt.hash(data['password'])
            if sha256_crypt.verify(password_user, password):
                session['logged_in'] = True
                session['username'] = username
                session['prof'] = data['prof']
                flash('You are logged in', 'success')
                if session['prof'] == 1:
                    return redirect(url_for('query_score_student',username=username))
                if session['prof'] == 2:
                    return redirect(url_for('query_class'))
                if session['prof'] == 3:
                    return redirect(url_for('query_user'))
            else:
                error = 'Invalid login'
                return error

            cursor.close()
        else:
            error = 'Username NOT FOUND'
            return error

    elif request.method == 'GET':
        return 'please login'


@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))


@app.route('/')
def main_page():
    return jsonify('Main page')


#view cho GV - class
@app.route('/class', methods=['GET'])
@is_logged_in
@is_teacher
def query_class():
    try:
        param = request.args.get('class_id')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if bool(param):
            cursor.execute("SELECT s.class_id, s.student_id, s.student_name, s.email, s.gender \
            FROM class c JOIN student s ON c.class_id = s.class_id where s.class_id = '%s'"%(param))
            rows = cursor.fetchall()
            respone = jsonify(rows)
            respone.status_code = 200
            return respone
        else:
            cursor.execute("SELECT * FROM class")
            rows = cursor.fetchall()
            respone = jsonify(rows)
            respone.status_code = 200
            return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/class/add', methods=['POST'])
@is_logged_in
@is_teacher
def add_class():
    try:
        class_id = request.form.get('class_id')
        class_name = request.form.get('class_name')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlCheck = "SELECT * FROM class WHERE class_id = '%s'" % (class_id)
        if bool(cursor.execute(sqlCheck)):
            return "class_id duplicated, fail to add"
        else:
            sqlQuery = "INSERT INTO class (class_id, class_name) VALUES(%s, %s)"
            bindData = (class_id, class_name)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('added successfully!')
            respone.status_code = 200
            print(respone)
            return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/class/update', methods=['PUT'])
@is_logged_in
@is_teacher
def update_class():
    try:
        class_id = request.form.get('class_id')
        class_name = request.form.get('class_name')

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlCheck = "SELECT * FROM class WHERE class_id = '%s'" % (class_id)
        if bool(cursor.execute(sqlCheck)):
            sqlQuery = "UPDATE class SET class_name='%s' WHERE class_id='%s'"%(class_name,class_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            conn.commit()
            respone = jsonify('updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return "class id %s not exist"%(class_id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/class/delete', methods=['DELETE'])
@is_logged_in
@is_teacher
def delete_class():
    try:
        class_id = request.args.get('class_id')
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM class WHERE class_id =%s", (class_id))
        conn.commit()
        respone = jsonify(("deleted class id %s successfully!") %(class_id))
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#view cho GV - subject
@app.route('/subject', methods=['GET'])
@is_logged_in
@is_teacher
def query_subject():
    try:
        param = request.args.get('subject_name')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if bool(param):
            cursor.execute("SELECT sc.student_id, s.subject_name, s.subject_id, sc.score \
            FROM score sc JOIN subject s ON sc.subject_id = s.subject_id  where s.subject_name = '%s'"%(param))
            rows = cursor.fetchall()
            respone = jsonify(rows)
            respone.status_code = 200
            return respone
        else:
            cursor.execute("SELECT * FROM subject")
            rows = cursor.fetchall()
            respone = jsonify(rows)
            respone.status_code = 200
            return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/subject/add', methods=['POST'])
@is_logged_in
@is_teacher
def add_subject():
    try:
        subject_id = request.form.get('subject_id')
        subject_name = request.form.get('subject_name')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlCheck = "SELECT * FROM subject WHERE subject_id = '%s'" % (subject_id)
        if bool(cursor.execute(sqlCheck)):
            return "subject_id duplicated, fail to add"
        else:
            sqlQuery = "INSERT INTO subject (subject_id, subject_name) VALUES(%s, %s)"
            bindData = (subject_id, subject_name)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('added successfully!')
            respone.status_code = 200
            print(respone)
            return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/subject/update', methods=['PUT'])
@is_logged_in
@is_teacher
def update_subject():
    try:
        subject_id = request.form.get('subject_id')
        subject_name = request.form.get('subject_name')

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlCheck = "SELECT * FROM subject WHERE subject_id = '%s'" % (subject_id)
        if bool(cursor.execute(sqlCheck)):
            sqlQuery = "UPDATE subject SET subject_name='%s' WHERE subject_id = '%s'" %(subject_name, subject_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            conn.commit()
            respone = jsonify('updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return "subject id %s not exist"%(subject_id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/subject/delete', methods=['DELETE'])
@is_logged_in
@is_teacher
def delete_subject():
    try:
        subject_id = request.args.get('subject_id')
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subject WHERE subject_id =%s", (subject_id))
        conn.commit()
        respone = jsonify(("deleted subject id %s successfully!") %(subject_id))
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#view cho GV - score
@app.route('/score', methods=['GET'])
@is_logged_in
@is_teacher
def query_score():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM score")
        rows = cursor.fetchall()
        respone = jsonify(rows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/score/add', methods=['POST'])
@is_logged_in
@is_teacher
def add_score():
    try:
        student_id = request.form.get('student_id')
        subject_name = request.form.get('subject_name')
        subject_id = request.form.get('subject_id')
        score = request.form.get('score')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlCheck = "SELECT * FROM score WHERE student_id = '%s' and subject_id = '%s'" % (student_id, subject_id)
        if bool(cursor.execute(sqlCheck)):
            return "score existed, fail to add"
        else:
            sqlQuery = "INSERT INTO score (student_id, subject_name, subject_id, score) VALUES(%s, %s, %s, %s)"
            bindData = (student_id, subject_name, subject_id, score)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('added successfully!')
            respone.status_code = 200
            print(respone)
            return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/score/update', methods=['PUT'])
@is_logged_in
@is_teacher
def update_score():
    try:
        student_id = request.form.get('student_id')
        subject_id = request.form.get('subject_id')
        score = request.form.get('score')

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlCheck = "SELECT * FROM score WHERE student_id = '%s' and subject_id = '%s'" % (student_id, subject_id)
        if bool(cursor.execute(sqlCheck)):
            sqlQuery = "UPDATE score SET score='%s' WHERE student_id = '%s' and subject_id = '%s'" %(score, student_id, subject_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            conn.commit()
            respone = jsonify('updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return "subject id %s not exist"%(subject_id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/score/delete', methods=['DELETE'])
@is_logged_in
@is_teacher
def delete_score():
    try:
        id = request.args.get('id')
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM score WHERE id =%s", (id))
        conn.commit()
        respone = jsonify(("deleted successfully!"))
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#view cho SV - score
@app.route('/score/<username>', methods=['GET'])
@is_logged_in
@is_student
def query_score_student(username):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT t.student_name, t.username, s.subject_name, s.subject_id, s.score FROM score s join student t "
                       "on s.student_id = t.student_id WHERE username = '%s'" %session['username'])
        rows = cursor.fetchall()
        respone = jsonify(rows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/score/download', methods=['GET'])
@is_logged_in
@is_student
def download_score_student():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT t.student_name, t.username, s.subject_name, s.subject_id, s.score FROM score s join student t "
                       "on s.student_id = t.student_id WHERE username = '%s'" % session['username'])
        rows = cursor.fetchall()
        df =pd.DataFrame(rows, columns=['student_name', 'username', 'subject_name', 'subject_id', 'score'])
        df.index = df.index + 1

        execel_file = io.StringIO()
        filename = "%s.csv" % ('score_detail')
        df.to_csv(execel_file, encoding='utf-8')
        csv_output = execel_file.getvalue()
        execel_file.close()
        resp = make_response(csv_output)
        resp.headers["Content-Disposition"] = ("attachment; filename=%s" % filename)
        resp.headers["Content-Type"] = "text/csv"
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# view cho ad
@app.route('/user', methods=['GET'])
@is_logged_in
@is_admin
def query_user():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM user")
        rows = cursor.fetchall()
        respone = jsonify(rows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/user/add', methods=['POST'])
@is_logged_in
@is_admin
def add_user():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        prof = request.form.get('prof')
        student_id = request.form.get('student_id')
        email = request.form.get('email')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlCheck = "SELECT * FROM user WHERE username = '%s'" % (username)
        if bool(cursor.execute(sqlCheck)):
            return "username duplicated, fail to add"
        else:
            sqlQuery = "INSERT INTO user (username, password, name, prof, student_id, email) VALUES(%s, %s, %s, %s, %s, %s)"
            bindData = (username, password, name, prof, student_id, email)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('added successfully!')
            respone.status_code = 200
            print(respone)
            return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/user/update', methods=['PUT'])
@is_logged_in
@is_admin
def update_user():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        prof = request.form.get('prof')
        student_id = request.form.get('student_id')
        email = request.form.get('email')

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlCheck = "SELECT * FROM user WHERE username = '%s'" % (username)
        if bool(cursor.execute(sqlCheck)):
            sqlQuery = "UPDATE user SET password='%s', name='%s', prof='%s', student_id='%s', email='%s' WHERE username='%s'" %(password, name, prof,student_id, email, username)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            conn.commit()
            respone = jsonify('updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return "username %s not exist"%(username)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/user/delete', methods=['DELETE'])
@is_logged_in
@is_admin
def delete_user():
    try:
        username = request.args.get('username')
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user WHERE username =%s", (username))
        conn.commit()
        respone = jsonify(("deleted successfully!"))
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()




@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    app.secret_key = '1se3z34@'
    app.run(port=5000,debug=False)
