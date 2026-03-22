from flask import Flask, render_template,request,redirect,url_for
import mysql.connector

app=Flask(__name__)

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="PragathiRoot2578",
    database="library"
)

cursor=db.cursor()

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        name=request.form.get('username')
        password=request.form.get('password')
        query='select * from users where username=%s and password=%s'
        cursor.execute(query,(name,password))
        data=cursor.fetchone()
        if data:
            return redirect(url_for('home',username=name))
        else:
            return render_template('login.html',error='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name=request.form.get('username')
        password=request.form.get('password')
        query='insert into users(username,password) values(%s,%s)'
        cursor.execute(query,(name,password))
        db.commit()
        return redirect(url_for('home',username=name))
    else:
        return render_template('signup.html')

@app.route('/home')
def home():
    name=request.args.get('username')
    return render_template('home.html',welcome_name=name)

if __name__=='__main__':
    app.run(debug=True)
