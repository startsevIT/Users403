import re
from dateutil.relativedelta import relativedelta
from datetime import datetime

def birthdate_validate(value : datetime) -> datetime:
    if(value > (datetime.now() - relativedelta(years = 18))):
        raise Exception("Вам должно быть больше 18 лет")
    return value

def gender_validate(value : str) -> str:
    if(value.lower() not in ["мужской", "женский"]):
        raise Exception("Пола всего два")
    return value 

def password_validate(value : str):
    if(not(8 < len(value) < 20)):
        raise Exception("Длина пароля должна быть от 8 до 20 символов")
    if(not bool(re.search(r'[A-Z]', value))):
        raise Exception("Пароль должен содержать хотя-бы одну заглавную букву")
    if(not bool(re.search(r'[a-z]', value))):
        raise Exception("Пароль должен содержать хотя-бы одну прописную букву")
    if(not bool(re.search(r'\d', value))):
        raise Exception("Пароль должен содержать хотя-бы одну цифру")
    return value
