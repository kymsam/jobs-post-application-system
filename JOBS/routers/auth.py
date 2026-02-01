from fastapi import FastAPI,APIRouter,Depends,status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..Database import get_db
from sqlalchemy.orm import Session
from ..import models,schemas,utils,oauth2


router = APIRouter()

@router.post("/login")
async def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==user_credentials.username).first()
    

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail = f"‼️Oooops Invalid credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"‼️Ooops Invalid Credentials")
    

    access_token = oauth2.create_access_token(data={'user_id':user.id,"role":user.role})
    return ({'access_token':access_token,"token_type":"Bearer"})



    
    


