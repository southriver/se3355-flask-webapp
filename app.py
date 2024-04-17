import sqlite3 as sql
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

def initDB():
    conn = sql.connect('database.db')
    print( "Opened database successfully")   
    
    conn.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, addr TEXT, city TEXT, pin TEXT)')
    print ("Table created successfully")
    conn.close()

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall();
   return render_template("list.html", rows=rows)

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()   

@app.route('/delrec/<id>',methods = ['GET'])
def delrec(id):
   if request.method == 'GET':
      try:

         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM students WHERE Id = ?",(id) )
            
            con.commit()
            msg = "Record successfully deleted"
      except:
         con.rollback()
         msg = "error in deleted operation"
      
      finally:
         return redirect(url_for('list'))
         con.close()  

# @app.route('/')
# def index():
#     return 'Hello, World!'

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/result',methods = ['POST'])
# def result():
#     age  = int(request.form['age'])
#     city = request.form['city']
#     status = 'Old'
#     if age < 20:
#         status = 'Young'
#     return render_template("result.html",status=status)
            

if __name__ == '__main__':
   # initDB()
   app.run(debug=True)