# crypfolio

A portfolio manager for your cryptocurrencies.

## Use

First, inside of the crypfolio directy, run:

`pip install -r requirements.txt`

Next, create a file called `portfolio.yaml` in the crypfolio directory, and formatted as such:

```
bitcoin: 0.50223008
augur: 129.89723048
monero: 189.27788475
```

There's also the special word 'cad', which can be used to include fiat total (CAD) in the total.

Then, to get budget information, use:

`python crypfolio.py`
