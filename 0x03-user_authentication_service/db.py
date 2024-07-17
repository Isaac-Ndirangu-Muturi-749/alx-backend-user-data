#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User

valid_fields = ['id', 'email', 'hashed_password', 'session_id',
                'reset_token']


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        """
        if not email or not hashed_password:
            return

        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments
        """
        if not kwargs or any(x not in valid_fields for x in kwargs):
            raise InvalidRequestError

        session = self._session
        query = session.query(User).filter_by(**kwargs)
        user = query.first()
        if user is None:
            raise NoResultFound(
                "No result found for the given filter criteria.")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"User has no attribute '{key}'")
            setattr(user, key, value)
        self._session.commit()
