from fastapi import APIRouter, Body, HTTPException, Depends, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Union, List


from datetime import datetime, timedelta


from  ..database.mongodb import create_mongo_client
mydb = create_mongo_client()


from ..authentication.utils import OAuth2PasswordBearerWithCookie

from jose import jwt

JWT_SECRET = 'myjwtsecret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

api = APIRouter()
templates = Jinja2Templates(directory="apps/templates")



from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")



from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# login_router = APIRouter(include_in_schema=False)
# templates = Jinja2Templates(directory="templates")



def get_password_hash(password):
    return pwd_context.hash(password)

password1 = ""
def authenticate_user(username, password):
    
    user = mydb.login.find({'$and':[{"username":username},{'status':'Approved'}]})
    

    for i in user:
       
        username = i['username']
        password1 = i['password']
        
   
        if user:
            
            password_check = pwd_context.verify(password,password1)
            
            return password_check

            
        else :
            False



def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})

    
    return to_encode


@api.post('/sign-up')
def sign_up(fullname: str, username: str, password: str, status: str,created: Union[datetime, None] = Body(default=None),token: str = Depends(oauth_scheme)):
    """This function is for inserting """
    dataInsert = dict()
    dataInsert = {
        "fullname": fullname,
        "username": username,
        "password": get_password_hash(password),
        "status": status,
        "created": created
        
        }
    mydb.login.insert_one(dataInsert)
    return {"message":"User has been save"} 
  




@api.get("/", response_class=HTMLResponse)
async def api_login(request: Request):
    return templates.TemplateResponse("login.html", {"request":request}) 