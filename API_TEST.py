import time
from Pages.class_env import *
import json
import pytest
from pydantic import BaseModel, ValidationError, Field, validator
from typing import Optional
import requests


class VlojennuyObjekt(BaseModel):
    id: int
    type_name: str
    subtype_name: str
    class_name: str
    class_full_name: str
    class_full_name_en: str
    is_rate: int
    is_change: int

class TeloGet(BaseModel):
    data: list[VlojennuyObjekt]


"""Метод Get на получение списка классов"""

def metod_get():
    url = 'https://52.bex.su/api/classes'
    res = requests.get(url)
    result = res.json()
    status = res.status_code


    return result, status

def test_keys_validacion_json():
    """Тест кейс на валидацию Json ответа от сервера со статусом 200. для валидации ответа
    используем библиотеку pydantic, создаем макет будущего ответа. Парсим ответ и получаем первый id"""
    result, status = metod_get()
    result2 = TeloGet.model_validate(result)
    result3 = result2.data
    result4 = result3[0].id
    print(f'{status} == 200')
    assert status == 200
    print(f'Длина ответа от сервера {len(result)} != 0')
    assert len(result) != 0
    print(f'Номер id первого json {result4} == 1')
    assert result4 == 1

############################################################################

"""Тут мы используем необязательные поля и заменяем на Optional - если поле пустое None"""
class TeloGetFolders(BaseModel):
    id: int
    name: str
    name_en: str
    icon: str
    is_tag: str
    parent_id: int
    sort: int
    dashboard_id: int
    url: str
    limited_access: int
    meta_title: str
    meta_title_en: str
    meta_description:  Optional[str]
    meta_description_en:  Optional[str]
    h1: str
    h1_en: str
    detail_text: str
    detail_text_en: str
    sef: str
    icon_url: str

"""Mутод ГЕТ на получение данных по ID"""
def metod_get_folders_id(param_id):
    number_id = param_id

    url = 'https://52.bex.su/api/folders/'
    res = requests.get(url + f'{number_id}')
    result = res.json()
    status = res.status_code
    return result, status

"""Параметризем тест с помощью Pytest и валидируем ответ json с серевера
    Параметры должны соответствовать определенному типу. Пустые параметры мы с помощью
    опции Optional возвращаем либо None вместо null, либо просто string"""
@pytest.mark.parametrize("param_id", [1, 2, 3, 4, 5, 6], ids=[1, 2, 3, 4, 5, 6])
def test_get_folders_id_valid(param_id):

    resul, status = metod_get_folders_id(f'{param_id}')
    result = TeloGetFolders.model_validate(resul)
    name = result.name
    detali = result.detail_text
    meta_description = result.meta_description
    print(name)
    print(meta_description)
    assert meta_description == None or str



"""Метод Get на получение данных класса по ID"""

def metod_get_class_id(param_id):
    number_id = param_id
    url = 'https://52.bex.su/api/classes/'
    res = requests.get(url + f'{number_id}')
    result = res.json()
    status = res.status_code


    return result, status

"""Параметризем тест с помощью Pytest и валидируем ответ json с серевера
Параметры должны соответствовать определенному типу."""
@pytest.mark.parametrize("param_id", [1, 2, 3, 4, 5, 6], ids=[1, 2, 3, 4, 5, 6])
def test_get_class_id(param_id):
    resul, status = metod_get_class_id(f'{param_id}')
    result = VlojennuyObjekt.model_validate(resul)
    type_name = result.type_name
    print(type_name)
    class_name = result.class_name
    print(class_name)
    is_rate = result.is_rate
    assert type(is_rate) == int
    print(f'Тип {is_rate} == int')
    assert status == 200


"""Метод на получения АПИ ключа (док. сваггер GET запросс)"""

def metod_get_api_key_pets():
    url = 'https://petfriends.skillfactory.ru/'
    headers = {'email': Env.valid_maill, 'password': Env.valid_pass}
    res = requests.get(url + '/api/key', headers=headers)
    result = res.json()
    status = res.status_code
    return result, status

# a,b = metod_get_api_key_pets()
# print(a['key'])
"""Metod на получение всех сущностей (док. сваггер Гет запросс)"""

def metod_get_api_spisok():
    url = 'https://petfriends.skillfactory.ru/'
    auth_key, status = metod_get_api_key_pets()
    headers = {'auth_key': auth_key['key']}
    filter = {'filter': ""}
    res = requests.get(url + '/api/pets', headers=headers, params=filter)
    result = res.json()
    status = res.status_code
    return result, status

# a,b = metod_get_api_spisok()
# print(a)
class PetsVlojenie(BaseModel):
    age: str
    animal_type: str
    created_at: str
    id: str
    name: str
    pet_photo: str

class PetsOsnova(BaseModel):
    pets: list[PetsVlojenie]


a, b = metod_get_api_spisok()
a1 = PetsOsnova.model_validate(a)
age = a1.pets[2]
print(age)
