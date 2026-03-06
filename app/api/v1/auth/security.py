from bcrypt import checkpw, hashpw, gensalt

def get_password_hash(password: str):
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

def verify_password(users_password: str, hashed_password: str):
    return checkpw(users_password.encode("utf-8"), hashed_password.encode("utf-8"))