from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from .import resume,jobs
from ..Database import get_db 
from ..import schemas,models
import re 
from difflib import SequenceMatcher
from JOBS.notification  import celery_app
from ..notification import send_email

router = APIRouter()

def tokenize_skills(skills_str: str): 
    if not skills_str: 
        return []
     # Lowercase, split on commas/colons/semicolons, strip punctuation 
    tokens = re.split(r"[,:;]", skills_str.lower()) 
    return [t.strip() for t in tokens if t.strip()]

def fuzzy_overlap(resume_skills, job_skills, threshold=0.7): 
    matches = 0 
    for r in resume_skills: 
        for j in job_skills:
             if SequenceMatcher(None, r, j).ratio() >= threshold: 
                 matches += 1 
             break 
        return matches / len(job_skills) if job_skills else 0.0


def normalize_cv(resume, job):
     
     
     # Experience normalized to max 10 years 
     experience_score = min(resume.experience / 10, 1.0) 
     # Tokenize skills 
     resume_skills = tokenize_skills(resume.skills) 
     job_skills = tokenize_skills(job.Skills_required) 
     # Fuzzy overlap 
     skills_overlap = fuzzy_overlap(resume_skills, job_skills)
    #mapping education
     education_map = {"PHD":0.9,"MASTERS":0.8,"BACHELORS":0.5,"DIPLOMA":0.3,"OTHERS":0.1}
     education_score = education_map.get(resume.education_level.upper(),0.0)

     # Salary expectation normalized 
     salary_score = min(resume.expected_salary / job.Job_salary, 1.0)


     return {"experience":experience_score,"skills":skills_overlap,"education":education_score,"salary":salary_score}




@router.post("/applications/{application_id}/score",status_code=status.HTTP_201_CREATED)
async def score_application(application_id:int,db:Session=Depends(get_db)):
    application = db.query(models.Application).filter(models.Application.id==application_id).first()
    if application is None:
        raise HTTPException(status_code= 404,#status.HTTP_404_NOT_FOUND,
                            detail = f"Application with id {application_id} was not found")
    
    job = db.query(models.Job).filter(models.Job.id==application.job_id).first()
    resume  = db.query(models.Resume).filter(models.Resume.user_id==application.user_id).first()
    if not resume:
        raise HTTPException(status_code=404,
                            detail=f"Resume not found")
    #rules = db.query(models.JobScoringRule).filter(models.Job.id==application.job_id)
    rules = db.query(models.JobScoringRule).filter(models.JobScoringRule.job_id == application.job_id).all()

    if not rules:
        application_status = "submitted"
        db.commit()
        return {"application_id":application.id,"score":None,"status":application_status}



    #normalizing the users scores
    user_scores = normalize_cv(resume,job)

    #compute weigthed score
    total_score = 0
    for rule in rules:
        total_score += user_scores[rule.criteria] * rule.weight

    #comparison against threshold
    status = application.status
    threshold = (sum([rule.threshold or 0 for rule in rules]) / len(rules)) if rules else 0.5 #the default value
    if total_score >= threshold:
        status = "Qualified" 
    else: 
        status = "Not Qualified"
    
    #updating the application score
    application.score =  total_score
    application.status = status
    db.commit()

    job = db.query(models.Job).filter(models.Job.id==application.job_id).first()
    if application.status == "Qualified":

        kwargs = {
            "to_email": application.user.email, 
            "subject": "Congratulations🥳🥳🥳{}!".format(application.user.first_name),
            "body": f"Dear applicant you have qualified for {job.Job_position} position in our company" 
        } 
        # Use apply_async instead of send_task 
        task = send_email.apply_async(kwargs=kwargs) 
        print("Enqueued task ID:", task.id) 
        print("to_email:", kwargs["to_email"]) 
        print("subject:", kwargs["subject"]) 
        print("body:", kwargs["body"]) 

        return{"application":application.id,"score":total_score,"status":status}


    







    




