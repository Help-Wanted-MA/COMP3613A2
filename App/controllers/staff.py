from App.models import Staff, Shift
from App.database import db
from datetime import datetime

def create_staff_user(name, password):
    newstaff = Staff(name=name, password=password)
    db.session.add(newstaff)
    db.session.commit()
    return newstaff

def timeShift(shiftId, type, time=None):
    shift = Shift.query.get(shiftId)
    if not shift:
        return {"success": False, "error": "Shift not found"}, 404

    if not time: 
        time = datetime.now()
        
    if type == "in":
        if shift.timedIn is not None:
            return {"success": False, "error": "Already timed in this shift"}, 400
        
        shift.timedIn = time
        delta = time - shift.startTime
        if delta.total_seconds() > 600: #If timeIn is more than 10 minutes after scheduled start time
            shift.attendance = "lateTimeIn"
            
        db.session.add(shift)
        db.session.commit()
        
    elif type == "out":
        if shift.timedOut is not None:
            return {"success": False, "error": "Already timed out this shift"}, 400
        
        shift.timedOut = time
        delta = shift.endTime - time
        if delta.total_seconds() > 600: #If timeOut is more than 10 minutes before scheduled end time
            shift.attendance = "earlyTimeOut"
        elif shift.attendance == "Pending":
            shift.attendance = "onTime"
            
        db.session.add(shift)
        db.session.commit()
        return {
            "success": True,
            "shift_id": shiftId,
            "type": type,
            "time": time.isoformat(),
            "attendance": shift.attendance
        }, 200

def get_shifts(staffId):
    staff = Staff.query.get(staffId)
    if not staff: return None
    
    shifts = ""
    for shift in staff.shifts:
        shifts += f'ID: {shift.Id}, {shift.startTime.strftime("%Y/%m/%d - %H:%M")} to {shift.endTime.strftime("%Y/%m/%d - %H:%M")}\n'
        
    return shifts
    
def list_staff():
    allStaff = Staff.query.all()
    str = ""
    for staff in allStaff:
        str += f'ID: {staff.id}, Name: {staff.name}\n'
        
    return str

def list_staff_json():
    allStaff = Staff.query.all()
    staffList = []
    for staff in allStaff:
        staffList.append({
            "id": staff.id,
            "name": staff.name
        })
    return staffList

def get_staff_by_name(name):
    result = db.session.execute(db.select(Staff).filter_by(name=name))
    return result.scalar_one_or_none()

def get_staff(id):
    return db.session.get(Staff, id)

def get_all_staff():
    return db.session.scalars(db.select(Staff)).all()

def get_all_staff_json():
    staffUsers = get_all_staff()
    if not staffUsers:
        return []
    staffUsers = [staff.get_json() for staff in staffUsers]
    return staffUsers
 
def delete_staff(id):
    staff = Staff.query.get(id)
    if not staff: return {"error": f"Admin with ID:{id} not found"}, 404
    db.session.delete(staff)
    db.session.commit()
    return {"success": f"Staff with ID:{id} successfully deleted"}, 204
