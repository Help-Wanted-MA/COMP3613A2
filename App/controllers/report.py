from App.models import Staff, Shift, Report
from App.database import db
from App.exceptions.exceptions import ConflictError, InternalError, NotFoundError, ValidationError
from datetime import datetime, timedelta

#Generate a roster for the week containing `reference_date`. If no date is provided, defaults to the current week
def generate_roster(referenceDate=None):
    if referenceDate is None:
        referenceDate = datetime.now().date()
    elif isinstance(referenceDate, str):
        referenceDate = datetime.strptime(referenceDate, "%Y/%m/%d").date()
        
    weekStart = referenceDate - timedelta(days=referenceDate.weekday())
    weekEnd = weekStart + timedelta(days=5)
    
    shifts = Shift.query.filter(
        Shift.startTime >= weekStart,
        Shift.startTime <= weekEnd
    ).all()
    
    roster = {}
    
    for shift in shifts:
        staff_name = shift.staffName
        entry = f'{shift.startTime.strftime("%Y/%m/%d %H:%M")} - {shift.endTime.strftime("%Y/%m/%d %H:%M")}'
        roster.setdefault(staff_name, []).append(entry)

    return roster
   
def generate_report_data():
    today = datetime.now().date()
    weekStart = today - timedelta(days=today.weekday())
    weekEnd = weekStart + timedelta(days=7)

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
        
        shifts = Shift.query.filter(Shift.staffId == staff.id, Shift.startTime >= weekStart, Shift.startTime <= weekEnd).all() #Grab shifts from the past 7 days
        for shift in shifts:
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
            "totalShifts": totalShifts,
            "totalExpectedHours": totalExpectedHours,
            "totalWorkedHours": totalWorkedHours,
            "onTime": onTime,
            "lateTimeIns": lateTimeIns,
            "earlyTimeOuts": earlyTimeOuts,
            "absents": absents,
            "shiftIds": shiftIds
        }
        
    return data
        
     
def generate_report():
    roster = generate_roster()
    data = generate_report_data()

    try:
        newReport = Report(roster=roster, data=data)
        db.session.add(newReport)
        db.session.commit()
    except Exception as e:
        print(e)
        raise InternalError
    
    return newReport

def list_reports_json():
    allReports = Report.query.all()
    data = []
    for report in allReports:
        data.append({
            "reportId": report.id,
            "dateGenerated": report.dateGenerated
        })
        
    return data
    
def get_report(id):
    report = db.session.get(Report, id)
    if not report:
        raise NotFoundError(f'Report with ID: {id} not found')
    
    return report

def delete_report(id):
    report = Report.query.get(id)
    if not report: 
        raise NotFoundError(f"Report with ID:{id} not found")
    
    try:
        db.session.delete(report)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        raise InternalError
    
def get_all_reports():
    return db.session.scalars(db.select(Report)).all()