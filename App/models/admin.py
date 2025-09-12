from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    createdShifts = db.relationship('Shift', backref="admin")

    def __init__(self, name, password):
        self.name = name
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'name' : self.name,
            'createdShifts' : [shift.get_json() for shift in self.createdShifts]
        }

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

