from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.exceptions.handlers import register_error_handlers
from App.controllers import ( 
    role_required, timeShift, generate_roster
)

staff_user_views = Blueprint('staff_user_views', __name__, template_folder='../templates')
register_error_handlers(staff_user_views)
     
@staff_user_views.route('/staff/roster', methods=['GET'])
@jwt_required()
def view_roster_route():
    referenceDate = request.args.get("referenceDate")
    roster = generate_roster(referenceDate)
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
