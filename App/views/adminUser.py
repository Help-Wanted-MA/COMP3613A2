from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user as jwt_current_user
from datetime import datetime
from.index import index_views

from App.exceptions.handlers import register_error_handlers
from App.controllers import ( 
    create_user, get_all_users_json, get_all_users, initialize, jwt_required, get_user_by_username, role_required, 
    create_admin_user, scheduleShift, get_all_admins, get_all_admins_json, list_admins, list_admins_json, get_admin, delete_admin,
    create_staff_user, timeShift, get_all_staff, get_all_staff_json, list_staff, get_staff, get_staff_by_name, list_staff_json, delete_staff,
    get_shift_info, is_shift_timed_in, pretty_print_shift_json, get_shift, reschedule_shift, delete_shift,
    generate_roster, generate_report_data, generate_report, get_report, get_all_reports, pretty_print_report_json, list_reports, delete_report)

admin_user_views = Blueprint('admin_user_views', __name__, template_folder='../templates')
register_error_handlers(admin_user_views)

@admin_user_views.route('/admin', methods=['GET'])
@role_required("admin")
def list_admins_route():
    adminList = list_admins_json()
    return jsonify(adminList), 200
    
@admin_user_views.route('/admin<int:id>', methods=['DELETE'])
@role_required("admin")
def delete_admin_route(id):
    delete_admin(id)
    return jsonify({
        'success': 'True',
        'message': 'Admin successfully deleted'
    }), 204

@admin_user_views.route('/admin/<int:id>', methods=['GET'])
@role_required("admin")
def view_admin_route(id):
    admin = get_admin(id)
    data = admin.get_json()
    return jsonify({
        "staffID": data["id"],
        "username": data["name"],
        "shifts": data["shifts"]
    }), 200

@admin_user_views.route('/admin', methods=['POST'])
@role_required("admin")
def create_admin_route():
    data = request.json
    username = data.get('username')
    password = data.get('password')     
    admin = create_admin_user(username, password)
    
    return jsonify({
        'message': f'User successfully created. Username: {username}, ID: {admin.id}'
    }), 201

@admin_user_views.route("/shift", methods=['POST'])
@role_required("admin")
def schedule_shift_route():
    data = request.json
    adminId = int(get_jwt_identity())
    staffId = data["staffId"]
    startTime = data["startTime"] #click.prompt("Enter the start time of the shift(YYYY/MM/DD HH:MM): ")
    endTime = data["endTime"] #click.prompt("Enter the end time of the shift(YYYY/MM/DD HH:MM): ")
    newShift = scheduleShift(staffId, adminId, startTime, endTime)
    return {
        "success": True,
        "staffId": newShift.staffId,
        "adminId": newShift.adminId,
        "shiftId": newShift.id,
        "startTime": datetime.strftime(startTime, "%Y/%m/%d %H:%M"),
        "endTime": datetime.strftime(endTime, "%Y/%m/%d %H:%M"),   
    }, 201

@admin_user_views.route("/shift<int:id>", methods=['DELETE'])
@role_required("admin")
def delete_shift_route(id):
    delete_shift(id)
    return jsonify({
        'success': 'True',
        'message': 'Shift successfully deleted'
    }), 204

@admin_user_views.route("/report", methods=["POST"])
@role_required("admin")
def generate_report_route():
    report = generate_report()
    return jsonify(report), 200

@admin_user_views.route("/report", methods=["GET"])
@role_required("admin")
def list_reports_route():
    reports = list_reports()
    return jsonify(reports), 200
    
@admin_user_views.route("/report/<int:id>", methods=["GET"])
@role_required("admin")
def view_report_route(id):    
    report = get_report(id)
    return jsonify(report), 200

@admin_user_views.route("/report/<int:id>", methods=["DELETE"])
@role_required("admin")
def delete_report_route(id):    
    delete_report(id)
    return jsonify({
        'success': 'True',
        'message': 'Report successfully deleted'
    }), 204

@admin_user_views.route("/staff/<int:id>", methods=["DELETE"])
@role_required("admin")
def delete_staff_route(id):
    delete_staff(id)
    return jsonify({
        'success': 'True',
        'message': 'Staff successfully deleted'
    }), 204


