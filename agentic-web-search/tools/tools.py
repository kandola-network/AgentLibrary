import requests
from data3_network_variables.variables import Data3Utils

def call_web_search(query):
    
    data3 = Data3Utils().fetch_env_variables
    base_url = data3.fetch_base_url()
    port = data3.fetch_port("agentic-crypto-api")
    print("Base URL:", base_url)
    print("Port:", port)
    answer = requests.post(f"{base_url}:{port}/search", json={"query": query})
    return answer.json()

user_tools = [call_web_search]
