#!/usr/bin/python3
import datetime
import re
import sqlalchemy
from sqlalchemy.orm import validates

from config import db
from user_repository import UserRepository
from helpers import apology

# Describe db table 'User' structure

class User(UserRepository):

    __tablename__ = "users"

    #id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date_of_birth = db.Column(db.DateTime)
    email = db.Column(db.String(80), unique=True)
    deleted = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return '<User(name {}, email: {})>'.format(self.name, self.email) if not self.deleted else None

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise AssertionError('No name provided')
        if not re.match("[a-zA-Z ]+", name):
            raise AssertionError('The name should contain only latin alphabet letters')
        if len(name) < 3 or len(name) > 20:
            raise AssertionError('The name must be between 4 and 20 characters')
        return name

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')
        if db.session.query(User).filter(User.email==email).one_or_none():
            raise AssertionError('There is already a user with this email')
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError('Provided email is not an email address')
        return email

    @validates('date_of_birth')
    def validate_dob(self, key, date_of_birth):
        if not date_of_birth:
            raise AssertionError('No date of birth provided')
        return datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')


