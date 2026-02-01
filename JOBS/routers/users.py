from fastapi import APIRouter,FastAPI,status,HTTPException,Depends
from ..import utils,models,schemas,oauth2
from ..Database import get_db
from sqlalchemy.orm import Session
from ..password_validator import validate_password

  
router = APIRouter()




@router.post("/users",status_code=status.HTTP_201_CREATED)
async def create_user(new_user:schemas.CreateUser,db:Session=Depends(get_db)):
    
    requested_role = new_user.role.capitalize()

    if requested_role not in oauth2.allowed_roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid role: {oauth2.allowed_roles}")

    validate_password(new_user.password)
    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password


    new_user = models.User(**new_user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
 
    return new_user

@router.get("/users/{user_id}")
async def get_user(user_id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Ooops! user with id: {user_id} was not found')
    
    return user


