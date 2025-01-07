import uuid
from datetime import datetime

class ConversationManager:
    def __init__(self):
        self.conversations = {}

    def add_conversation(self, chat_id: int, query: str, response: str = ""):
        if chat_id not in self.conversations:
            self.conversations[chat_id] = []
        self.conversations[chat_id].append({
            "address": str(uuid.uuid4()),
            "dateCreated": int(datetime.now().timestamp() * 1000),
            "query": query,
            "response": response,
            "status": "COMPLETED"
        })

    def get_conversations(self, chat_id: int):
        return self.conversations.get(chat_id, [])

    def clear_conversations(self, chat_id: int):
        if chat_id in self.conversations:
            del self.conversations[chat_id]

conversation_manager = ConversationManager()
