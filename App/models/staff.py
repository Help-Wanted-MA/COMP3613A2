from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    shifts = db.relationship('Shift', backref="staff")
    
    def __init__(self, name, password):
        self.name = name
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'name' : self.name,
            'shifts' : [shift.get_json() for shift in self.shifts]
        }

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

