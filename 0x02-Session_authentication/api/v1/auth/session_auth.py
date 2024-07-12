#!/usr/bin/env python3
"""
auth module
"""

from typing import TypeVar
from api.v1.auth.auth import Auth
from uuid import uuid4
from flask import jsonify, make_response, request

from models.user import User


class SessionAuth(Auth):
    """SessionAuth"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create_session"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    @staticmethod
    def user_id_for_session_id(session_id: str) -> str:
        """user_id_for_session_id"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user"""
        if request is None:
            return None

        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return None

        _id = self.user_id_for_session_id(session_cookie)
        return User.get(_id)

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True

        return False
