from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List

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

#Путь /
@app.get('/')
def root():
    return{'message':'Hello, world!'}

#Получение списка собак
@app.post('/post')
def post() -> Timestamp:
    curr_time = datetime.now().timestamp()
    time = Timestamp(id=len(post_db), timestamp=int(curr_time))
    post_db.append(time)
    return time

#Получение собаки по типу
@app.get('/dog')
def get_dogs(kind: DogType=None)->List[Dog]:
    if kind is None:
        return list(dogs_db.values())
    list_dog = []
    for dog in dogs_db.values():
        if dog.kind == kind:
            list_dog.append(dog)
    return list_dog

#Создание записи собаки
@app.post('/dog')
def made_dog(dog: Dog)->Dog:
    if dog.pk in dogs_db:
        raise HTTPException(status_code=404)
    dogs_db[dog.pk] = dog
    return dog

#Получение собаки по id
@app.get('/dog/{pk}')
def get_dog(pk: int)-> Dog:
    if pk not in dogs_db:
        raise HTTPException(status_code=404)
    return dogs_db[pk]

#обновление собаки по id
@app.patch('/dog/{pk}')
def update_dog(pk: int, dog: Dog)->Dog:
    if pk not in dogs_db:
        raise HTTPException(status_code=404)
    if pk != dog.pk:
        raise HTTPException(status_code=404)
    dogs_db[pk] = dog
    return dog

