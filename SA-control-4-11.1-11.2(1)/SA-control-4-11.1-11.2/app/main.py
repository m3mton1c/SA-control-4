from fastapi import FastAPI
from .exceptions import CustomExceptionA, CustomExceptionB
from fastapi.exceptions import RequestValidationError
from .handlers import ( custom_exception_a_handler, custom_exception_b_handler, validation_exception_handler)
from .schemas import User

app = FastAPI()

app.add_exception_handler(CustomExceptionA, custom_exception_a_handler)
app.add_exception_handler(CustomExceptionB, custom_exception_b_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.get("/check")
def check(flag: bool):
    if not flag:
        raise CustomExceptionA()
    return {"message": "OK"}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id != 1:
        raise CustomExceptionB()
    return {"item_id": item_id}

@app.post("/users")
def create_user(user: User):
    return {"message": "User created", "data": user}

db = {}
current_id = 1

@app.post("/simple-users", status_code=201)
def create_simple_user(user: dict):
    global current_id
    db[current_id] = user
    response = {"id": current_id, **user}
    current_id += 1
    return response

@app.get("/simple-users/{user_id}")
def get_simple_user(user_id: int):
    if user_id not in db:
        raise CustomExceptionB()
    return {"id": user_id, **db[user_id]}

@app.delete("/simple-users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in db:
        raise CustomExceptionB()
    del db[user_id]