from flask import Flask, render_template, Response, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

@app.route("/")
def index():


    try:
        print("Checking for Todays Data")
        conn = sqlite3.connect('tracker.db')
        c = conn.cursor()
        c.execute('SELECT * FROM account1')
        data = c.fetchall()
        today = data[-1]


        total = today[2]



        return render_template('index.html', total=total, )



    except TypeError as missing_data:
        print(missing_data)
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False)


#heroku login
#cd C:\Users\oimap\Desktop\whalebotgui
#git add .
#git commit -m "note here"
#git push heroku master