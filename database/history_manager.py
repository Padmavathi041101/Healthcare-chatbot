from datetime import datetime

def insert_conversation_log(collection, prompt, content, conversation_id):
    logs = [
        {
            "role": "user",
            "content": prompt,
            "conversation_id": conversation_id,
            "date": datetime.utcnow()
        },
        {
            "role": "assistant",
            "content": content,
            "conversation_id": conversation_id,
            "date": datetime.utcnow()
        }
    ]
    collection.insert_many(logs)