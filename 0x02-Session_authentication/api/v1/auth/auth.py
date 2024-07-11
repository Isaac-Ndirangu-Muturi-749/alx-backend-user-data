#!/usr/bin/env python3
"""
auth module for the API
"""
from typing import List
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """
    auth
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determine if the path requires authentication."""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'

        for pattern in excluded_paths:
            if pattern.endswith('*'):
                if path.startswith(pattern[:-1]):
                    return False
            elif path == pattern:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Get the value of the Authorization header"""
        if request is None or not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user"""
        return None

    def session_cookie(self, request=None):
        """Get the value of the session cookie from the request"""
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME")
        return request.cookie.get(session_name, None)