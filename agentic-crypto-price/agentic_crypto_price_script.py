import requests

# API Configuration
API_HOST = "coinranking1.p.rapidapi.com"
API_KEY = "2aa2dc640bmshecc6af18f5a160ep1e79c5jsn095d25a21855"
BASE_URL = f"https://{API_HOST}"
HEADERS = {
    "x-rapidapi-host": API_HOST,
    "x-rapidapi-key": API_KEY
}

def _fetch_data(endpoint):
    """Helper function to fetch data from API"""
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["data"]

def _get_coin_uuid(symbol):
    """Helper function to get coin UUID"""
    coins = _fetch_data("coins?referenceCurrencyUuid=yhjMzLPhuIDl&limit=50")
    for coin in coins["coins"]:
        if coin["symbol"] == symbol:
            return coin["uuid"]
    return None

def fetch_token_pair_price(token_pair):
    """
    Fetch the current price for a token pair
    Example: BTC/USDT
    """
    command = f"Command: What is the latest price for {token_pair}?"
    
    base, quote = token_pair.split('/')
    base_uuid = _get_coin_uuid(base)
    quote_uuid = _get_coin_uuid(quote)
    
    if not base_uuid or not quote_uuid:
        return f"{command}\nResponse: One or both tokens in the pair {token_pair} are not available."
        
    base_price = float(_fetch_data(f"coin/{base_uuid}/price")["price"])
    quote_price = float(_fetch_data(f"coin/{quote_uuid}/price")["price"])
    
    pair_price = base_price / quote_price
    return f"{command}\nResponse: The current price for {token_pair} is ${pair_price:,.2f}."

def compare_token_pair_prices(pair1, pair2):
    """
    Compare prices of two token pairs
    Example: BTC/USDT vs ETH/USDT
    """
    command = f"Command: How does the price of {pair1} compare to {pair2}?"
    
    # Get first pair price
    base1, quote1 = pair1.split('/')
    base1_uuid = _get_coin_uuid(base1)
    if not base1_uuid:
        return f"{command}\nResponse: Token {base1} is not available."
    price1 = float(_fetch_data(f"coin/{base1_uuid}/price")["price"])
    
    # Get second pair price
    base2, quote2 = pair2.split('/')
    base2_uuid = _get_coin_uuid(base2)
    if not base2_uuid:
        return f"{command}\nResponse: Token {base2} is not available."
    price2 = float(_fetch_data(f"coin/{base2_uuid}/price")["price"])
    
    return f"{command}\nResponse: {pair1} is currently trading at ${price1:,.2f}, whereas {pair2} is trading at ${price2:,.2f}."

def fetch_historical_price_data(token, time_period="7d"):
    """
    Fetch historical price data for a token
    Example: ADA over 7 days
    """
    command = f"Command: Show me the price trend for {token}/USDT over the last {time_period}."
    
    token_uuid = _get_coin_uuid(token)
    if not token_uuid:
        return f"{command}\nResponse: Token {token} is not available."
        
    history = _fetch_data(f"coin/{token_uuid}/history?referenceCurrencyUuid=yhjMzLPhuIDl&timePeriod={time_period}")
    prices = [float(entry["price"]) for entry in history["history"]]
    
    if not prices:
        return f"{command}\nResponse: No historical data available for {token}/USDT."
        
    current_price = prices[-1]
    price_min = min(prices)
    price_max = max(prices)
    
    return f"{command}\nResponse: The {token}/USDT price trend over the last {time_period} has ranged from ${price_min:.2f} to ${price_max:.2f}, with a current price of ${current_price:.2f}."

def main():
    try:
        # Example usage of all three main functions
        print(fetch_token_pair_price("ETH/USDT"))
        print("\n")
        print(compare_token_pair_prices("BTC/USDT", "ETH/USDT"))
        print("\n")
        print(fetch_historical_price_data("ADA", "7d"))
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()