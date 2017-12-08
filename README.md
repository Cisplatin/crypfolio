# crypfolio

A portfolio manager for your cryptocurrencies.

## Use

First, inside of the crypfolio directy, run:

`pip install -r requirements.txt`

Next, create a file called `portfolio.yaml` in the crypfolio directory, and formatted as such:

```
bitcoin: 12
monero: 100
...
<cryptocurrency_name>: <amount>
```

Then, to get budget information, use:

`python crypfolio.py`
