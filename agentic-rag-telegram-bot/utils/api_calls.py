import aiohttp
from utils.conversation_manager import conversation_manager

BASE_URL = 'http://127.0.0.1:7000'

async def make_query_call(chat_id: int, query: str, rag_category: str):
    conversations = conversation_manager.get_conversations(chat_id)
    payload = {"conversations": conversations, "id": str(chat_id), "query": query, "rag_category": rag_category}
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/query", json=payload) as response:
            response_data = await response.json()
            conversation_manager.add_conversation(chat_id, query, response_data.get('response', ''))
            return response_data

async def make_agent_call(chat_id: int, query: str):
    conversations = conversation_manager.get_conversations(chat_id)
    payload = {"conversations": conversations, "id": str(chat_id), "query": query}
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/agent", json=payload) as response:
            response_data = await response.json()
            conversation_manager.add_conversation(chat_id, query, response_data.get('response', ''))
            return response_data.get('response', '')
