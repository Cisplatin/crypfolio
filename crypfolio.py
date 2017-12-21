import datetime
import requests
import yaml

FILENAME = 'portfolio.yaml'
API_ROOT = 'https://api.coinmarketcap.com/v1/ticker/'
FIXER_CAD_URL = 'https://api.fixer.io/{}?base=USD'
FORMAT = ['symbol', 'amount', 'price_usd', 'total_usd', 'percent_allocation', 'percent_change_24h']

if __name__ == '__main__':
    # Open the portfolio yaml file
    with open(FILENAME, 'r') as stream:
        try:
            portfolio = yaml.load(stream)
        except yaml.YAMLError as exc:
            print exc

    # Get the USD -> CAD conversion rate
    yesterday = (datetime.date.today() - datetime.timedelta(1))
    yesterday_rate = requests.get(FIXER_CAD_URL.format(yesterday)).json()['rates']['CAD']
    exchange_rate = requests.get(FIXER_CAD_URL.format('latest')).json()['rates']['CAD']
    exchange_change = "{:.2f}".format(1 - (yesterday_rate / float(exchange_rate)))

    # Get the data from coinmarketcap
    data = [FORMAT]
    total = 0
    for crypto in portfolio:
        # Make sure the crypto exists on CMC
        if crypto == 'cad':
            info = {'symbol' : 'CAD',
                    'price_usd' : exchange_rate,
                    'percent_change_24h' : exchange_change }
        else:
            try:
                info = requests.get(API_ROOT + crypto).json()[0]
            except KeyError:
                "Cryptocurrency '%s' not found." % crypto

        # Update the total
        total += portfolio[crypto] * float(info['price_usd'])

        # Formatting so that the output looks cleaner
        info['amount'] = float("{:.2f}".format(portfolio[crypto]))
        info['total_usd'] = info['amount'] * float(info['price_usd'])
        info['total_usd'] = "${:.2f}".format(info['total_usd'])
        info['percent_change_24h'] += '%'
        info['percent_allocation'] = 0 # Can't calculate yet

        data += [map(lambda x: str(info[x]), FORMAT)]

    # Calculate percent allocation for real
    for i in xrange(1, len(data)):
        total_usd = float(data[i][FORMAT.index('total_usd')][1:])
        allocation = "{:.2f}%".format(100 * total_usd / total)
        data[i][FORMAT.index('percent_allocation')] = allocation

    # Print the data cleanly
    widths = [max([len(item) for item in col]) for col in zip(*data)]
    fmt = ''.join(['{{:{}}}'.format(width + 4) for width in widths])
    for row in data:
        print(fmt.format(*row))
    print 'Total USD: %s' % "${:.2f}".format(total)
    print 'Total CAD: %s' % "${:.2f}".format(total * exchange_rate)
