from config import db, Constants
from helpers import user_public_info, make_public
from utils_softdelete import QueryWithSoftDelete

# Depository with user's functionality

class UserRepository(db.Model):
    __abstract__=True

    id = db.Column(db.Integer, primary_key=True)
    query_class = QueryWithSoftDelete

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def add(cls, **kwargs):
        ''' Add user to database '''
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    @make_public
    def get_user(cls, attr_name, attr_value):
        user = db.session.query(cls).filter(getattr(cls, attr_name)==attr_value).first()
        return user

    @classmethod
    @make_public
    def update(cls, email, **kwargs):
        user = db.session.query(cls).filter(getattr(cls, 'email')==email).first()
        for attr, value in kwargs.items():
            setattr(user, attr, value)
        user.save()
        return user

    @classmethod
    #@make_public
    def get_list(cls, page, users_per_page):
        # Retrieve specific number of users' names and emails from the db
        users = db.session.query(cls).\
                           paginate(page, users_per_page, False)
        return users




'''
    @classmethod
    def get_user(self, attr): #email):
        # Get user by email (unique field)
        user = db.session.query(cls).filter(cls.email==attr).one_or_none()
        return self.return_to_user(user)

    def update(self, user_id, name, date_of_birth, email):
#        Get user by id and update it. Return updated user.
        try:
            db.session.update().where('User.id'==user_id).values(name=name, email=email, date_of_birth=date_of_birth)
            db.session.commit()
            user = db.session.query(User).get(user_id).first()
            return self.return_to_user(user)
        except AssertionError as err:
            db.session.rollback()
            return apology(err, 400)

    def remove(self, email):
        #Removes user with given email using soft delete pattern
        try:
            user = self.get_user(email)
            user.deleted = True
            db.session.commit()
            return self.return_to_user(user)
        except AssertionError as err:
            db.session.rollback()
            return apology(err, 400)

    def get_list(self, page, users_per_page):
        # Retrieve specific number of users' names and emails from the db
        users = db.session.query(User.name, User.email).\
                           order_by(User.name.desc()).\
                           paginate(page, users_per_page, False)
        return users

    @staticmethod
    def return_to_user(user):
        # Return dict with specific fields from 'user', not the whole 'user'
        return {'name': user.name, 'email': user.email, 'date_of_birth': user.date_of_birth}

'''


