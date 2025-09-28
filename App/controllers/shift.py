from App.models import Shift
from App.database import db
from datetime import datetime

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
    if not shift: return None
    db.session.delete(shift)
    db.session.commit()
    
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
        return False
    
    if isinstance(startTime, str) and isinstance(endTime, str):
        try:
            startTime = datetime.strptime(startTime, "%Y/%m/%d %H:%M")
            endTime = datetime.strptime(endTime, "%Y/%m/%d %H:%M")
        except ValueError:
            print("Invalid time format. Please use (YYYY/MM/DD HH:MM)")
            return False
        
    try:
        shift.reschedule(startTime, endTime)
        db.session.add(shift)
        db.session.commit()
        return True
    except Exception as e:
        print(f'Error rescheduling shift: Database error - {e}')
        return False
    