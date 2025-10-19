from App.models import Admin, Staff, Shift
from App.database import db
from App.exceptions.exceptions import NotFoundError, ConflictError, InternalError, ValidationError
from datetime import datetime

def create_admin_user(username, password):
    if not username or not password:
        raise ValidationError("Username or password missing")
        
    if get_admin_by_name(username) is not None:
        raise ConflictError("User already exists")
        
    newadmin = Admin(name=username, password=password)
    db.session.add(newadmin)
    db.session.commit()
    return newadmin

def scheduleShift(staffId, adminId, startTime, endTime):
    if not staffId or not adminId or not startTime or not endTime:
        raise ValidationError("Required field missing")
    
    staffUser = Staff.query.get(staffId)
    if not staffUser:
        raise NotFoundError("Staff user not found")
    
    if isinstance(startTime, str) and isinstance(endTime, str):
        try:
            startTime = datetime.strptime(startTime, "%Y/%m/%d %H:%M")
            endTime = datetime.strptime(endTime, "%Y/%m/%d %H:%M")
        except ValueError:
            raise ValidationError("Invalid time format. Please use (YYYY/MM/DD HH:MM)")
    
    newShift = Shift(staffId=staffId, adminId=adminId, startTime=startTime, endTime=endTime)
    if not newShift:
        raise InternalError
    
    db.session.add(newShift)
    db.session.commit()
    return newShift

def list_admins():
    allAdmins = Admin.query.all()
    str = ""
    for admin in allAdmins:
        str += f'ID: {admin.id}, Name: {admin.name}\n'
        
    return str

def list_admins_json():
    allAdmins = Admin.query.all()
    adminList = []
    for admin in allAdmins:
        adminList.append({
            "id": admin.id,
            "name": admin.name
        })
    return adminList

def get_admin_by_name(name):
    result = db.session.execute(db.select(Admin).filter_by(name=name))
    return result.scalar_one_or_none()

def get_admin(id):
    admin = db.session.get(Admin, id)
    if not admin:
        raise NotFoundError(f'Admin with ID: {id} not found')
    return admin

def get_all_admins():
    return db.session.scalars(db.select(Admin)).all()

def get_all_admins_json():
    adminUsers = get_all_admins()
    if not adminUsers:
        return []
    adminUsers = [admin.get_json() for admin in adminUsers]
    return adminUsers

def delete_admin(id):
    admin = Admin.query.get(id)
    if not admin: 
        raise NotFoundError(f"Admin with ID: {id} not found")
    
    try:
        db.session.delete(admin)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        raise InternalError
