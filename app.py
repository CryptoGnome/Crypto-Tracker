from flask import Flask, render_template, Response, request, redirect, url_for
import sqlite3
import datetime
from accounts import *

app = Flask(__name__)

@app.route("/")
def index():


    try:
        print("Checking for Todays Data")

        if use_account1 == True:
            conn = sqlite3.connect('tracker.db')
            c = conn.cursor()
            c.execute('SELECT * FROM account1')
            datas = c.fetchall()
            data = datas[-1]
            today = round(data[2], 4)
            pnl = round(data[3], 4)
            daily = round(data[4], 4)
            nickname1 = data[5]
        else:
            today6 = 0
            pnl6 = 0
            daily6 = 0
            nickname6 = 'EMPTY'

        if use_account2 == True:
            c.execute('SELECT * FROM account2')
            datas2 = c.fetchall()
            data2 = datas2[-1]
            today2 = round(data2[2], 4)
            pnl2 = round(data2[3], 4)
            daily2 = round(data2[4], 4)
            nickname2 = data2[5]
        else:
            today6 = 0
            pnl6 = 0
            daily6 = 0
            nickname6 = 'EMPTY'

        if use_account3 == True:
            c.execute('SELECT * FROM account3')
            datas3 = c.fetchall()
            data3 = datas3[-1]
            today3 = round(data3[2], 4)
            pnl3 = round(data3[3], 4)
            daily3 = round(data3[4], 4)
            nickname3 = data3[5]

        if use_account4 == True:
            c.execute('SELECT * FROM account4')
            datas4 = c.fetchall()
            data4 = datas4[-1]
            today4 = round(data4[2], 4)
            pnl4 = round(data4[3], 4)
            daily4 = round(data4[4], 4)
            nickname4 = data4[5]
        else:
            today6 = 0
            pnl6 = 0
            daily6 = 0
            nickname6 = 'EMPTY'

        if use_account5 == True:
            c.execute('SELECT * FROM account5')
            datas5 = c.fetchall()
            data5 = datas5[-1]
            today5 = round(data5[2], 4)
            pnl5 = round(data5[3], 4)
            daily5 = round(data5[4], 4)
            nickname5 = data5[5]
        else:
            today6 = 0
            pnl6 = 0
            daily6 = 0
            nickname6 = 'EMPTY'

        if use_account6 == True:
            c.execute('SELECT * FROM account6')
            datas6 = c.fetchall()
            data6 = datas6[-1]
            today6 = round(data6[2], 4)
            pnl6 = round(data6[3], 4)
            daily6 = round(data6[4], 4)
            nickname6 = data6[5]
        else:
            today6 = 0
            pnl6 = 0
            daily6 = 0
            nickname6 = 'EMPTY'

        conn.commit()
        conn.close()

        return render_template('index.html', today=today, pnl=pnl, daily=daily, nickname1=nickname1, today2=today2, pnl2=pnl2, daily2=daily2, nickname2=nickname2,today3=today3, pnl3=pnl3, daily3=daily3,
                               nickname3=nickname3, today4=today4, pnl4=pnl4, daily4=daily4, nickname4=nickname4, today5=today5, pnl5=pnl5, daily5=daily5, nickname5=nickname5,
                               today6=today6, pnl6=pnl6, daily6=daily6, nickname6=nickname6)



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