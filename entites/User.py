from datetime import datetime
from uuid import UUID
import uuid
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id : UUID | None = Field(default=None, primary_key=True)
    email : EmailStr 
    hashed_password : str
    name : str
    surname : str
    birthdate : datetime
    gender : str
    
    def __init__(self, email: EmailStr, password: str, name: str, surname : str, birthdate : datetime, gender : str):
        self.id = uuid.uuid4()
        self.email = email
        self.hashed_password = password
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.gender = gender
    
    @property
    def age(self):
        return int((datetime.now() - self.birthdate).days / 365.2425) 

