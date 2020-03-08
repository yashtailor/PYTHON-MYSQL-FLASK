from flask import Flask,render_template,redirect,request
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'	
app.config['MYSQL_PASSWORD'] = 'root@mysql'
app.config['MYSQL_DB']	= 'crud_init_flask'

mysql = MySQL(app)

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="root@mysql"
# )

@app.route('/')
def index():
    data = []
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users;')
        data = cur.fetchall()
        cur.close()
    finally:
        return render_template('index.html',data = data,index=1)

@app.route('/insert',methods=['POST'])
def insert():
    name = request.form['name']
    email = request.form['email']
    print(name,email)
    try:
        cur = mysql.connection.cursor()
        cur.execute('CREATE TABLE users(id int PRIMARY KEY AUTO_INCREMENT,name varchar(200), email varchar(200));')
        cur.commit()
    finally:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users(name,email) VALUES(%s,%s);',(name,email))
        mysql.connection.commit()
        return redirect('/')

@app.route('/sort',methods=['POST'])
def sort():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users ORDER BY(name) ASC;')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html',data=data,index=1)

@app.route('/findEmail',methods=['POST'])
def findEmail():
    try:
        cur = mysql.connection.cursor()
        name = request.form['name']
        string = "SELECT * FROM users WHERE name = '"+name+"'"
        # string = "SELECT * FROM users WHERE name = %s"
        cur.execute(string)
        email = cur.fetchall()
        print(email)
        return render_template('index.html',data=email,index=2)
    except:
        return render_template('index.html',data=[],index=2)

@app.route('/searchSubstring',methods=['POST'])
def searchSubstring():
    try:
        cur = mysql.connection.cursor()
        name = request.form['name']
        cur.execute("SELECT * FROM users WHERE name LIKE '%"+name+"%'")
        names = cur.fetchall()
        cur.close()
        return render_template('index.html',data=names,index=1)
    except:
        return render_template('index.html',data=[],index=2)

@app.route('/reset',methods=['POST'])
def reset():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)