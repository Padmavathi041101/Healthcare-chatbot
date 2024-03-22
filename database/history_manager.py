from datetime import datetime

def insert_conversation_log(collection, prompt, content, user_id, conversation_id, conversation_type, connectycube_dialog_id, latitude, longitude):
    logs = [
        {
            "role": "user",
            "content": prompt,
            "user_id": user_id,
            "conversation_id": conversation_id,
            "conversation_type": conversation_type,
            "connectycube_dialog_id": connectycube_dialog_id,
            "latitude": latitude,
            "longitude": longitude,
            "date": datetime.utcnow()
        },
        {
            "role": "assistant",
            "content": content,
            "user_id": user_id,
            "conversation_id": conversation_id,
            "conversation_type": conversation_type,
            "connectycube_dialog_id": connectycube_dialog_id,
            "latitude": latitude,
            "longitude": longitude,
            "date": datetime.utcnow()
        }
    ]
    collection.insert_many(logs)