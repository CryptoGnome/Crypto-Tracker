import sqlite3
from accounts import *
import ccxt
import datetime
from sqlite3 import OperationalError
from time import sleep


def create(accountDB, start):
    print("DB does not Exist Yet, Creating Now")
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()
    c.execute('CREATE TABLE ' + accountDB + ' (date text, start integer, today integer, pnl integer, daily integer, nickname text)')
    conn.commit()
    c.execute('INSERT INTO ' + accountDB + '  VALUES (?, ?, ? , ?, ?, ?)',
              ('start', start, 0, 0, 0, 0))
    conn.commit()
    conn.close()

def read_db(exchange):
    print("Trying to Read DB")
    try:
        conn = sqlite3.connect('tracker.db')
        c = conn.cursor()
        c.execute('SELECT * FROM ' + exchange)
        data = c.fetchall()
        print(data)
    except sqlite3.OperationalError:
        create(exchange)
        conn.commit()
        conn.close()

def binance(accountDB, key, secret, start, nickname):
    exchange_id = 'binance'
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({
        'apiKey': key,
        'secret': secret,
        'timeout': 30000,
        'enableRateLimit': True,
        'option': {'defaultMarket': 'futures'},
        'urls': {
            'api': {
                'public': 'https://fapi.binance.com/fapi/v1',
                'private': 'https://fapi.binance.com/fapi/v1',
            }, }
    })
    #get Account Balance
    account = exchange.fapiPrivateGetAccount()
    binanceBalance = round(float(account['totalWalletBalance']), 2)
    todayCalc = datetime.date.today()
    yesterdayCalc = todayCalc - datetime.timedelta(days = 1)

    today = str(todayCalc)
    yesterday = str(yesterdayCalc)
    pnl = 0
    daily = 0

    #read Current Data in DB
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()

    #see if today already exists
    try:
        print("Checking for Todays Data")
        c.execute('SELECT * FROM ' + accountDB)
        data = c.fetchall()
        #[print(row) for row in data]

        #grab yestersterdays data

        print("Grabbing Yesterdays Data")
        c.execute('SELECT * FROM ' + accountDB + ' WHERE date = ?', (yesterday,))
        dates = c.fetchall()

        if dates:
            for data in dates:
                print("Calculating PNL $$$")
                pnl = data[2] - data[1]
                daily = pnl/data[1] * 100
                start = data[2]
        else:
            pnl = binanceBalance - start
            daily = pnl / start * 100

    except OperationalError:
        print("Error in Line")
        create(accountDB, start)
        return
    #print Exisiting Data in Table
    #[print(row) for row in data]

    print("Inserting New Values")
    #Delete Existting Data when updating
    try:
        c.execute('SELECT * FROM ' + accountDB)
        c.execute('DELETE FROM ' + accountDB + ' WHERE date = ?', (today,))
        conn.commit()
        start = data[2]
        pnl = binanceBalance - start
        daily = pnl/start * 100
        c.execute('INSERT INTO ' + accountDB + ' VALUES (?, ?, ? , ?, ?, ?)',
                  (today, start, binanceBalance, pnl, daily, nickname))

        conn.commit()
        conn.close()
    except OperationalError:
        print("Error In line 2")
        create(accountDB, start)
        return
    except IndexError:
        c.execute('SELECT * FROM ' + accountDB)
        c.execute('DELETE FROM ' + accountDB + ' WHERE date = ?', (today,))
        conn.commit()
        start = start
        pnl = binanceBalance - start
        daily = pnl/start * 100
        c.execute('INSERT INTO ' + accountDB + ' VALUES (?, ?, ? , ?, ?, ?)',
                  (today, start, binanceBalance, pnl, daily, nickname))

        conn.commit()
        conn.close()

    print("Data Added")

