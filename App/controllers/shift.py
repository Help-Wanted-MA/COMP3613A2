from App.models import Shift
from App.database import db
from datetime import datetime
from App.exceptions.exceptions import ConflictError, InternalError, NotFoundError, ValidationError

def is_shift_timed_in(id):
    shift = Shift.query.get(id)
    if not shift:
        raise NotFoundError(f"Shift not found with ID: {id}")
    
    if shift.timedIn and not shift.timedOut: # A timedIn time with no timedOut time means a staff member has started the shift
        return True
    else:
        return False
    
def delete_shift(id):
    shift = Shift.query.get(id)
    if not shift: 
        raise NotFoundError(f"Shift not found with ID: {id}")
    
    try:
        db.session.delete(shift)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        raise InternalError

def get_shift(id):
    shift = db.session.get(Shift, id)
    if not shift:
        raise NotFoundError(f"Shift not found with ID: {id}")
    return shift
    