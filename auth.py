from bcrypt import hashpw, gensalt, checkpw


def hash_password(password: str):
    password = password.encode()
    password = hashpw(password, gensalt())
    password = password.decode()
    return password
