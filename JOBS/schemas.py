from pydantic import BaseModel,EmailStr,validator,root_validator,model_validator
from typing import Optional
from JOBS.password_validator import validate_password


class Job(BaseModel):
    Job_position:str
    Job_description:str
    Skills_required:str
    location:str
    Job_salary:int
    Required_experience:int
    Education_background:str

class CreateJob(BaseModel):
    Job_position:str
    Job_description:str
    Skills_required:str
    location:str
    Job_salary:int
    Required_experience:int
    Education_background:str

class UpdateJob(BaseModel):
    Job_position:str
    Job_description:str
    Skills_required:str
    location:str
    Job_salary:int
    Required_experience:int
    Education_background:str

class CreateUser(BaseModel):
    first_name:str
    second_name:str
    surname:str
    email:EmailStr
    password:str
    location:str
    role:str = "User"
    _password_validator = validator("password", allow_reuse=True)(validate_password)

    @model_validator(mode="after")
    def validate_names(cls, models): 

        first = models.first_name 
        middle = models.second_name 
        surname = models.surname
        names = [n for n in [first, middle, surname] if n] 
        if len(names) != len(set(names)):
            raise ValueError("First name, middle name, and surname cannot all be identical.") 
        return models



class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int] = None
    role:Optional[str] = None



class Application(BaseModel):
    job_id:int
    cover_letter:str

class UpdateApplication(BaseModel):
    cover_letter:str


class Resume(BaseModel):
    skills:str
    experience:int
    education_level:str
    expected_salary:int

class ResumeCreate(BaseModel):
    pass


class Rule(BaseModel):
    criteria:str
    weight:float
    threshold:float

class RuleUpdate(BaseModel):
    criteria:str
    weight:float
    threshold:float


