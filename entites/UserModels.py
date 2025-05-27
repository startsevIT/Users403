from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID
from pydantic import AfterValidator, BaseModel, EmailStr
from entites.validators import birthdate_validate, gender_validate, password_validate

class RegisterUserModel(BaseModel):
    email : EmailStr
    password : Annotated[str, AfterValidator(password_validate)]
    name : str
    surname : str
    birthdate : Annotated[datetime, AfterValidator(birthdate_validate)]
    gender : Annotated[str, AfterValidator(gender_validate)]
    
class LoginUserModel(BaseModel):
    email : EmailStr
    password : str
    
class ReadUserModel(BaseModel):
    id : UUID | None
    email : EmailStr 
    name : str
    surname : str
    birthdate : datetime
    age : int
    gender : str
      
class UpdateUserModel(BaseModel):
    email : Optional[EmailStr | None] = None
    name : Optional[str | None] = None 
    surname : Optional[str | None] = None 
    birthdate : Optional[Annotated[datetime, AfterValidator(birthdate_validate)] | None] = None 
    password : Optional[Annotated[str, AfterValidator(password_validate)] | None] = None 
    gender : Optional[Annotated[str, AfterValidator(gender_validate)] | None] = None 
