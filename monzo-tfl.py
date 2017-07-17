#!/usr/bin/env python3

from datetime import datetime
from dateutil import parser

from monzo.monzo import Monzo # Import Monzo Class

with open('.token') as tf:
    TOKEN = tf.read().strip()

client = Monzo(TOKEN)
account_id = client.get_first_account()['id']

def pprint_transaction(transaction):
    f = (float(transaction['amount']) / 100.0) * -1
    #date = datetime.strptime(transaction['created'], '%.%3Z')
    date = parser.parse(transaction['created']).strftime('%Y-%m-%d %H:%M:%S')
    s = '{date}\t{amount_float} {currency}\t{notes}'.format(date=date, amount_float=f, **transaction)
    print(s)

sum = 0.0
for transaction in client.get_transactions(account_id)['transactions']:
    if 'TFL' in transaction['description']:
        pprint_transaction(transaction)
        notes = transaction['notes']
        if 'Saturday' not in notes and 'Sunday' not in notes:
            sum += (float(transaction['amount']) / 100.0) * -1

print('Total: ', sum, 'GBP')
