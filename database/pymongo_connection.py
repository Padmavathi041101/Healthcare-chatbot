import pymongo

class mongo_db:

    def __init__(self, connection_string, database) -> None:
        self.connection_string = connection_string
        self.database = database
        self.client = None
        self.db = None

    def connect(self):
        """Connect to the MongoDB database."""
        if self.client is None:  # Check if already connected to avoid reconnecting
            self.client = pymongo.MongoClient(self.connection_string)
            self.db = self.client[self.database]

    def get_collection(self, collection_name):
        """Connect to the database and get a collection directly."""
        self.connect()  # Ensure connection to the database
        return self.db[collection_name]

    def insert_one(self, collection_name, data):
        """Insert a single document into a collection."""
        collection = self.get_collection(collection_name)
        return collection.insert_one(data).inserted_id

    def insert_many(self, collection_name, documents):
        """Insert multiple documents into a collection."""
        collection = self.get_collection(collection_name)
        return collection.insert_many(documents).inserted_ids

    def find_document(self, collection, query):
        """Find a document in a collection."""
        if self.db is None:
            self.connect()
        collection = self.db[collection]
        return collection.find_one(query)
    
    def find_documents_by_user_id(self, collection_name, user_id):
        """Retrieve documents from a collection that match the given user_id."""
        collection = self.db[collection_name]
        documents = collection.find({"user_id": user_id}, {"role": 1, "content": 1, "_id": 0})
        return list(documents)

    def update_document(self, collection, query, new_values):
        """Update a document in a collection."""
        if self.db is None:
            self.connect()
        collection = self.db[collection]
        return collection.update_one(query, {"$set": new_values})

    def delete_document(self, collection, query):
        """Delete a document from a collection."""
        if self.db is None:
            self.connect()
        collection = self.db[collection]
        return collection.delete_one(query)

    def close_connection(self):
        """Close the database connection."""
        if self.client:
            self.client.close()
