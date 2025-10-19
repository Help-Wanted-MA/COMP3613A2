from App.models import Staff, Shift, Report
from App.database import db
from datetime import datetime, timedelta

def generate_roster():
    today = datetime.now().date()
    weekStart = today - timedelta(days=today.weekday())
    weekEnd = weekStart + timedelta(days=6)
    
    allStaff = Staff.query.all()
    roster = {}
    
    for staff in allStaff:
        shifts = Shift.query.filter(Shift.staffId == staff.id, Shift.startTime >= weekStart, Shift.startTime <= weekEnd).all()
        
        roster[staff.name] = [f'{shift.startTime.strftime("%Y/%m/%d %H:%M")} - {shift.endTime.strftime("%Y/%m/%d %H:%M")}' for shift in shifts]
        
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

    newReport = Report(roster=roster, data=data)
    db.session.add(newReport)
    db.session.commit()
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

def list_reports():
    allReports = Report.query.all()
    str = ""
    for report in allReports:
        str += f'Report ID: {report.id} | Generated on: {report.dateGenerated}\n'
        
    return str

def pretty_print_report_json(report):
    str = f'''
        ReportID: {report["id"]}
        Date Generated: {report["dateGenerated"]}
    '''
    
    for staffName, data in report["data"].items():
        str += f'''
        -----------------------------------------
            Name: {staffName}
            Total Shifts: {data["totalShifts"]},
            Total Expected Hours: {data["totalExpectedHours"]},
            Total Worked Hours: {data["totalWorkedHours"]:.2f},
            On Time: {data["onTime"]},
            Late Time Ins: {data["lateTimeIns"]},
            Early Time Outs: {data["earlyTimeOuts"]},
            Absent: {data["absents"]},
            shiftIds: {data["shiftIds"]}
        -----------------------------------------
        '''
    return str
    
def get_report(id):
    return db.session.get(Report, id)

def delete_report(id):
    report = Report.query.get(id)
    if not report: return None
    db.session.delete(report)
    db.session.commit()
    return True
    
def get_all_reports():
    return db.session.scalars(db.select(Report)).all()