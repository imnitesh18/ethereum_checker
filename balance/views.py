from django.shortcuts import render
from eth_utils import is_checksum_address, to_checksum_address
from web3 import Web3
import requests


def home(request):
    return render(request, 'index.html')


def fetch_balance(request):
    if request.method == 'POST':
        ethereum_address = request.POST['ethereum_address']

        # Normalize the address to checksum format
        normalized_address = to_checksum_address(ethereum_address)

        # Connect to the Ethereum network using Web3
        web3 = Web3(Web3.HTTPProvider(
            'https://mainnet.infura.io/v3/57a0bbe72ea74a20982fb7857b26a54c'))

        try:
            # Check if the normalized address is valid
            if not is_checksum_address(normalized_address):
                error_message = "Invalid Ethereum address"
                context = {
                    'error': error_message
                }
                return render(request, 'index.html', context)

            # Fetch the balance
            balance = web3.eth.get_balance(normalized_address)

            # Convert the balance from Wei to Ether
            balance_in_ether = web3.from_wei(balance, 'ether')

            # Fetch the current conversion rate from an API or a service
            conversion_rate_usd = fetch_conversion_rate('usd')
            conversion_rate_inr = fetch_conversion_rate('inr')

            # Calculate the balance in USD and INR
            balance_in_usd = float(balance_in_ether) * conversion_rate_usd
            balance_in_inr = float(balance_in_ether) * conversion_rate_inr

            # Fetch the recent 5 transactions
            transactions = fetch_recent_transactions(
                normalized_address, 5, web3)

            context = {
                'balance': balance_in_ether,
                'balance_usd': balance_in_usd,
                'balance_inr': balance_in_inr,
                'ethereum_address': normalized_address,
                'transactions': transactions
            }

            return render(request, 'index.html', context)

        except Exception as e:
            error_message = str(e)
            context = {
                'error': error_message
            }

            return render(request, 'index.html', context)


def fetch_conversion_rate(currency):
    # Fetch the current conversion rate from an API or a service
    response = requests.get(
        f'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies={currency}')
    conversion_rate = response.json()['ethereum'][currency]
    return conversion_rate


def fetch_recent_transactions(address, count, web3):
    # Fetch the recent transactions
    # replace with your Etherscan API key
    api_key = 'K81TTXIW6ZKPHX6XEW7T2989ITVGT37P5F'
    url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset={count}&sort=desc&apikey={api_key}'
    response = requests.get(url)
    transactions = response.json()['result']

    # Convert the transaction values from Wei to Ether
    for transaction in transactions:
        transaction['value'] = web3.from_wei(
            int(transaction['value']), 'ether')

    return transactions
