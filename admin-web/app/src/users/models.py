# -*- coding: utf-8 -*-

import dateutil.parser
from sqlalchemy import Boolean, Column, Integer, String, Date, DateTime
from app.src.utils.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=False)
    user_id = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=True)
    landline_number = Column(String(255), nullable=True)
    mobile_number = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    status = Column(String(255), nullable=True)
    created_date = Column(DateTime, nullable=False)
    updated_date = Column(DateTime, nullable=True)
    deleted_date = Column(DateTime, nullable=True)

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.birth_date = data['birth_date']
        self.landline_number = data['landline_number']
        self.mobile_number = data['mobile_number']
        self.image_url = data['image_url']
        self.status = data['status']
        if data['created_date'] is not None:
            self.created_date = dateutil.parser.parse(data['created_date'])
        else:
            self.created_date = None
        if data['updated_date'] is not None:
            self.updated_date = dateutil.parser.parse(data['updated_date'])
        else:
            self.updated_date = None
        if data['deleted_date'] is not None:
            self.deleted_date = dateutil.parser.parse(data['deleted_date'])
        else:
            self.deleted_date = None

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @property
    def serialize(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'birth_date': self.birth_date,
            'landline_number': self.landline_number,
            'mobile_number': self.mobile_number,
            'image_url': self.image_url,
            'status': self.status,
            'created_date': self.created_date,
            'updated_date': self.updated_date,
            'deleted_date': self.deleted_date
        }
