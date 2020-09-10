''''
To Add more accounts Duplicate account details with new number set, then add that number set to the credentials.
'''

use_account1 = True
#start balance
start1 = 1000
asset1 = 'USD'
exchange1 = 'binance'
key1 = 'key here'
secret1 = 'secret here'

use_account2 = False
#start balance
start2 = 1000
asset2 = 'USD'
exchange2 = 'binance'
key2 = 'key here'
secret2 = 'secret here'

use_account3 = False
start3 = 8994.48
asset3 = 'USD'
exchange3 = 'binance'
key3 = 'key here'
secret3 = 'secret here'

use_account4 = False
start4 = 0.12411724
asset4 = 'BTC'
exchange4 = 'bybit'
key4 = 'key here'
secret4 = 'secret here'

use_account5 = False
start5 = 409.57
asset5 = 'USD'
exchange5 = 'ftx'
key5 = 'key here'
secret5 = 'secret here'

credentials = {
    'account_one': [exchange1, key1, secret1, start1, 'account1', asset1],
    'account_two': [exchange2, key2, secret2, start2, 'account2', asset2],
    'account_three': [exchange3, key3, secret3, start3, 'account3', asset3],
    'account_four': [exchange4, key4, secret4, start4, 'account4', asset4],
    'account_five': [exchange5, key5, secret5, start5, 'account5', asset5]

               }