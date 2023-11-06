from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from time import time_ns


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


@app.get('/', summary='Root')
def root():
    return 'Hello'


@app.post('/post', response_model=Timestamp, summary='Get Post')
def get_post():
    new_timestamp = Timestamp(id=len(post_db), 
                              timestamp=time_ns())
    post_db.append(new_timestamp)
    return new_timestamp


@app.get('/dog', response_model=List[Dog], summary='Get Dogs')
def get_dogs(kind: DogType = None):
    if kind:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    else:
        return list(dogs_db.values())


@app.post('/dog', response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog):
    if dog.pk not in dogs_db.keys():
        dogs_db[dog.pk] = dog
        return dog
    raise HTTPException(status_code=409, 
                        detail='The specified PK already exists.')
    

@app.get('/dog/{pk}', response_model=Dog, summary='Get Dog By Pk')
def get_dog_by_pk(pk: int):
    if pk in dogs_db:
        return dogs_db.get(pk)
    raise HTTPException(status_code=409, 
                        detail='The requested PK is not in the database.')


@app.patch('/dog/{pk}', response_model=Dog, summary='Update Dog')
def update_dog(pk: int, dog: Dog):
    if pk in dogs_db:
        dogs_db[pk].name = dog.name
        dogs_db[pk].kind = dog.kind
        return dogs_db[pk]
    raise HTTPException(status_code=409, 
                        detail='The requested PK is not in the database.')