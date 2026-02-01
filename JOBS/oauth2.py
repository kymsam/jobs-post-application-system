from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
from .import schemas,models
from fastapi import status,Depends,HTTPException
from sqlalchemy.orm import Session
from .Database import get_db




oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 30


allowed_roles = ["Admin", "Recruiter", "User"]

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token:str,credential_exceptions):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:int = payload.get('user_id')
        role:str = payload.get("role")
        token_data = schemas.TokenData(id=id,role=role)

        if id is None or role is None:
            print ("Missing user_id or role in the payload ")
            raise credential_exceptions
    except JWTError:
        raise credential_exceptions
    return token_data

        

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Ooops could not validate credential",
                                          headers={"WWW-Authenticate":"Bearer"})
    
    token_data = verify_access_token(token,credential_exceptions)
    user = db.query(models.User).filter(models.User.id==token_data.id).first()
    user.role = token_data.role #attached role from token
    return user
    
    

def role_required(allowed_roles: list[str]): 
    def wrapper(current_user: models.User = Depends(get_current_user)): 
        if current_user.role not in allowed_roles:
             raise HTTPException( status_code=status.HTTP_403_FORBIDDEN,
                                  detail="You do not have permission to perform this action" ) 
        return current_user 
    return wrapper

    