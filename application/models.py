from application import db

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, unique=True, nullable=False)
    firstname = db.Column(db.String, unique=True, nullable=False)
    lastname = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self,username):
        return True
    def get_id(self,username):
        return self.username
    def is_authenticated(self,authenticated):
        return self.authenticated
    def is_anonymous(self):
        return False

# class Data(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     notes = db.Column(db.String(128), index=True, unique=False)
    
    def __init__(self, notes):
        self.notes = notes

    def __repr__(self):
        return '<Data %r>' % self.notes
