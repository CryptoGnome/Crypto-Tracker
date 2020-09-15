## Crypto-Tracker
Simple Bot to Track Balances using Python, SQLite, &amp; Flask


![IMAGE ALT TEXT HERE](https://i.imgur.com/Cx9WaJ7.png)


# SETUP GUIDE

## Install Python: 

https://www.python.org/downloads/

## Clone or Download Zip File Below:

https://github.com/CryptoGnome/Crypto-Tracker/archive/master.zip

## Install Requirements via Windows Command Prompt:

```pip install -r requirements.txt```


## Edit Accounts to match Exchanges & Keys using a text editor

```accounts.py```

## Run Main.py

## Run App.py & Visit http://localhost:8000/ to view UI

To view from outside source you mus edit the app.py file to match your public ip & set a custom port usign the code below, you then must open the port to outside traffic.

```if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081)```
