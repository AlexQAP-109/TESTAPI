from pydantic import BaseModel, ValidationError, Field, validator

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




