from datetime import datetime
from uuid import UUID
from sqlalchemy import Engine
from sqlmodel import  SQLModel, Session, create_engine, select
from auth.auth import create_token
from entites.User import User
from storage.UserDataManipulations import gender_filter, pagination, search, sort
from entites.UserModels import LoginUserModel, ReadUserModel, RegisterUserModel, UpdateUserModel
from auth.hash import get_password_hash, verify_password
import os.path

class UserRepository:
    __path : str 
    __engine : Engine 
    
    def __init__(self):
        self.__path = "database.db"
        self.__engine = create_engine(f"sqlite:///{self.__path}")
        
        if not os.path.exists(self.__path): 
            SQLModel.metadata.create_all(self.__engine)
            init_data(self)
    
    def register(self, reg_model : RegisterUserModel) -> None:
        if self.__identification(reg_model.email):
            raise Exception("Такой пользователь уже существует")
        
        self.__add(reg_model)
        
    def login(self, login_model : LoginUserModel) -> str:
        user : User = self.__authetification(login_model.email, login_model.password)
        token : str = create_token({"id" :  str(user.id)})
        return token
                  
    def __authetification(self, identificatior : str, password : str) -> User:
        user = self.__identification(identificatior)
        if not user:
            raise Exception("Такой пользователь не существует") 
        
        if not verify_password(password, user.hashed_password):
            raise Exception("Пароли не совпадают")  
        return user
        
    def __identification(self, identificator : str) -> User | None:
        with Session(self.__engine) as session:
            statement = select(User).where(User.email == identificator)
            user = session.exec(statement).first()
            return user
      
    def __add(self, reg_model : RegisterUserModel) -> None:
        hashed_password = get_password_hash(reg_model.password)
        user : User = User(reg_model.email, 
                        hashed_password, 
                        reg_model.name,
                        reg_model.surname,
                        reg_model.birthdate,
                        reg_model.gender)
        with Session(self.__engine) as session:
            session.add(user)
            session.commit()
    
    def read(self, 
            search_value : str | None,
            filter_value : str | None,
            sort_field : str | None, 
            sort_type : int | None,
            page_size : int | None, 
            page_num : int | None) -> list[ReadUserModel]:

        with Session(self.__engine) as session:
            b0 = select(User)
            b1 = search(b0, search_value)
            b2 = gender_filter(b1, filter_value)
            b3 = sort(b2, sort_field, sort_type)
            b4 = pagination(b3,page_size,page_num)   
            users = session.exec(b4).all()
        result = [ReadUserModel(
                id = user.id,
                email = user.email,
                name = user.name,
                surname = user.surname,
                birthdate = user.birthdate,
                age = user.age,
                gender = user.gender)
            for user in users]
        
        return result
    
    def read_by_id(self, id : UUID) -> ReadUserModel | None:
        with Session(self.__engine) as session:
            statement = select(User).where(User.id == id)
            user = session.exec(statement).first()
        
        if(user == None):
            raise Exception("Пользовтель не найден")
        
        return ReadUserModel(
                    id = user.id,
                    email = user.email,
                    name = user.name,
                    surname = user.surname,
                    birthdate = user.birthdate,
                    age = user.age,
                    gender = user.gender)
        
    def update(self, id : UUID, update_model : UpdateUserModel) -> None:
        with Session(self.__engine) as session:
            statement = select(User).where(User.id == id) 
            user = session.exec(statement).first()
            
            if user == None:
                raise Exception("Пользователь не найден")
            
            if(update_model.email != None):
                user.email = update_model.email 
            if(update_model.name != None):
                user.name = update_model.name 
            if(update_model.surname != None):
                user.surname = update_model.surname 
            if(update_model.birthdate != None):
                user.birthdate = update_model.birthdate 
            if(update_model.password != None):
                user.hashed_password = update_model.password
            if(update_model.gender != None):
                user.gender = update_model.gender
                
            session.add(user)
            session.commit()
            session.refresh(user)
            
        return None          
        
    def delete(self, id : UUID) -> None:
        with Session(self.__engine) as session:  
            statement = select(User).where(User.id == id)
            user = session.exec(statement).first()
            
            if(user == None):
                raise Exception("Пользовтель не найден")
            
            session.delete(user)  
            session.commit()  
    
    def get_gender_tags(self) -> set[str]:
        with Session(self.__engine) as session:
            statement = select(User.gender)
            genders = session.exec(statement).all()
        return set(genders)

    
    
    
def init_data(user_repo : UserRepository):
    #region init_data
    user_repo.register(RegisterUserModel( 
        email="1@mail.ru", 
        password="123aaaAAA", 
        name="АААААА", 
        surname="Первый",
        birthdate=datetime(1999,3,4),
        gender="Мужской"))

    user_repo.register(RegisterUserModel( 
        email="2@mail.ru", 
        password="123aaaAAA", 
        name="ЯЯЯЯЯЯЯ", 
        surname="Первый",
        birthdate=datetime(1899,3,4),
        gender="Мужской"))

    user_repo.register(RegisterUserModel( 
        email="3@mail.ru", 
        password="123aaaAAA", 
        name="ГГГГГГГ", 
        surname="Первый",
        birthdate=datetime(1989,3,4),
        gender="Мужской"))

    user_repo.register(RegisterUserModel( 
        email="4@mail.ru", 
        password="123aaaAAA", 
        name="ЖЖЖЖЖЖЖ", 
        surname="Первый",
        birthdate=datetime(1779,3,4),
        gender="Мужской"))

    user_repo.register(RegisterUserModel( 
        email="5@mail.ru", 
        password="123aaaAAA", 
        name="ВВВВВВВВ", 
        surname="Первый",
        birthdate=datetime(1777,3,4),
        gender="Женский"))

    user_repo.register(RegisterUserModel( 
        email="6@mail.ru", 
        password="123aaaAAA", 
        name="ЛЛЛЛЛЛЛЛЛ", 
        surname="Первый",
        birthdate=datetime(2005,3,4),
        gender="Женский"))

    user_repo.register(RegisterUserModel( 
        email="7@mail.ru", 
        password="123aaaAAA", 
        name="МММММММММ", 
        surname="Первый",
        birthdate=datetime(2001,3,4),
        gender="Женский"))

    user_repo.register(RegisterUserModel( 
        email="8@mail.ru", 
        password="123aaaAAA", 
        name="НННННННННН", 
        surname="Первый",
        birthdate=datetime(2002,3,4),
        gender="Женский"))

    user_repo.register(RegisterUserModel( 
        email="9@mail.ru", 
        password="123aaaAAA", 
        name="КККККККК", 
        surname="Первый",
        birthdate=datetime(2003,3,4),
        gender="Женский"))

    user_repo.register(RegisterUserModel( 
        email="10@mail.ru", 
        password="123aaaAAA", 
        name="ААААААААА", 
        surname="Первый",
        birthdate=datetime(2003,3,4),
        gender="Женский"))
    #endregion`