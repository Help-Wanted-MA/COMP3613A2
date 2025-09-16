from App.database import db
from datetime import datetime

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staffId = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    adminId = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    timedIn = db.Column(db.DateTime)
    timedOut = db.Column(db.DateTime)
    attendance = db.Column(db.String(50), default="Pending")

    def __init__(self, staffId, adminId, startTime, endTime):
        self.staffId = staffId
        self.adminId = adminId
        self.startTime = startTime
        self.endTime = endTime

    def reschedule(self, startTime, endTime):
        self.startTime = startTime
        self.endTime = endTime
        self.timedIn = None
        self.timedOut = None
        self.attendance = "Pending"
        
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
            'adminId' : self.adminId,
            'startTime' : self.startTime.strftime("%Y/%m/%d %H:%M"),
            'endTime' : self.endTime.strftime("%Y/%m/%d %H:%M"),
            'timedIn' : self.timedIn.strftime("%Y/%m/%d %H:%M") if self.timedIn else None,
            'timedOut' : self.timedOut.strftime("%Y/%m/%d %H:%M") if self.timedOut else None,
            'attendance' : self.attendance
        }


