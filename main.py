from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from time import time


app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get(path='/', 
         summary='Root', 
         operation_id='root__get')
def root__get() -> dict:
    '''Возвращает приветствие.'''

    return {'Greetings': 'my friend!'}


@app.post(path='/post', 
          response_model=Timestamp, 
          summary='Get Post', 
          operation_id='get_post_post_post')
def get_post_post_post() -> Timestamp:
    '''
    Делает запись в базу данных с порядковым номером и количеством секунд с начала Unix эпохи.
    Возвращает отчет в виде этой записи.
    '''

    new_timestamp = Timestamp(id=len(post_db), 
                              timestamp=time())
    post_db.append(new_timestamp)

    return new_timestamp


@app.get(path='/dog', 
         response_model=List[Dog], 
         summary='Get Dogs', 
         operation_id='get_dogs_dog_get')
def get_dogs_dog_get(kind: DogType = None) -> List[Dog]:
    '''
    Возвращает список собак из базы данных.

    Parameters
    ----------
    kind: str - выбрать одну из пород собак ('terrier', 'bulldog', 'dalmatian') или всех собак (игнорируйте).
    '''
    
    if kind:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    else:
        return list(dogs_db.values())


@app.post(path='/dog', 
          response_model=Dog, 
          summary='Create Dog', 
          operation_id='create_dog_dog_post')
def create_dog_dog_post(dog: Dog) -> Dog:
    '''
    Делает запись о новой собаке в базу данных и возвращает отчет о записи в виде описания новой собаки.

    Parameters
    ----------
    dog: Dog - экземпляр класса Dog с описанием имени собаки, id(pk) и ее породы.

    Raises
    ------
    HTTPException - Если с таким pk уже есть собака в базе данных, вызовется исключение.
    '''

    if dog.pk not in dogs_db.keys():
        dogs_db[dog.pk] = dog
        return dog
    
    raise HTTPException(status_code=409, 
                        detail='The specified PK already exists.')
    

@app.get(path='/dog/{pk}', 
         response_model=Dog, 
         summary='Get Dog By Pk', 
         operation_id='get_dog_by_pk_dog__pk__get')
def get_dog_by_pk_dog__pk__get(pk: int) -> Dog:
    '''
    Возвращает описание собаки из базы данных по номеру "pk"

    Parameters
    ----------
    pk: int - уникальный идентификатор собаки в базе данных

    Raises
    ------
    HTTPException - Если в базе данных отсутствует такой "pk", вызовется исключение.
    '''

    if pk in dogs_db:
        return dogs_db.get(pk)
    
    raise HTTPException(status_code=409, 
                        detail='The requested PK is not in the database.')


@app.patch(path='/dog/{pk}', 
           response_model=Dog, 
           summary='Update Dog', 
           operation_id='update_dog_dog__pk__patch')
def update_dog_dog__pk__patch(pk: int, dog: Dog) -> Dog:
    '''
    Обновляет описание собаки в базе данных по номеру "pk" и возвращает отчет в виде обновленного описания собаки.

    Parameters
    ----------
    pk: int - уникальный идентификатор собаки в базе данных
    dog: Dog - экземпляр класса Dog с описанием имени собаки, id(pk) и ее породы.

    Raises
    ------
    HTTPException - Если в базе данных отсутствует такой "pk", вызовется исключение.
    '''

    if pk in dogs_db:
        dogs_db[pk].name = dog.name
        dogs_db[pk].kind = dog.kind
        return dogs_db[pk]
    
    raise HTTPException(status_code=409, 
                        detail='The requested PK is not in the database.')