import re
from fastapi import HTTPException,status,Header,Depends
from .import models
from .Database import get_db
from sqlalchemy.orm import Session



def validate_password(password:str,db:Session=Depends(get_db)):

    if len(password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                           detail=f'Your password should contain more than 8 characters')
    
    #atleast one uppercase letter
    if not re.search(r'[A-Z]',password):
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f'Password should  contain an uppercase letter')

    ## At least one digit 
    if not re.search(r"\d", password):
        raise HTTPException( status_code=status.HTTP_405_METHOD_NOT_ALLOWED, 
                            detail="Password must contain at least one digit." ) 
    # At least one special character 
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): 
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Password must contain at least one special character." ) 
    
    return password

    





