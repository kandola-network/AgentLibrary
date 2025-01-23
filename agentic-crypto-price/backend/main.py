import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import dotenv   
from data3_network_agent.lib import Data3AgentUtils
dotenv.load_dotenv()

# API Configuration


app = FastAPI(
    title="Agentic Crypto Price API",
    description="API to fetch cryptocurrency price data",
    version="0.1"
)


# Helper function to fetch data from the API
def _fetch_data(endpoint):
    API_HOST = "coinranking1.p.rapidapi.com"
    data3 = Data3AgentUtils()
    api_key = data3.fetch_agent_env_variables(docker_service_name="agentic-crypto-api", field_names=["API_KEY"])
    API_KEY = api_key["API_KEY"]
    print(f"from agent backend API_KEY: {API_KEY}")
    BASE_URL = f"https://{API_HOST}"
    HEADERS = {
        "x-rapidapi-host": API_HOST,
        "x-rapidapi-key": API_KEY
    }
    """Helper function to fetch data from API"""
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["data"]

# Helper function to get coin UUID by symbol
def _get_coin_uuid(symbol):
    """Helper function to get coin UUID"""
    coins = _fetch_data("coins?referenceCurrencyUuid=yhjMzLPhuIDl&limit=50")
    for coin in coins["coins"]:
        if coin["symbol"] == symbol:
            return coin["uuid"]
    return None

# Fetch the current price for a token pair

@app.get("/api/tokens/{token_1}/{token_2}/price", tags=["Token Price"])
def fetch_token_pair_price(token_1: str, token_2: str):
    """
    Fetch the current price for a token pair
    Example: BTC/USDT
    """
    print(f"token 1: {token_1}")
    print(f"token 2: {token_2}")
    # base, quote = token_pair.split('/')
    base_uuid = _get_coin_uuid(token_1)
    quote_uuid = _get_coin_uuid(token_2)
    
    if not base_uuid or not quote_uuid:
        raise HTTPException(status_code=404, detail=f"One or both tokens in the pair {token_1}/{token_2} are not available.")
        
    base_price = float(_fetch_data(f"coin/{base_uuid}/price")["price"])
    quote_price = float(_fetch_data(f"coin/{quote_uuid}/price")["price"])
    
    pair_price = base_price / quote_price
    return f"The current price for {token_1}/{token_2} is ${pair_price:,.2f}."

# Compare prices of two token pairs
@app.get("/api/tokens/{token_1_pair_1}/{token_2_pair_1}/{token_1_pair_2}/{token_2_pair_2}/compare", tags=["Token Price Comparison"])
def compare_token_pair_prices(token1_pair1: str, token2_pair1: str, token1_pair2: str, token2_pair2: str):
    """
    Compare prices of two token pairs
    Example: BTC/USDT vs ETH/USDT
    """    
    # Get first pair price
    base1_uuid = _get_coin_uuid(token1_pair1)
    if not base1_uuid:
        raise HTTPException(status_code=404, detail=f"Token {token1_pair1} is not available.")
    price1 = float(_fetch_data(f"coin/{base1_uuid}/price")["price"])

    base2_uuid = _get_coin_uuid(token2_pair1)
    if not base2_uuid:
        raise HTTPException(status_code=404, detail=f"Token {token2_pair1} is not available.")
    price2 = float(_fetch_data(f"coin/{base2_uuid}/price")["price"])

    pair1_price = price1 / price2

    base3_uuid = _get_coin_uuid(token1_pair2)
    if not base3_uuid:
        raise HTTPException(status_code=404, detail=f"Token {token1_pair2} is not available.")
    price3 = float(_fetch_data(f"coin/{base3_uuid}/price")["price"])

    base4_uuid = _get_coin_uuid(token2_pair2)
    if not base4_uuid:
        raise HTTPException(status_code=404, detail=f"Token {token2_pair2} is not available.")
    price4 = float(_fetch_data(f"coin/{base4_uuid}/price")["price"])

    pair2_price = price3 / price4
        
    return f"{token1_pair1}/{token2_pair1} is currently trading at ${pair1_price:,.2f}, whereas {token1_pair2}/{token2_pair2} is trading at ${pair2_price:,.2f}."

# Fetch historical price data for a token
@app.get("/api/tokens/{token}/history/{timeperiod}", tags=["Historical Price Data"])
def fetch_historical_price_data(token: str, time_period: str = "7d"):
    """
    Fetch historical price data for a token
    Example: ADA over 7d (7 days)
    """    
    token_uuid = _get_coin_uuid(token)
    if not token_uuid:
        raise HTTPException(status_code=404, detail=f"Token {token} is not available.")
        
    history = _fetch_data(f"coin/{token_uuid}/history?referenceCurrencyUuid=yhjMzLPhuIDl&timePeriod={time_period}")
    prices = [float(entry["price"]) for entry in history["history"]]
    
    if not prices:
        raise HTTPException(status_code=404, detail=f"No historical data available for {token}/USDT.")
        
    current_price = prices[-1]
    price_min = min(prices)
    price_max = max(prices)
    
    return f"The {token}/USDT price trend over the last {time_period} has ranged from ${price_min:.2f} to ${price_max:.2f}, with a current price of ${current_price:.2f}."

# Health check endpoint
@app.get("/api/status/ping", tags=["Health Check"])
def ping():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0" , port=8000, reload=True)
