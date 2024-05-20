import strawberry
from typing import Optional,List

from datetime import date, datetime


from  ..database.mongodb import create_mongo_client
mydb = create_mongo_client()


@strawberry.type
class User:
   

    fullname: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    created: Optional[str] = None

    

@strawberry.type
class Query:
    
    @strawberry.field
    async def get_users(self) -> Optional[List[User]]:
        result = mydb.login.find()
        # Convert MongoDB cursor to a list of User objects
        users = [User(fullname=user['fullname'], username=user['username'], password=user['password'], created=user['created']) for user in result]
        return users

    # Define a field to fetch a single user by username
    @strawberry.field
    async def get_user_by_username(self, username: str) -> Optional[User]:
        user = mydb.login.find_one({"username": username})
        if user:
            return User(fullname=user['fullname'], username=user['username'], password=user['password'], created=user['created'])
        else:
            return None





