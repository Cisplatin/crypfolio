import yaml
import requests

FILENAME = 'portfolio.yaml'
API_ROOT = 'https://api.coinmarketcap.com/v1/ticker/'
FIXER_CAD_URL = 'https://api.fixer.io/latest?base=USD'
FORMAT = ['symbol', 'amount', 'price_usd', 'total_usd', 'percent_change_24h']

if __name__ == '__main__':
    # Open the portfolio yaml file
    with open(FILENAME, 'r') as stream:
        try:
            portfolio = yaml.load(stream)
        except yaml.YAMLError as exc:
            print exc

    # Get the USD -> CAD conversion rate
    exchange_rate = requests.get(FIXER_CAD_URL).json()['rates']['CAD']

    # Get the data from coinmarketcap
    data = [FORMAT]
    total = 0

    # Check if fiat was supplied
    fiat = False
    if 'fiat' in portfolio:
        fiat = portfolio['fiat']
        del portfolio['fiat']

    for crypto in portfolio:
        try:
            info = requests.get(API_ROOT + crypto).json()[0]
        except KeyError:
            "Cryptocurrency '%s' not found." % crypto

        # Update the total
        total += portfolio[crypto] * float(info['price_usd'])

        # Formatting so that the output looks cleaner
        info['amount'] = portfolio[crypto]
        info['total_usd'] = info['amount'] * float(info['price_usd'])
        info['total_usd'] = "${:.2f}".format(info['total_usd'])
        info['percent_change_24h'] += '%'

        data += [map(lambda x: str(info[x]), FORMAT)]

    if fiat:
        data += [map(str, ['Fiat', fiat, exchange_rate, "${:.2f}".format(fiat / exchange_rate), 'N/A'])]

    usd_total = total
    cad_total = total * exchange_rate
    total = total * exchange_rate + fiat

    # Print the data cleanly
    widths = [max([len(item) for item in col]) for col in zip(*data)]
    fmt = ''.join(['{{:{}}}'.format(width + 4) for width in widths])
    for row in data:
        print(fmt.format(*row))
    print 'Total USD: %s' % "${:.2f}".format(usd_total)
    print 'Total CAD: %s' % "${:.2f}".format(cad_total)
    print 'Total CAD (with  fiat): %s' % "${:.2f}".format(total)
