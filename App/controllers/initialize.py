from .user import create_user
from .admin import create_admin_user, scheduleShift
from .staff import create_staff_user, timeShift
from App.database import db
from datetime import datetime

def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_staff_user('Tyler', 'tylerpass')
    create_staff_user('John', 'johnpass')
    create_admin_user('Jimmy', 'jimmypass')
    create_admin_user('Bobby', 'bobbypass')
    
    shift1 = scheduleShift(1, 1, "2025/09/15 08:00", "2025/09/15 09:00")
    shift2= scheduleShift(1, 1, "2025/09/16 10:00", "2025/09/16 12:00")
    
    shift3 = scheduleShift(2, 1, "2025/09/15 11:00", "2025/09/15 12:00")
    shift4 = scheduleShift(2, 2, "2025/09/16 16:00", "2025/09/16 17:00")
    shift5 = scheduleShift(2, 1, "2025/09/17 17:00", "2025/09/17 18:00")
    shift6 = scheduleShift(2, 2, "2025/09/18 20:00", "2025/09/18 21:00")
    
    timeShift(1, "in", datetime.strptime("2025/09/15 08:01", "%Y/%m/%d %H:%M"))
    timeShift(1, "out", datetime.strptime("2025/09/15 08:55", "%Y/%m/%d %H:%M"))
    
    timeShift(2, "in", datetime.strptime("2025/09/16 10:11", "%Y/%m/%d %H:%M"))
    timeShift(2, "out", datetime.strptime("2025/09/16 11:55", "%Y/%m/%d %H:%M"))
    
    timeShift(3, "in", datetime.strptime("2025/09/15 11:01", "%Y/%m/%d %H:%M"))
    timeShift(3, "out", datetime.strptime("2025/09/15 11:30", "%Y/%m/%d %H:%M"))

    # Shift 4 absent
    
    timeShift(5, "in", datetime.strptime("2025/09/17 17:01", "%Y/%m/%d %H:%M"))
    timeShift(5, "out", datetime.strptime("2025/09/17 17:59", "%Y/%m/%d %H:%M"))
    
    timeShift(6, "in", datetime.strptime("2025/09/18 20:20", "%Y/%m/%d %H:%M"))
    timeShift(6, "out", datetime.strptime("2025/09/18 20:58", "%Y/%m/%d %H:%M"))
    
    
