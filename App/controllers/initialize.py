from .user import create_user
from .admin import create_admin_user, scheduleShift
from .staff import create_staff_user
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_staff_user('staff1', 'staff1pass')
    create_staff_user('staff2', 'staff2pass')
    create_admin_user('admin1', 'admin1pass')
    create_admin_user('admin2', 'admin2pass')
    
    scheduleShift(1, 1, "2025-09-10 08:00", "2025-09-10 09:00")
    scheduleShift(1, 1, "2025-09-11 10:00", "2025-09-11 12:00")
    
