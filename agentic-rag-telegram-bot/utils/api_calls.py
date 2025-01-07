import aiohttp
from utils.conversation_manager import conversation_manager
from utils.constant import BASE_URL

async def make_query_call(chat_id: int, query: str, rag_category: str):
    conversations = conversation_manager.get_conversations(chat_id)
    payload = {"conversations": conversations, "id": str(chat_id), "query": query, "rag_category": rag_category}
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/query", json=payload) as response:
            response_data = await response.json()
            response_content = response_data.get('response', '')
            conversation_manager.add_conversation(chat_id, query, response_data.get('response', ''))
            return response_content

async def make_agent_call(chat_id: int, query: str):
    conversations = conversation_manager.get_conversations(chat_id)
    payload = {"conversations": conversations, "id": str(chat_id), "query": query}
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/agent", json=payload) as response:
            response_data = await response.json()
            print(response_data)
            # Extract the nested "response" string if it exists
            response_content = response_data.get('response', {}).get('response', '')

            # Print the extracted response
            print(response_content)

            # Store the conversation
            conversation_manager.add_conversation(chat_id, query, response_content)
            return response_content

