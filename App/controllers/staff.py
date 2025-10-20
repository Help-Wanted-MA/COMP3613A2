from App.models import Staff, Shift
from App.database import db
from App.exceptions.exceptions import NotFoundError, ValidationError, ConflictError, InternalError
from datetime import datetime

def create_staff_user(username, password):
    if not username or not password:
        raise ValidationError("Missing username or password")
        
    if Staff.query.filter_by(name=username).first() is not None:
        raise ConflictError("User already exists")
        
    newstaff = Staff(name=username, password=password)
    db.session.add(newstaff)
    db.session.commit()
    return newstaff

def timeShift(shiftId, type, time=None):
    shift = Shift.query.get(shiftId)
    if not shift:
        raise NotFoundError(f'Shift {shiftId} not found')

    if not time: 
        time = datetime.now()
        
    if type == "in":
        if shift.timedIn is not None:
            raise ConflictError("Already timed in this shift")
        
        shift.timedIn = time
        delta = time - shift.startTime
        if delta.total_seconds() > 600: #If timeIn is more than 10 minutes after scheduled start time
            shift.attendance = "lateTimeIn"
            
        db.session.add(shift)
        db.session.commit()
        
    elif type == "out":
        if shift.timedOut is not None:
            raise ConflictError("Already timed in this shift")
        
        shift.timedOut = time
        delta = shift.endTime - time
        if delta.total_seconds() > 600: #If timeOut is more than 10 minutes before scheduled end time
            shift.attendance = "earlyTimeOut"
        elif shift.attendance == "Pending":
            shift.attendance = "onTime"
            
        db.session.add(shift)
        db.session.commit()
    else:
        raise ValidationError("Invalid type. Must be 'in' or 'out'")
    
    return shift

def get_shifts(staffId):
    staff = Staff.query.get(staffId)
    if not staff:
        raise NotFoundError(f"Staff with ID: {staffId} not found")
    
    shifts = ""
    for shift in staff.shifts:
        shifts += f'ID: {shift.Id}, {shift.startTime.strftime("%Y/%m/%d - %H:%M")} to {shift.endTime.strftime("%Y/%m/%d - %H:%M")}\n'
        
    return shifts

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
    staff = result.scalar_one_or_none()
    if not staff:
        raise NotFoundError(f"Staff with name: {name} not found")
    return staff

def get_staff(id):
    staff = db.session.get(Staff, id)
    if not staff:
        raise NotFoundError(f"Staff not found with ID: {id}")
    return staff

def get_all_staff():
    return db.session.scalars(db.select(Staff)).all()
 
def delete_staff(id):
    staff = Staff.query.get(id)
    if not staff: 
        raise NotFoundError(f"Admin with ID:{id} not found")

    try:
        db.session.delete(staff)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        raise InternalError
