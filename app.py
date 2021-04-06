from flask import Flask, render_template, json, request
from werkzeug.security import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

#My SQL configurations
app.config['MYSQL_DATABASE_USER'] = 'bcpython'
app.config['MYSQL_DATABASE_PASSWORD'] = 'sqs204a201'
app.config['MYSQL_DATABASE_DB'] = 'appdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')

@app.route('/signUp', methods = ['POST','GET'])	
def signUp():
	try:
		name = request.form['input_name']		
		email = request.form['input_email']
		password = request.form['input_password']

		if name and email and password:
			with closing(mysql.connect()) as conn:
				with closing(conn.cursor()) as cursor:
					hashed_password = generate_password_hash(password)
					cursor.callproc('sp_createUser', (name,email,hashed_password))
					data = cursor.fetchall()
					if len(data) == 0:
						conn.commit()
						return json.dumps({'message':'Usuário criado com sucesso!'})
					else:
						return json.dumps({'error':str(data[0])})
		else:
			return json.dumps({'html':'<span> Preencha todos os campos! </span>'})
	except Exception as e:
		return json.dumps({'error':str(e)})

if __name__ == "__main__":
	app.run(port=5002)

