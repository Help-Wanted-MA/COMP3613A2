from App.models import Admin, Staff, Shift, Report
from App.database import db

def generate_roster():
    allStaff = Staff.query.all()
    roster = {}
    
    for staff in allStaff:
        roster[staff.name] = [f'{shift.startTime.strftime("%Y/%m/%d %H:%M")} - {shift.endTime.strftime("%Y/%m/%d %H:%M")}' for shift in staff.scheduledShifts]
        
    return roster
   
def generate_report_data():
    allStaff = Staff.query.all()
    data = {}
    for staff in allStaff:
        totalShifts = 0
        totalExpectedHours = 0
        totalWorkedHours = 0
        lateTimeIns = 0
        earlyTimeOuts = 0
        onTime = 0
        absents = 0
        shiftIds = []
        
        for shift in staff.scheduledShifts:
            shiftIds.append(shift.id)
            totalShifts += 1
            totalExpectedHours += shift.getExpectedHours()
            totalWorkedHours += shift.getWorkedHours()
            
            if shift.attendance == "lateTimeIn":
                lateTimeIns += 1
                
            elif shift.attendance == "earlyTimeOut":
                earlyTimeOuts += 1
                
            elif shift.attendance == "onTime":
                onTime += 1
                
            elif shift.attendance == "Pending":
                shift.attendance = "Absent"
                absents += 1
        
        data[staff.name] = {
            "Total Shifts": totalShifts,
            "Total Expected Hours": totalExpectedHours,
            "Total Worked Hours": totalWorkedHours,
            "On Time": onTime,
            "Late Time In": lateTimeIns,
            "Early Time Out": earlyTimeOuts,
            "Absent": absents,
            "shiftIds": shiftIds
        }
        
    return data
        
     
def create_report():
    roster = generate_roster()
    data = generate_report_data()

    newReport = Report(roster=roster, data=data)
    db.session.add(newReport)
    db.session.commit()
    return newReport

def get_report(id):
    return db.session.get(Report, id)

def delete_report(id):
    report = Report.query.get(id)
    if not report: return None
    db.session.delete(report)
    db.session.commit()
    
def get_all_reports():
    return db.session.scalars(db.select(Report)).all()