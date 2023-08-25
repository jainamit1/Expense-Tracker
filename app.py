from flask import Flask, render_template, request, session, flash, url_for, redirect
from Forms import LoginForm, RegistrationForm, IncomeForm, ExpenseForm
import mysql.connector
from flask_bootstrap import Bootstrap
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
Bootstrap(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dD23012002@'
app.config['MYSQL_DB'] = 'tracker_db'
app.config['SECRET_KEY']='xyz'



@app.route('/',methods=['GET','POST'])
def home():
	loginform = LoginForm(request.form)
	regform = RegistrationForm(request.form)
	if session.get('loggedin') is None:
		if request.method=='POST' :
			details = request.form.to_dict()
			print(details)
			name = details['name']
			email = details['email']
			phone = details['phone']
			pwd = details['password']
			if len(pwd)<8:
				flash('Password Should Have Minimum 8 characters','message')
				return redirect(url_for('home'))
			hashed_pwd = pbkdf2_sha256.hash(pwd)

			mydb = mysql.connector.connect(host='localhost',user='root',password='dD23012002@',database='tracker_db')
			mycursor =  mydb.cursor()
			sql = 'SELECT * from users where email = %s'
			mycursor.execute(sql,(email,))
			account = mycursor.fetchone()
			if account is not None:
				flash('The email id is already registered','message')
				return redirect(url_for('home'))
			else:
				mycursor.execute('insert into users (username, email, phone, pwd) values (%s,%s,%s,%s);',(name, email, phone, hashed_pwd))
				mydb.commit()
				mycursor.close()
				flash('Registered Successfully','message')
				return redirect(url_for('home'))
		
		return render_template('forms.html',loginform=loginform,regform=regform)
	else:
		return redirect(url_for('dashboard'))


	
@app.route('/login',methods=['POST'])
def login():
	print(session)
	if session.get('loggedin') is None:
		if request.method=='POST':
			details = request.form.to_dict()
			email = details['email']
			pwd = details['password']
			mydb = mysql.connector.connect(host='localhost',user='root',password='dD23012002@',database='tracker_db')
			mycursor =  mydb.cursor()
			sql = 'SELECT * FROM users Where email = %s'
			mycursor.execute(sql,(email,))
			account = mycursor.fetchone()
			if account is not None:
				if pbkdf2_sha256.verify(pwd, account[4]):
					session['loggedin']= True
					session['user_id'] = account[0]
					print(session)
					return redirect(url_for('dashboard'))
				else:
					flash('Incorrect password','message')
					return redirect(url_for('home'))
			elif account is None:
				flash('User Not Registered','message')
				return redirect(url_for('home'))
	else:
		flash('already logged in','flash')
		return redirect(url_for('dashboard'))

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
	if session.get('loggedin') is not None:
		income_form = IncomeForm(request.form)
		expense_form = ExpenseForm(request.form)

		mydb = mysql.connector.connect(host='localhost',user='root',password='dD23012002@',database='tracker_db')
		mycursor =  mydb.cursor()
		sql = 'SELECT * from tracker where id=%s'
		mycursor.execute(sql,(session['user_id'],))
		details = mycursor.fetchall()
		if details:
			expense_sum = 0
			income_sum = 0
			for each in details:
				if each[3] == 'Expense':
					expense_sum+=float(each[2])
				elif each[3] =='Income':
					income_sum+=float(each[2])
			if income_sum-expense_sum>0:
				message='You are at surplus of ₹{} '.format(income_sum-expense_sum)
			elif income_sum-expense_sum<0:
				message='You are at deficit of ₹{} '.format(income_sum-expense_sum)
			else:
				message = 'You are neither at deficit nor surplus!'
			return render_template('dashboard.html',income_form=income_form,expense_form=expense_form,data=details,message=message)
		else:
			return render_template('dashboard.html',income_form=income_form,expense_form=expense_form,data=None)
	else:
		flash('Your Session Expired','message')
		return redirect(url_for('home'))	
	
@app.route('/income',methods=['GET','POST'])
def income():
	if session.get('loggedin') is not None:
		income_form = IncomeForm(request.form)
		if request.method=='POST':
			details = request.form.to_dict()
			income_src = details['income_src']
			income_amt = details['income_amt']
			try :
				income_amt = float(income_amt)
				if income_amt < 0:
					flash('Income Amount cannot be negative','msg')
					return redirect(url_for('dashboard'))
			except ValueError:
				flash('Amount should be in numbers only','msg')
				return redirect(url_for('dashboard'))
			mydb = mysql.connector.connect(host='localhost',user='root',password='dD23012002@',database='tracker_db')
			mycursor =  mydb.cursor()
			sql = 'insert into tracker values (%s, %s, %s, %s);'
			mycursor.execute(sql,(session['user_id'],income_src,income_amt,'Income'))
			mydb.commit()
			return redirect(url_for('dashboard'))
	else:
		flash('Your Session Expired','message')
		return redirect(url_for('home'))

@app.route('/expense',methods=['GET','POST'])
def expense():
	if session.get('loggedin') is not None:
		expense_form = ExpenseForm(request.form)
		if request.method=='POST':
			details = request.form.to_dict()
			expense_src = details['expense_src']
			expense_amt = details['expense_amt']
			try:
				expense_amt = float(expense_amt)
				if expense_amt <0:
					flash('Expense Amount cannot be negative','msg')
					return redirect(url_for('dashboard'))
			except ValueError:
				flash('Amount should be in numbers only','msg')
				return redirect(url_for('dashboard'))
			mydb = mysql.connector.connect(host='localhost',user='root',password='dD23012002@',database='tracker_db')
			mycursor =  mydb.cursor()
			sql = 'insert into tracker values (%s, %s, %s, %s);'
			mycursor.execute(sql,(session['user_id'],expense_src,expense_amt,'Expense'))
			mydb.commit()
			return redirect(url_for('dashboard'))

	else:
		flash('Your Session Expired','message')
		return redirect(url_for('home'))

@app.route('/logout', methods=['POST'])
def logout():
	if session.get('loggedin') is not None:
		session.pop('user_id',None)
		session.pop('loggedin',None)
		return redirect(url_for('home'))
	else:
		flash('Session Expired Login Again', 'message')
		return redirect(url_for('home'))
if __name__ == '__main__':
	app.run()