def bybit(accountDB, key, secret, start, nickname, asset):
    print("Checking Bybit")
    bybit = ccxt.bybit({
        'apiKey': key,
        'secret': secret,
    })

    # get Account Balance
    params = {
        'coin': asset
    }
    data = bybit.fetch_balance(params=params)
    account = data['info']['result'][asset]
    balance = round(float(account['equity']), 7)

    todayCalc = datetime.date.today()
    yesterdayCalc = todayCalc - datetime.timedelta(days=1)
    today = str(todayCalc)
    yesterday = str(yesterdayCalc)
    pnl = 0
    daily = 0

    # read Current Data in DB
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()

    # see if today already exists
    try:
        print("Checking for Todays Data")
        c.execute('SELECT * FROM ' + accountDB)
        data = c.fetchall()
        # [print(row) for row in data]

        # grab yestersterdays data

        print("Grabbing Yesterdays Data")
        c.execute('SELECT * FROM ' + accountDB + ' WHERE date = ?', (yesterday,))
        dates = c.fetchall()

        if dates:
            for data in dates:
                print("Calculating PNL $$$")
                pnl = round(data[2] - data[1], 6)
                daily = round(pnl / data[1] * 100, 6)
                start = data[2]
        else:
            pnl = round(balance - start, 6 )
            daily = round(pnl / start * 100, 6)

    except OperationalError:
        #print("Error in Line")
        create(accountDB, start)
        return
    # print Exisiting Data in Table
    # [print(row) for row in data]

    print("Inserting New Values")
    # Delete Existting Data when updating
    try:
        c.execute('SELECT * FROM ' + accountDB)
        c.execute('DELETE FROM ' + accountDB + ' WHERE date = ?', (today,))
        conn.commit()
        start = data[2]
        pnl = balance - start
        daily = pnl / start * 100
        c.execute('INSERT INTO ' + accountDB + ' VALUES (?, ?, ? , ?, ?, ?)',
                  (today, start, balance, pnl, daily, nickname))

        conn.commit()
        conn.close()
    except OperationalError:
        print("Error In line 2")
        create(accountDB, start)
        return
    except IndexError:
        c.execute('SELECT * FROM ' + accountDB)
        c.execute('DELETE FROM ' + accountDB + ' WHERE date = ?', (today,))
        conn.commit()
        start = start
        pnl = round(balance - start, 6)
        daily = round(pnl / start * 100, 6)
        c.execute('INSERT INTO ' + accountDB + ' VALUES (?, ?, ? , ?, ?, ?)',
                  (today, start, balance, pnl, daily, nickname))

        conn.commit()
        conn.close()

    print("Data Added")


def ftx(accountDB, key, secret, start, nickname):
    print("Checking FTX")
    ftx = ccxt.ftx({
        'apiKey': key,
        'secret': secret,
    })

    # get Account Balance
    account = ftx.privateGetAccount()['result']
    balance = round(float(account['collateral']), 2)

    todayCalc = datetime.date.today()
    yesterdayCalc = todayCalc - datetime.timedelta(days=1)
    today = str(todayCalc)
    yesterday = str(yesterdayCalc)
    pnl = 0
    daily = 0

    # read Current Data in DB
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()

    # see if today already exists
    try:
        print("Checking for Todays Data")
        c.execute('SELECT * FROM ' + accountDB)
        data = c.fetchall()
        # [print(row) for row in data]

        # grab yestersterdays data

        print("Grabbing Yesterdays Data")
        c.execute('SELECT * FROM ' + accountDB + ' WHERE date = ?', (yesterday,))
        dates = c.fetchall()

        if dates:
            for data in dates:
                print("Calculating PNL $$$")
                pnl = round(data[2] - data[1], 6)
                daily = round(pnl / data[1] * 100, 6)
                start = data[2]
        else:
            pnl = round(balance - start, 6)
            daily = round(pnl / start * 100, 6)

    except OperationalError:
        print("Error in Line")
        create(accountDB, start)
        return
    # print Exisiting Data in Table
    # [print(row) for row in data]

    print("Inserting New Values")
    # Delete Existting Data when updating
    try:
        c.execute('SELECT * FROM ' + accountDB)
        c.execute('DELETE FROM ' + accountDB + ' WHERE date = ?', (today,))
        conn.commit()
        start = data[2]
        pnl = balance - start
        daily = pnl / start * 100
        c.execute('INSERT INTO ' + accountDB + ' VALUES (?, ?, ? , ?, ?, ?)',
                  (today, start, balance, pnl, daily, nickname))

        conn.commit()
        conn.close()
    except OperationalError:
        print("Error In line 2")
        create(accountDB, start)
        return
    except IndexError:
        c.execute('SELECT * FROM ' + accountDB)
        c.execute('DELETE FROM ' + accountDB + ' WHERE date = ?', (today,))
        conn.commit()
        start = start
        pnl = round(balance - start, 6)
        daily = round(pnl / start * 100, 6)
        c.execute('INSERT INTO ' + accountDB + ' VALUES (?, ?, ? , ?, ?, ?)',
                  (today, start, balance, pnl, daily, nickname))

        conn.commit()
        conn.close()

    print("Data Added")


