from pydantic_settings import BaseSettings 
from pydantic import Field

class Settings(BaseSettings):
    database_hostname:str = Field(...,env="DATABASE_HOSTNAME")
    database_username:str = Field(...,env="DATABASE_USERNAME")
    database_port:str = Field(...,env="DATABASE_POST")
    database_password:str = Field(...,env="DATABASE_PASSWORD")
    database_name:str = Field(...,env="DATABASE_NAME")
    redis_hostname:str = Field(...,env="REDIS_HOSTNAME")
    redis_port:int = Field(...,env="REDIS_PORT")
    class Config:
        env_file = '.env'



settings = Settings()