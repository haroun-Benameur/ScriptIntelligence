# app/user_service.py

from app.models import User

users_db = []
user_id_counter = 1


def create_user(name: str, email: str) -> User:
    global user_id_counter

    # Check uniqueness
    for user in users_db:
        if user.email == email:
            raise ValueError("Email already exists")

    new_user = User(id=user_id_counter, name=name, email=email)
    users_db.append(new_user)
    user_id_counter += 1

    return new_user


def get_user_by_email(email: str) -> User:
    for user in users_db:
        if user.email == email:
            return user

    raise ValueError("User not found")