def run():

    if use_account1 == True:
        #Fetch Credentials to find Exchange & Route Data this is found in the accounts.py file
        creds = credentials['account_one']
        exchange = creds[0]
        key = creds[1]
        secret = creds[2]
        start = creds[3]
        accountDB = creds[4]
        asset = creds[5]
        nickname = creds[6]
        #Route to the correct echange to read & write data
        if exchange == 'binance':
            binance(accountDB, key, secret, start, nickname)
        if exchange == 'bybit':
            bybit(accountDB, key, secret, start, nickname, asset)
        if exchange == 'ftx':
            ftx(accountDB, key, secret, start, nickname)

    if use_account2 == True:
        # Fetch Credentials to find Exchange & Route Data this is found in the accounts.py file
        creds = credentials['account_two']
        exchange = creds[0]
        key = creds[1]
        secret = creds[2]
        start = creds[3]
        accountDB = creds[4]
        asset = creds[5]
        nickname = creds[6]
        #Route to the correct echange to read & write data
        if exchange == 'binance':
            binance(accountDB, key, secret, start, nickname)
        if exchange == 'bybit':
            bybit(accountDB, key, secret, start, nickname, asset)
        if exchange == 'ftx':
            ftx(accountDB, key, secret, start, nickname)

    if use_account3 == True:
        # Fetch Credentials to find Exchange & Route Data this is found in the accounts.py file
        creds = credentials['account_three']
        exchange = creds[0]
        key = creds[1]
        secret = creds[2]
        start = creds[3]
        accountDB = creds[4]
        asset = creds[5]
        nickname = creds[6]
        #Route to the correct echange to read & write data
        if exchange == 'binance':
            binance(accountDB, key, secret, start, nickname)
        if exchange == 'bybit':
            bybit(accountDB, key, secret, start, nickname, asset)
        if exchange == 'ftx':
            ftx(accountDB, key, secret, start, nickname)
    if use_account4 == True:
        # Fetch Credentials to find Exchange & Route Data this is found in the accounts.py file
        creds = credentials['account_four']
        exchange = creds[0]
        key = creds[1]
        secret = creds[2]
        start = creds[3]
        accountDB = creds[4]
        asset = creds[5]
        nickname = creds[6]
        #Route to the correct echange to read & write data
        if exchange == 'binance':
            binance(accountDB, key, secret, start, nickname)
        if exchange == 'bybit':
            bybit(accountDB, key, secret, start, nickname, asset)
        if exchange == 'ftx':
            ftx(accountDB, key, secret, start, nickname)

    if use_account5 == True:
        # Fetch Credentials to find Exchange & Route Data this is found in the accounts.py file
        creds = credentials['account_five']
        exchange = creds[0]
        key = creds[1]
        secret = creds[2]
        start = creds[3]
        accountDB = creds[4]
        asset = creds[5]
        nickname = creds[6]
        #Route to the correct echange to read & write data
        if exchange == 'binance':
            binance(accountDB, key, secret, start, nickname)
        if exchange == 'bybit':
            bybit(accountDB, key, secret, start, nickname, asset)
        if exchange == 'ftx':
            ftx(accountDB, key, secret, start, nickname)

    if use_account6 == True:
        # Fetch Credentials to find Exchange & Route Data this is found in the accounts.py file
        creds = credentials['account_six']
        exchange = creds[0]
        key = creds[1]
        secret = creds[2]
        start = creds[3]
        accountDB = creds[4]
        asset = creds[5]
        nickname = creds[6]
        #Route to the correct echange to read & write data
        if exchange == 'binance':
            binance(accountDB, key, secret, start, nickname)
        if exchange == 'bybit':
            bybit(accountDB, key, secret, start, nickname, asset)
        if exchange == 'ftx':
            ftx(accountDB, key, secret, start, nickname)


while True:
    run()
    print("Closing Connection...")
    sleep(60)