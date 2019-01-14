import sqlalchemy
from user import User
from config import db
from helpers import apology

# Depository with user's functionality

class UserRepository:

    def add(self, name, date_of_birth, email):
        ''' Add user to database '''
        user = User(name = name,
                    date_of_birth = date_of_birth,
                    email = email)
        try:
            db.session.add(user)
            db.session.commit()
            return return_to_user(user)
        except AssertionError as err:
            db.session.rollback()
            return apology(err, 400)
            
    def get_user(self, email):
        ''' Get user by email (unique field)'''
        user = db.session.query(User).filter(email=email).one_or_none()
        return return_to_user(user)
        
    def update(self, user_id, name, date_of_birth, email):  
        ''' Get user by id and update it. Return updated user.'''
        try:
	    db.session.query(User).get(user_id).update({'name': name,
	                                                'email': email,
	                                                'date_of_birth': date_of_birth}) 
	    db.session.commit()
            user = db.session.query(User).get(user_id)
            return return_to_user(user)
        except AssertionError as err:
            db.session.rollback()
            return apology(err, 400)

    def remove(self, email):
        ''' Removes user with given email using soft delete pattern'''
        try:
            user = self.get_user(email)
            user.deleted = True
            db.session.commit()
            return return_to_user(user)
        except AssertionError as err:
            db.session.rollback()
            return apology(err, 400)

    def get_list(self, page, users_per_page):
        ''' Retrieve specific number of users' names and emails from the db '''
        users = db.session.query(User.name, User.email).\
                           order_by(User.name.desc()).\
                           paginate(page, users_per_page, False)
        
   

    @staticmethod
    def return_to_user(user):
        ''' Return dict with specific fields from 'user', not the whole 'user' '''
        return {'name': user.name, 'email': user.email, 'date_of_birth': user.date_of_birth}


   

