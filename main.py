from tkinter import N
from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException
from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()


db: List[User] = [
    User(
        id=UUID("7f33615e-1667-4612-ba9f-9de19fee54fd"),
        first_name="Gemma",
        last_name="Teller",
        gender=Gender.female,
        roles=[Role.student]
    ),
    User(
        id=UUID("15d624bd-39a9-4748-8039-33566c99df50"),
        first_name="Clay",
        last_name="Morrow",
        gender=Gender.male,
        roles=[Role.admin, Role.user]
    )
]


@app.get("/")
async def root():
    return {"Hello": "Mundo"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    return HTTPException(
        status_code=404,
        detail=f"User with ID: {user_id} doesn't exist"
    )


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return

    raise HTTPException(
        status_code=404,
        detail=f"User with ID: {user_id} doesn't exist"
    )
