from flask import Flask,render_template,url_for,request
import sqlite3 as sql
from werkzeug.utils import redirect

conn = sql.connect('database.db')

conn.execute("CREATE TABLE IF NOT EXISTS tour(title TEXT, discribe CHAR(50), start_date, end_date, price NUMBER, distance NUMBER, travel_by TEXT)")


app = Flask(__name__, static_url_path='/static')



@app.route('/')
def home():
    return render_template("tourpage.html")


@app.route('/send',methods=["GET","POST"])
def send():
    
    if request.method == "POST":
        title = request.form.get("title")
        discribe = request.form.get("discribe")
        start_date = request.form.get("start-date")
        end_date = request.form.get("end-date")
        price = request.form.get("price")
        distance = request.form.get("distance")
        travel_by = request.form.get("travel-by")
        
        try:
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO tour (title, discribe, start_date, end_date, price, distance, travel_by) VALUES (?,?,?,?,?,?,?)",\
                    (title,discribe,start_date,end_date,price,distance,travel_by))
                
                con.commit()
                #print database content in terminal
                cur.execute("SELECT * FROM tour;")
                all_results = cur.fetchall()
                print(all_results)
        finally:
            con.close()
            
    return render_template("tourpage.html") 

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from tour")
   
   rows = cur.fetchall() 
   return render_template("list.html",rows = rows)



if __name__ == '__main__':
   app.run(debug = True)