from sqlalchemy.orm import Session
from fastapi import APIRouter,FastAPI,Header,Depends,status,HTTPException
from ..Database import get_db
from ..import schemas,models,oauth2
from ..routers import users,jobs,resume
from ..oauth2 import role_required




router = APIRouter()



@router.post("/applications",status_code=status.HTTP_201_CREATED)
async def application(new_application:schemas.Application,db:Session=Depends(get_db),current_user:models.User = Depends(role_required(["User"]))):
#async def application(new_application:schemas.Application,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #ensuring the applicant has a resume before applying for the job
    resume = db.query(models.Resume).filter(models.Resume.user_id==current_user.id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You are required to create a resume before applying to this job"
        )
    
    job = db.query(models.Job).filter(models.Job.id == new_application.job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Job with: {new_application.job_id} does not exist")

    
    existing = db.query(models.Application).filter(models.Application.job_id==new_application.job_id,models.Application.user_id==current_user.id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'You have already reacted to this application')
    
    new_application = models.Application(**new_application.dict(),
                                         #cover_letter=new_application.cover_letter,
                                         user_id=current_user.id,
                                         resume_id=resume.id
                                         )
    
   
    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


@router.get("/applications")
async def get_all_application(db:Session=Depends(get_db),current_user:models.User = Depends(role_required(["Recruiter","Admin"]))):
    application = db.query(models.Application).all()

    if not current_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Not allowed to perform the above command")
    return application


@router.get("/applications/{application_id}")
async def get_application(application_id:int,db:Session=Depends(get_db),current_user:models.User = Depends(role_required(["Recruiter","Admin"]))):

    application = db.query(models.Application).filter(models.Application.id==application_id).first()
    

    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Application with id {application_id} was not found")
    
    return application


@router.patch("/applications/{application_id}")
async def update_application(application_id:int,update_application:schemas.UpdateApplication,db:Session=Depends(get_db),
                             current_user:int=Depends(oauth2.get_current_user)):
    application_query = db.query(models.Application).filter(models.Application.id==application_id)
    application = application_query.first()

    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Application with id:{application_id} was not found')

    if application.user_id != current_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Unable to processe your request")
    
    application_query.update(update_application.dict(),synchronize_session=False)
    db.commit()

    return application_query.first()


@router.delete("/applications/{application_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(application_id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    application_query = db.query(models.Application).filter(models.Application.id == application_id)
    application = application_query.first()

    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Application with id: {application_id} was not found")
    
    if application.user_id != current_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Unable to process your request')
    
    application_query.delete(synchronize_session=False)
    return application_query.first()

    
