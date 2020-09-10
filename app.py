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
        datas = c.fetchall()
        data = datas[-1]
        today = round(data[2], 4)
        pnl = round(data[3], 4)
        daily = round(data[4], 4)

        c.execute('SELECT * FROM account2')
        datas2 = c.fetchall()
        data2 = datas2[-1]
        today2 = round(data2[2], 4)
        pnl2 = round(data2[3], 4)
        daily2 = round(data2[4], 4)

        c.execute('SELECT * FROM account3')
        datas3 = c.fetchall()
        data3 = datas3[-1]
        today3 = round(data3[2], 4)
        pnl3 = round(data3[3], 4)
        daily3 = round(data3[4], 4)

        conn.commit()
        conn.close()

        return render_template('index.html', today=today, pnl=pnl, daily=daily, today2=today2, pnl2=pnl2, daily2=daily2, today3=today3, pnl3=pnl3, daily3=daily3)



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