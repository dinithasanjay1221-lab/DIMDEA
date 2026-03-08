import json
import random
import os

from fastapi import Header, HTTPException

DB_PATH = "database/users.json"

# create database if missing
if not os.path.exists(DB_PATH):
    os.makedirs("database", exist_ok=True)
    with open(DB_PATH, "w") as f:
        json.dump([], f)


def load_users():
    with open(DB_PATH, "r") as f:
        return json.load(f)


def save_users(users):
    with open(DB_PATH, "w") as f:
        json.dump(users, f, indent=4)


# REGISTER USER
def register_user(username, password, email=None, phone=None):

    users = load_users()

    for user in users:
        if user["username"] == username or user.get("email") == email:
            return False

    users.append({
        "username": username,
        "password": password,
        "email": email,
        "phone": phone
    })

    save_users(users)
    return True


# LOGIN VALIDATION
def validate_user(identifier, password):

    users = load_users()

    for user in users:
        if (
            user["username"] == identifier
            or user.get("email") == identifier
        ):
            if user["password"] == password:
                return True

    return False


# PASSWORD RESET
def update_password(identifier, new_password):

    users = load_users()

    for user in users:
        if (
            user["username"] == identifier
            or user.get("email") == identifier
            or user.get("phone") == identifier
        ):
            user["password"] = new_password

    save_users(users)


# OTP GENERATOR
def generate_otp():
    return str(random.randint(100000, 999999))



def get_current_user(x_user: str = Header(None)):

    users = load_users()

    for user in users:
        if user["username"] == x_user:
            return user

    raise HTTPException(
        status_code=401,
        detail="Unauthorized user"
    )