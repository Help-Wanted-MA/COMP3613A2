from App.database import db
from datetime import datetime

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staffId = db.Column(db.Integer, db.ForeignKey('staff.id'))
    staffName = db.Column(db.String(200))
    adminId = db.Column(db.Integer, db.ForeignKey('admin.id'))
    adminName = db.Column(db.String(200))
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    timedIn = db.Column(db.DateTime)
    timedOut = db.Column(db.DateTime)
    attendance = db.Column(db.String(50), default="Pending")

    def __init__(self, staffId, staffName, adminId, adminName, startTime, endTime):
        self.staffId = staffId
        self.staffName = staffName
        self.adminId = adminId
        self.adminName = adminName
        self.startTime = startTime
        self.endTime = endTime

    def getExpectedHours(self):
        if not self.startTime or not self.endTime:
            return None
        else:
            return (self.endTime - self.startTime).total_seconds() / 3600
    
    def getWorkedHours(self):
        if not self.timedIn or not self.timedOut:
            return 0
        else:
            return (self.timedOut - self.timedIn).total_seconds() / 3600
        
    def get_json(self):
        return{
            'id': self.id,
            'staffId' : self.staffId,
            'staffName': self.staffName,
            'adminId' : self.adminId,
            'adminName': self.adminName,
            'startTime' : self.startTime.strftime("%Y/%m/%d %H:%M"),
            'endTime' : self.endTime.strftime("%Y/%m/%d %H:%M"),
            'timedIn' : self.timedIn.strftime("%Y/%m/%d %H:%M") if self.timedIn else None,
            'timedOut' : self.timedOut.strftime("%Y/%m/%d %H:%M") if self.timedOut else None,
            'attendance' : self.attendance
        }


