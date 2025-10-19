from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import ( 
    create_user, get_all_users_json, get_all_users, initialize, jwt_required, get_user_by_username,
    create_admin_user, scheduleShift, get_all_admins, get_all_admins_json, list_admins, get_admin, delete_admin,
    create_staff_user, timeShift, get_all_staff, get_all_staff_json, list_staff, get_staff, get_staff_by_name, list_staff_json, delete_staff,
    get_shift_info, is_shift_timed_in, pretty_print_shift_json, get_shift, reschedule_shift, delete_shift,
    generate_roster, generate_report_data, generate_report, get_report, get_all_reports, pretty_print_report_json, list_reports, delete_report)

admin_user_views = Blueprint('admin_user_views', __name__, template_folder='../templates')

@admin_user_views.route('/admin', methods=['GET'])
def list_admins_route():
    return jsonify(list_admins()), 200
    
@admin_user_views.route('/admin<int:id>', methods=['DELETE'])
def delete_admin_route(id):
    result, status = delete_admin(id)
    return jsonify(result), status

@admin_user_views.route('/admin/<int:id>', methods=['GET'])
def view_admin_route(id):
    admin = get_admin(id)
    if not admin:
        return jsonify({
            'error': "Not Found",
            'message': f'Admin with ID: {id} not found'
        }), 404

    data = admin.get_json()
    return jsonify({
        "staffID": data["id"],
        "username": data["name"],
        "shifts": data["shifts"]
    }), 200

        
@admin_user_views.route('/admin', methods=['POST'])
def create_admin_route():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({
            'error': "Bad Request",
            'message': "Username and password required"
        }), 400
        
    if get_user_by_username(username) is not None:
        return jsonify({
            'error': "Conflict",
            'message': "User already exists"
        }), 409
        
    admin = create_admin_user(username, password)
    return jsonify({
        'message': f'User successfully created. Username: {username}, ID: {admin.id}'
    }), 201

@admin_user_views.route("/shift", methods=['POST'])
def schedule_shift_route():
    data = request.json
    adminId = jwt_current_user #perhaps?
    staffId = data["staffId"]
    startTime = data["startTime"] #click.prompt("Enter the start time of the shift(YYYY/MM/DD HH:MM): ")
    endTime = data["endTime"] #click.prompt("Enter the end time of the shift(YYYY/MM/DD HH:MM): ")
    result, status = scheduleShift(staffId, adminId, startTime, endTime)
    return jsonify(result), status

@admin_user_views.route("/shift<int:id>", methods=['DELETE'])
def delete_shift_route(id):
    result, status = delete_shift(id)
    return jsonify(result), status
    
@admin_user_views.route("/shift/<int:id>", methods=["PATCH"])
def reschedule_shift_route(id):
    shift = get_shift(id)
    if not shift:
        return jsonify({
            'error': "Not Found",
            'message': f'Shift with ID: {id} not found'
        }), 404
    
    data = request.json
    startTime = data["startTime"] #click.prompt("Enter the new start time of the shift(YYYY/MM/DD HH:MM): ")
    endTime = data["endTime"] #click.prompt("Enter the new end time of the shift(YYYY/MM/DD HH:MM): ")
    result, status = reschedule_shift(id, startTime, endTime)
    return jsonify(result), status

@admin_user_views.route("/report", methods=["POST"])
def generate_report_route():
    report = generate_report()
    return jsonify(report), 200

@admin_user_views.route("/report", methods=["GET"])
def list_reports_route():
    reports = list_reports()
    return jsonify(reports), 200
    
@admin_user_views.route("/report/<int:id>", methods=["GET"])
def view_report_route(id):    
    report = get_report(id)
    if not report:
        return jsonify({
            'error': "Not Found",
            'message': f'Report with ID: {id} not found'
        }), 404

    return jsonify(report), 200

@admin_user_views.route("/report/<int:id>", methods=["DELETE"])
def delete_report_route(id):    
    result, status = delete_report(id)
    return jsonify(result), status

@admin_user_views.route("/staff/<int:id>", methods=["DELETE"])
def delete_staff_route(id):
    result, status = delete_staff(id)
    return jsonify(result), status


