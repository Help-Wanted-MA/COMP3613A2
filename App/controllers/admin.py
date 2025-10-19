from App.models import Admin, Staff, Shift
from App.database import db
from datetime import datetime

def create_admin_user(name, password):
    newadmin = Admin(name=name, password=password)
    db.session.add(newadmin)
    db.session.commit()
    return newadmin

def scheduleShift(staffId, adminId, startTime, endTime):
    staffUser = Staff.query.get(staffId)
    if not staffUser:
        return {"success": False, "error": "Staff user not found"}, 404
    
    if isinstance(startTime, str) and isinstance(endTime, str):
        try:
            startTime = datetime.strptime(startTime, "%Y/%m/%d %H:%M")
            endTime = datetime.strptime(endTime, "%Y/%m/%d %H:%M")
        except ValueError:
            return {"success": False, "error": "Invalid time format. Please use (YYYY/MM/DD HH:MM)"}, 400
    
    newShift = Shift(staffId=staffId, adminId=adminId, startTime=startTime, endTime=endTime)
    if not newShift:
        return {"success": False, "error": "Error creating new shift"}, 500
    
    db.session.add(newShift)
    db.session.commit()
    return {
        "success": True,
        "staffId": newShift.staffId,
        "adminId": newShift.adminId,
        "shiftId": newShift.id,
        "startTime": datetime.strptime(startTime, "%Y/%m/%d %H:%M"),
        "endTime": datetime.strptime(endTime, "%Y/%m/%d %H:%M"),   
    }, 201
    
    

def list_admins():
    allAdmins = Admin.query.all()
    str = ""
    for admin in allAdmins:
        str += f'ID: {admin.id}, Name: {admin.name}\n'
        
    return str

def get_admin_by_name(name):
    result = db.session.execute(db.select(Admin).filter_by(name=name))
    return result.scalar_one_or_none()

def get_admin(id):
    return db.session.get(Admin, id)

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
    if not admin: return {"error": f"Admin with ID:{id} not found"}, 404
    db.session.delete(admin)
    db.session.commit()
    return {"success": f"Admin with ID:{id} successfully deleted"}, 204
