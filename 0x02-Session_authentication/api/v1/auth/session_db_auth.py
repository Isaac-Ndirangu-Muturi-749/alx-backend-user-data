#!/usr/bin/env python3
""" SessionDBAuth module """

from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class that inherits from SessionExpAuth"""

    def create_session(self, user_id=None):
        """Create a session ID and store it in the database"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {
            'user_id': user_id,
            'session_id': session_id
        }
        user_session = UserSession(**session_dict)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return the user ID for the session ID by querying the database"""
        if not session_id:
            return None

        try:
            user_session = UserSession.search({'session_id': session_id})
            if not user_session:
                return None

            session = user_session[0]
            if self.session_duration <= 0:
                return session.user_id

            created_at = session.created_at
            if not created_at:
                return None

            if created_at + \
                    timedelta(seconds=self.session_duration) < datetime.now():
                return None

            return session.user_id
        except Exception:
            return None

    def destroy_session(self, request=None):
        """Destroy the session in the database"""
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        try:
            user_sessions = UserSession.search({'session_id': session_id})
            if not user_sessions:
                return False
            user_session = user_sessions[0]
            user_session.remove()
            return True
        except Exception:
            return False
