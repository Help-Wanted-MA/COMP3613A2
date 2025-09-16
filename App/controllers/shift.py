from App.models import Admin, Staff, Shift
from App.database import db

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
