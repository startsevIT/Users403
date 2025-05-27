from sqlmodel import col, or_
from sqlmodel.sql.expression import SelectOfScalar

from entites.User import User

# def age_sort_asceding(buffer_list : list[ReadUserModel]) -> list[ReadUserModel]:
#     buffer_list.sort(key=lambda user: user.age)
#     return buffer_list

# def age_sort_desceding(buffer_list : list[ReadUserModel]) -> list[ReadUserModel]:
#     buffer_list.sort(key=lambda user: user.age, reverse=True)
#     return buffer_list

# def name_sort_asceding(buffer_list : list[ReadUserModel]) -> list[ReadUserModel]:
#     buffer_list.sort(key=lambda user: user.name)
#     return buffer_list

# def name_sort_desceding(buffer_list : list[ReadUserModel]) -> list[ReadUserModel]:
#     buffer_list.sort(key=lambda user: user.name, reverse=True)
#     return buffer_list

#Проверить фильтр
def gender_filter(
    buffer_query : SelectOfScalar[User], 
    value : str | None) -> SelectOfScalar[User]:
    if value == None:
        return buffer_query
    
    if value.lower() not in ["мужской", "женский"]:
        raise Exception("Некорректный пол")
    
    return buffer_query.where(User.gender == value) # type: ignore

def search(
    buffer_query : SelectOfScalar[User],
    value : str | None) -> SelectOfScalar[User]:
    if value is None:
        return buffer_query
    
    return buffer_query.where(or_(col(User.name).contains(value.lower()),
                                  col(User.surname).contains(value.lower()),
                                  col(User.email).contains(value.lower()))) 

def pagination(
    buffer_query : SelectOfScalar[User],
    size : int | None, 
    num : int | None) -> SelectOfScalar[User]:
    
    if size is None or num is None:
        return buffer_query
    
    return buffer_query.offset(size * num).limit(size)

def sort(buffer_list : SelectOfScalar[User],
        field : str | None = None, 
        sort_type : int | None = None) -> SelectOfScalar[User]:
    if(field is None or sort_type is None):
        return buffer_list
    
    if(field == "name" and sort_type == 0):
        return buffer_list.order_by(User.name)
    if(field == "name" and sort_type == 1):
        return buffer_list.order_by(User.name.desc())
    if(field == "age" and sort_type == 0):
        return buffer_list.order_by(User.age)
    if(field == "age" and sort_type == 1):
        return buffer_list.order_by(User.age.desc())
    raise Exception("Неожиданная ошибка в сортировке")
    