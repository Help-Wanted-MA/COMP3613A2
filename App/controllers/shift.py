from App.models import Shift
from App.database import db
from datetime import datetime
from App.exceptions.exceptions import ConflictError, InternalError, NotFoundError, ValidationError
def get_shift_info(id):
    shift = Shift.query.get(id)
    if not shift:
        print("Shift not found")
        return None
    
    return shift.get_json()

def is_shift_timed_in(id):
    shift = Shift.query.get(id)
    if not shift:
        print("Shift not found")
        return None
    
    if shift.timedIn and not shift.timedOut: # A timedIn time with no timedOut time means a staff member has started the shift
        return True
    else:
        return False
    
def delete_shift(id):
    shift = Shift.query.get(id)
    if not shift: 
        raise NotFoundError(f"Admin with ID:{id} not found")
    
    try:
        db.session.delete(shift)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        raise InternalError
    
def pretty_print_shift_json(shift):
    str = f'''
        ShiftID: {shift["id"]}
        Start time: {shift["startTime"]}
        End time: {shift["endTime"]}
        Timed in: {shift["timedIn"]}
        Timed out: {shift["timedOut"]}
        Attendance: {shift["attendance"]}
    '''
    return str

def get_shift(id):
    return db.session.get(Shift, id)

def reschedule_shift(id, startTime, endTime):
    shift = get_shift(id)
    if not shift:
        return {"success": False, "error": "Shift not found"}, 404
    
    if isinstance(startTime, str) and isinstance(endTime, str):
        try:
            startTime = datetime.strptime(startTime, "%Y/%m/%d %H:%M")
            endTime = datetime.strptime(endTime, "%Y/%m/%d %H:%M")
        except ValueError:
            return {"success": False, "error": "Invalid time format. Please use (YYYY/MM/DD HH:MM)"}, 400
        
    try:
        shift.reschedule(startTime, endTime)
        db.session.add(shift)
        db.session.commit()
        return {
            "success": True, 
            "startTime": datetime.strptime(startTime, "%Y/%m/%d %H:%M"),
            "endTime": datetime.strptime(endTime, "%Y/%m/%d %H:%M")
        }, 201
        
    except Exception as e:
        return {"success": False, "error": "Internal server error"}, 500
    