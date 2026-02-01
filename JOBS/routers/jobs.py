from fastapi import APIRouter,Header,Depends,HTTPException,status
from ..import models,schemas,oauth2
from ..Database import get_db
from sqlalchemy.orm import Session
from..oauth2 import role_required
from ..service.job_search import search_jobs


router = APIRouter()



#creating the clud for jobs
@router.get("/jobs")
async def read_all_books(db:Session=Depends(get_db)):
    jobs = db.query(models.Job).all()
    return jobs

@router.get("/jobs/{job_id}")
async def get_one_job(job_id:int,db:Session=Depends(get_db)):#,current_user:models.User=Depends(role_required(["Recruiter","Admin","User"]))):
    #job = db.query(models.Job).filter(models.Job.id==job_id).first()
    job = search_jobs(job_id,db)

    
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Ooops! job with id: {job_id} was not found')
    
   # Only count views if the current user is a candidate 
    #if current_user.role == "User": 
    #    existing_view = db.query(models.JobView).filter_by( job_id=job_id, user_id=current_user.id ).first() 
    #    if not existing_view: 
    #        # Record new unique view 
    #         
    #        new_view = models.JobView(job_id=job_id, user_id=current_user.id) 
    #        db.add(new_view) 
    #        job.views += 1 
    #        db.commit() 
    #        db.refresh(job)

    return job

@router.post("/jobs",status_code=status.HTTP_201_CREATED)
#async def create_new_post(recent_job:schemas.CreateJob,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
async def create_new_job( recent_job: schemas.CreateJob, db: Session = Depends(get_db), current_user: models.User = Depends(role_required(["Admin", "Recruiter"]))):
    print("current_user")
    recent_job = models.Job(**recent_job.dict())

    #recent_job.owner_id = current_user.id

    db.add(recent_job)
    db.commit()
    db.refresh(recent_job)

    return recent_job

@router.patch("/jobs/{job_id}")
#async def update_job(job_id:int,update_job:schemas.UpdateJob,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
async def update_job(job_id:int,update_job:schemas.UpdateJob,db:Session=Depends(get_db),current_user:models.User=Depends(role_required(["Admin","Recruiter"]))):
    job_query = db.query(models.Job).filter(models.Job.id==job_id)
    job = job_query.first()

    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Ooops! job with id: {job_id} was not found')
    job_query.update(update_job.dict(),synchronize_session=False)
    db.commit()

    return job_query.first()

@router.delete("/jobs/{job_id}",status_code=status.HTTP_204_NO_CONTENT)
#async def delete_job(job_id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
async def delete_job(job_id:int,db:Session=Depends(get_db),current_user:models.User=Depends(role_required(["Admin","Recruiter"]))):
    job_query = db.query(models.Job).filter(models.Job.id==job_id)
    job = job_query.first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Ooops! job with id: {job_id} was not found')
    
    job_query.delete(synchronize_session=False)
    db.commit()

    return job_query.first()




