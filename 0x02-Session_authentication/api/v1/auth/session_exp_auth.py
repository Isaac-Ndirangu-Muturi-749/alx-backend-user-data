#!/usr/bin/env python3
""" SessionExpAuth module """

import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class that inherits from SessionAuth"""

    def __init__(self):
        """Initialize the instance with session duration"""
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session ID with an expiration time"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return the user ID for the session ID, or None if expired"""
        if not session_id:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if not created_at:
            return None

        if created_at + \
                timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return session_dict.get('user_id')
