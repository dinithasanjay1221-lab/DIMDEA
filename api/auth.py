import json
import random
import os
from fastapi import Header, HTTPException

DB_PATH = "database/users.json"

# -----------------------------
# CREATE DATABASE IF MISSING
# -----------------------------
if not os.path.exists(DB_PATH):
    os.makedirs("database", exist_ok=True)
    with open(DB_PATH, "w") as f:
        json.dump([], f)

# -----------------------------
# LOAD USERS
# -----------------------------
def load_users():
    """Load all users from the JSON database."""
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If file is corrupted, reset to empty list
        return []

# -----------------------------
# SAVE USERS
# -----------------------------
def save_users(users):
    """Save all users to the JSON database."""
    with open(DB_PATH, "w") as f:
        json.dump(users, f, indent=4)

# -----------------------------
# REGISTER USER
# -----------------------------
def register_user(username, password, email=None, phone=None):
    """
    Registers a new user.
    Returns True if successful, False if username/email already exists.
    """
    users = load_users()

    for user in users:
        if user["username"] == username or (email and user.get("email") == email):
            return False

    users.append({
        "username": username,
        "password": password,
        "email": email,
        "phone": phone
    })

    save_users(users)
    return True

# -----------------------------
# LOGIN VALIDATION
# -----------------------------
def validate_user(identifier, password):
    """
    Validates login credentials.
    Returns True if user exists and password matches.
    """
    users = load_users()

    for user in users:
        if user["username"] == identifier or user.get("email") == identifier:
            if user["password"] == password:
                return True

    return False

# -----------------------------
# PASSWORD RESET
# -----------------------------
def update_password(identifier, new_password):
    """
    Updates password for a user identified by username, email, or phone.
    """
    users = load_users()

    for user in users:
        if (
            user["username"] == identifier
            or user.get("email") == identifier
            or user.get("phone") == identifier
        ):
            user["password"] = new_password

    save_users(users)

# -----------------------------
# OTP GENERATOR
# -----------------------------
def generate_otp():
    """Generates a 6-digit OTP."""
    return str(random.randint(100000, 999999))

# -----------------------------
# GET CURRENT USER
# -----------------------------
def get_current_user(x_user: str = Header(None)):
    """
    Retrieves the current user based on 'x-user' header.
    Raises 401 Unauthorized if not found.
    """
    users = load_users()

    for user in users:
        if user["username"] == x_user:
            return user

    raise HTTPException(
        status_code=401,
        detail="Unauthorized user"
    )