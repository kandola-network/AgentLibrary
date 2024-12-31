import requests

def call_fetch_token_pair_price(token1, token2):
    """
    Fetch token pair price
    :param token1: token symbol (e.g. BTC, ETH, etc.)
    :param token2: token symbol (e.g. BTC, ETH, etc.)
    """
    base_url = "http://localhost:8000"
    url = f"{base_url}/api/tokens/{token1}{token2}/price"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Token Pair Price API Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error calling fetch_token_pair_price API:", e)

def call_compare_token_pair_prices(token1_pair1, token2_pair1, token1_pair2, token2_pair2):
    """
    Compare token pair prices
    :param base_url: base URL for the API
    :param token1_pair1: token symbol (e.g. BTC, ETH, etc.)
    :param token2_pair1: token symbol (e.g. BTC, ETH, etc.)
    :param token1_pair2: token symbol (e.g. BTC, ETH, etc.)
    :param token2_pair2: token symbol (e.g. BTC, ETH, etc.)
    """
    base_url = "http://localhost:8000"
    url = f"{base_url}/api/tokens/{token1_pair1}{token2_pair1}{token1_pair2}{token2_pair2}/compare"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Compare Token Pair Prices API Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error calling compare_token_pair_prices API:", e)

def call_fetch_historical_price_data(token, time_period="7d"):
    """
    Fetch historical price data for a token
    :param token: token symbol (e.g. BTC, ETH, etc.)
    :param time_period: time period for historical data (e.g. 1d, 7d, 30d, 90d, 180d, 365d)
    """
    base_url = "http://localhost:8000"
    url = f"{base_url}/api/tokens/{token}/history/{time_period}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Historical Price Data API Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error calling fetch_historical_price_data API:", e)


user_tools = [call_fetch_token_pair_price, call_compare_token_pair_prices, call_fetch_historical_price_data]