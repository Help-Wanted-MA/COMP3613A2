from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import ( 
    create_user, get_all_users_json, get_all_users, initialize, jwt_required,
    create_admin_user, scheduleShift, get_all_admins, get_all_admins_json, list_admins, get_admin,
    create_staff_user, timeShift, get_all_staff, get_all_staff_json, list_staff, get_staff, get_staff_by_name, list_staff_json,
    get_shift_info, is_shift_timed_in, pretty_print_shift_json, get_shift, reschedule_shift,
    generate_roster, generate_report_data, generate_report, get_report, get_all_reports, pretty_print_report_json, list_reports)

staffUser_views = Blueprint('staffUser_views', __name__, template_folder='../templates')

@staffUser_views.route('/staff', methods=['POST'])
def create_staff_route():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({
            'error': "Bad Request",
            'message': "Username and password required"
        }), 400
        
    if get_staff_by_name(username) is not None:
        return jsonify({
            'error': "Conflict",
            'message': "User already exists"
        }), 409
        
    staff = create_staff_user(username, password)
    return jsonify({
        'message': f'User successfully created. Username: {username}, ID: {staff.id}'
    }), 201

@staffUser_views.route('/staff', methods=['GET'])
def view_staff_list_route():
    jsonify(list_staff_json()), 200
        
@staffUser_views.route('/staff/<int:id>', methods=['GET'])
def view_staff_route(id):
    staff = get_staff(id)
    if not staff:
        return jsonify({
            'error': "Not Found",
            'message': f'User with ID: {id} not found'
        }), 404

    data = staff.get_json()
        
    return jsonify({
        "staffID": data["id"],
        "username": data["name"],
        "shifts": data["shifts"]
    }), 200
     
@staffUser_views.route('/staff/roster', methods=['GET'])
def view_roster_route(week):
    week = request.args.get("week")
    roster = generate_roster(week) #must implement
    return jsonify(roster), 200    
        
@staffUser_views.route('/shift/<int:id>', methods=["PATCH"])
def time_shift_command(id):
    type = request.args.get("type")
    result, status = timeShift(id, type)
    return jsonify(result), status
