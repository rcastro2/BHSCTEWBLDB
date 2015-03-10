import os, cteDAO
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, g, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

@app.before_request
def before_request():
	con = MongoClient(os.environ.get('DATABASE_URL'))
	g.db = con.bhsbox
	g.cte = cteDAO.cteDAO(g.db)

@app.route('/')
@app.route('/index')
def index():
	return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == "POST":
		u = request.form['u']
		p = request.form['p']
		data = g.db.users.find_one({'user':u})
		if data != None and check_password_hash(data['pwd'], p):
			session["user"] = u
			print "Access Granted"
			return "Access Granted"
		else:
			session["user"] = None
			return render_template('login.html')
	else:
		return render_template('login.html')

@app.route('/logout')
def logout():
	session['user'] = None
	return redirect(url_for('index'))

@app.route('/wbl/<option>',methods=['GET','POST'])
def wbl(option):
	if session["user"] == None:
		return redirect(url_for('index'))
	if option == 'display':
		data = g.cte.get_wbl()
		return render_template('wbl.html',activities = data)
	elif option == 'upsert' and request.method == "POST":
		g.cte.upsert_wbl(request.form)
		return redirect(request.referrer)
	elif option == 'remove' and request.method == "POST":
		g.cte.remove_wbl(request.form['title'])
		return redirect(request.referrer)
	else:
		return redirect(request.referrer)

@app.route('/students/<option>',methods=['GET','POST'])
def students(option):
	if session["user"] == None:
		return redirect(url_for('index'))
	if option == 'display' and request.method == 'GET':
		data = g.cte.get_students()
		return render_template('students.html',students = data)
	elif option == 'studentID' and request.method == 'POST':
		data = g.cte.get_students(request.form['studentID'])
		return render_template('students.html',students = data)
	elif option == 'wblTitle' and request.method == 'POST':
		data = g.cte.get_students(wbl=request.form['wblTitle'])
		return render_template('students.html',students = data)
	else:
		return redirect(request.referrer)

if __name__ == '__main__':
	app.debug = True
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
