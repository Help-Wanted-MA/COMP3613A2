from App.models import Staff, Shift
from App.database import db
from sqlalchemy.exc import SQLAlchemyError
from App.exceptions.exceptions import NotFoundError, ValidationError, ConflictError, InternalError
from datetime import datetime

def create_staff_user(username, password):
    if not username or not password:
        raise ValidationError("Missing username or password")
        
    if Staff.query.filter_by(name=username).first() is not None:
        raise ConflictError("User already exists")
        
    try:
        newstaff = Staff(name=username, password=password)
        db.session.add(newstaff)
        db.session.commit()
        return newstaff
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        raise InternalError

def time_shift(shiftId, type, time=None):
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
        
    elif type == "out":
        if shift.timedOut is not None:
            raise ConflictError("Already timed out this shift")
        
        shift.timedOut = time
        delta = shift.endTime - time
        if delta.total_seconds() > 600: #If timeOut is more than 10 minutes before scheduled end time
            shift.attendance = "earlyTimeOut"
        elif shift.attendance == "Pending":
            shift.attendance = "onTime"
            
    else:
        raise ValidationError("Invalid type. Must be 'in' or 'out'")
    
    try:
        db.session.add(shift)
        db.session.commit()
        return shift
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        raise InternalError

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
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        raise InternalError
    
def get_staff_shifts(id, date=None):
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, "%Y/%m/%d").date()
        except ValueError:
            raise ValidationError("Invalid date format. Use YYYY/MM/DD")
        
    staff = get_staff(id)
    
    if date:
        dayStart = datetime.combine(date, datetime.min.time())
        endStart = datetime.combine(date, datetime.max.time())
        shifts = Shift.query.filter(
            Shift.staffId == id,
            Shift.startTime >= dayStart, 
            Shift.startTime <= endStart
        ).all()
    else:
        shifts = Shift.query.filter(Shift.staffId == id).all()
    
    return shifts
