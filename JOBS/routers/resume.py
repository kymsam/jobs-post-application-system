from fastapi import APIRouter,FastAPI,Depends,status,HTTPException
from sqlalchemy.orm import Session
from ..Database import get_db
from ..import models,schemas,oauth2
from ..oauth2 import role_required


router = APIRouter()

@router.get("/resume")
async def get_resume(db:Session=Depends(get_db),current_user:models.User = Depends(role_required(["Recruiter","Admin"]))):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Unable to process your request")
    resume = db.query(models.Resume).all()

    return resume
    
@router.get("/resume/{resume_id}")
async def get_resume(resume_id:int,db:Session=Depends(get_db),current_user:models.User = Depends(role_required(["Recruiter","Admin"]))):
    resume  = db.query(models.Resume).filter(models.Resume.id==resume_id).first()

    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Resume with id:{resume_id} was not found')
    if not current_user:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Unable to process your request")
    

    
    return resume

@router.post("/resume",status_code=status.HTTP_201_CREATED)
async def post_resume(create_resume:schemas.Resume,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    resume  = models.Resume(**create_resume.dict(),user_id=current_user.id)

    existing = db.query(models.Resume).filter( models.Resume.user_id == current_user.id ).first()
    if existing: 
        raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="You already created a resume" )
    db.add(resume)
    db.commit()

    db.refresh(resume)
    return resume

@router.patch("/resume/{resume_id}")
async def update_resume(resume_id:int,update_resume:schemas.Resume,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    resume_query = db.query(models.Resume).filter(models.Resume.id==resume_id)
    resume = resume_query.first()

    if resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Resume with id:{resume_id} was never found')
    
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Unable to process your request")


    resume_query.update(update_resume.dict(),synchronize_session=False)
    db.commit()
    return resume_query.first()


@router.delete("/resume/{resume_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(resume_id:int,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    resume_query = db.query(models.Resume).filter(models.Resume.id==resume_id)
    resume = resume_query.first()

    if resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The resume with id:{resume_id}  was not found')
    
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Unable to process you request")
    
    resume_query.delete(synchronize_session=False)
    db.commit()

    return resume_query.first()