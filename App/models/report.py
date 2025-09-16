from App.database import db
from datetime import datetime

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dateGenerated = db.Column(db.DateTime, nullable=False)
    roster = db.Column(db.JSON)
    data = db.Column(db.JSON)

    def __init__(self, roster, data):
        self.dateGenerated = datetime.now()
        self.roster = roster
        self.data = data

    def get_json(self):
        return{
            'id': self.id,
            'dateGenerated': self.dateGenerated.strftime("%Y-%m-%d"),
            'roster': self.roster,
            'data': self.data
        }


