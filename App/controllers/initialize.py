from .user import create_user
from .admin import create_admin_user, schedule_shift
from .staff import create_staff_user, time_shift
from App.database import db
from datetime import datetime, timedelta

def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_staff_user('Tyler', 'tylerpass')
    create_staff_user('John', 'johnpass')
    create_admin_user('Jimmy', 'jimmypass')
    create_admin_user('Bobby', 'bobbypass')
    
    # Dynamically allocate some shifts for the current real world week, and time in/out a few.
    weekStart = datetime.now().date() - timedelta(days=datetime.now().date().weekday())
    
    #schedule_shift(StaffID, AdminID, StartTime, EndTime)
    shift1 = schedule_shift(1, 1, 
                datetime.combine(weekStart, datetime.strptime("08:00", "%H:%M").time()),
                datetime.combine(weekStart, datetime.strptime("09:00", "%H:%M").time())
            )
    
    shift2= schedule_shift(1, 1, 
                datetime.combine(weekStart + timedelta(days=1), datetime.strptime("10:00", "%H:%M").time()),
                datetime.combine(weekStart + timedelta(days=1), datetime.strptime("12:00", "%H:%M").time())
            )
    
    shift3 = schedule_shift(2, 1, 
                datetime.combine(weekStart, datetime.strptime("11:00", "%H:%M").time()),
                datetime.combine(weekStart, datetime.strptime("12:00", "%H:%M").time())
            )
    
    shift4 = schedule_shift(2, 2, 
                datetime.combine(weekStart + timedelta(days=1), datetime.strptime("16:00", "%H:%M").time()),
                datetime.combine(weekStart + timedelta(days=1), datetime.strptime("17:00", "%H:%M").time())
            )
    
    shift5 = schedule_shift(2, 1, 
                datetime.combine(weekStart + timedelta(days=2), datetime.strptime("17:00", "%H:%M").time()),
                datetime.combine(weekStart + timedelta(days=2), datetime.strptime("18:00", "%H:%M").time())
            )
    
    shift6 = schedule_shift(2, 2, 
            datetime.combine(weekStart + timedelta(days=3), datetime.strptime("20:00", "%H:%M").time()),
            datetime.combine(weekStart + timedelta(days=3), datetime.strptime("21:00", "%H:%M").time())
            )
    
    shift7 = schedule_shift(2, 2, "2025/10/07 10:00", "2025/10/07 12:00")
    shift8 = schedule_shift(2, 1, "2025/10/09 10:00", "2025/09/09 12:00")
    
    #time_shift(1, "in", datetime.combine(weekStart, datetime.strptime("08:01", "%H:%M").time()))
    #time_shift(1, "out", datetime.combine(weekStart, datetime.strptime("08:55", "%H:%M").time()))

    time_shift(2, "in", datetime.combine(weekStart + timedelta(days=1), datetime.strptime("10:11", "%H:%M").time()))
    time_shift(2, "out", datetime.combine(weekStart + timedelta(days=1), datetime.strptime("11:55", "%H:%M").time()))

    time_shift(3, "in", datetime.combine(weekStart, datetime.strptime("11:01", "%H:%M").time()))
    time_shift(3, "out", datetime.combine(weekStart, datetime.strptime("11:30", "%H:%M").time()))

    # shift4 absent

    time_shift(5, "in", datetime.combine(weekStart + timedelta(days=2), datetime.strptime("17:01", "%H:%M").time()))
    time_shift(5, "out", datetime.combine(weekStart + timedelta(days=2), datetime.strptime("17:59", "%H:%M").time()))

    time_shift(6, "in", datetime.combine(weekStart + timedelta(days=3), datetime.strptime("20:20", "%H:%M").time()))
    time_shift(6, "out", datetime.combine(weekStart + timedelta(days=3), datetime.strptime("20:58", "%H:%M").time()))
    
    
