from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.exceptions.handlers import register_error_handlers
from App.controllers import ( 
    create_user, get_all_users_json, get_all_users, initialize, jwt_required, role_required,
    create_admin_user, scheduleShift, get_all_admins, get_all_admins_json, list_admins, get_admin,
    create_staff_user, timeShift, get_all_staff, get_all_staff_json, list_staff, get_staff, get_staff_by_name, list_staff_json,
    get_shift_info, is_shift_timed_in, pretty_print_shift_json, get_shift, reschedule_shift,
    generate_roster, generate_report_data, generate_report, get_report, get_all_reports, pretty_print_report_json, list_reports)

staff_user_views = Blueprint('staff_user_views', __name__, template_folder='../templates')
register_error_handlers(staff_user_views)

@staff_user_views.route('/staff', methods=['POST'])
@role_required("staff")
def create_staff_route():
    data = request.json
    username = data.get('username')
    password = data.get('password')
        
    staff = create_staff_user(username, password)
    return jsonify({
        'message': f'User successfully created. Username: {username}, ID: {staff.id}'
    }), 201

@staff_user_views.route('/staff', methods=['GET'])
@role_required("staff")
def view_staff_list_route():
    staffList = list_staff_json()
    jsonify(staffList), 200
        
@staff_user_views.route('/staff/<int:id>', methods=['GET'])
@role_required("staff")
def view_staff_route(id):
    staff = get_staff(id)
    data = staff.get_json()
        
    return jsonify({
        "staffID": data["id"],
        "username": data["name"],
        "shifts": data["shifts"]
    }), 200
     
@staff_user_views.route('/staff/roster', methods=['GET'])
@role_required("staff")
def view_roster_route(week):
    week = request.args.get("week")
    roster = generate_roster(week) #must implement
    return jsonify(roster), 200    
        
@staff_user_views.route('/shift/<int:id>', methods=["PATCH"])
@role_required("staff")
def time_shift_command(id):
    type = request.args.get("type")
    shift = timeShift(id, type)
    return jsonify({
        "success": True,
        "shift_id": shift.id,
        "type": type,
        "time": shift.timedIn.isoformat() if type == "in" else shift.timedOut.isoformat(),
        "attendance": shift.attendance
    }), 200
