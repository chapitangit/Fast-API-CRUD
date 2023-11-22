import pymongo
from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# Create or switch to a database named 'sampledb'
db = client.sampledb

# Create a collection named 'users' in the 'sampledb' database
users_collection = db.users

# CREATE (Insert a document)
user_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 25
}

user_id = users_collection.insert_one(user_data).inserted_id
print(f"User added with ID: {user_id}")

# READ (Find documents)
print("All users:")
for user in users_collection.find():
    print(user)

# UPDATE (Update a document)
query = {"name": "John Doe"}
new_values = {"$set": {"age": 26}}
users_collection.update_one(query, new_values)
print("User updated")

# READ (Find and print updated document)
updated_user = users_collection.find_one({"name": "John Doe"})
print("Updated user:")
print(updated_user)

# DELETE (Delete a document)
delete_query = {"name": "John Doe"}
users_collection.delete_one(delete_query)
print("User deleted")

# READ (Find and print remaining documents)
print("Remaining users:")
for user in users_collection.find():
    print(user)

# Close the MongoDB connection
client.close()
