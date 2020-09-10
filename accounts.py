''''
To Add more accounts Duplicate account details with new number set, then add that number set to the credentials.
'''

use_account1 = True
#start balance
start1 = 1000
exchange1 = 'binance'
key1 = 'key here'
secret1 = 'secret here'

use_account2 = False
#start balance
start2 = 1000
exchange2 = 'binance'
key2 = 'key here'
secret2 = 'secret here'



credentials = {
    'account_one': [exchange1, key1, secret1, start1, 'account1'],
    'account_two': [exchange2, key2, secret2, start2, 'account2']

               }