#!/usr/bin/env python3
"""encrypt_password module"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Salted password generation"""
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a password matches its hashed version"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
