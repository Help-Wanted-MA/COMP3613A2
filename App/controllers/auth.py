from functools import wraps
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

from App.models import User, Admin, Staff
from App.database import db

def login(username, password):
  # Try Admin first
  admin = db.session.execute(db.select(Admin).filter_by(name=username)).scalar_one_or_none()
  if admin and admin.check_password(password):
    return create_access_token(identity=str(admin.id), additional_claims={"user_type": "admin"})
  
  # Try Staff
  staff = db.session.execute(db.select(Staff).filter_by(name=username)).scalar_one_or_none()
  if staff and staff.check_password(password):
    return create_access_token(identity=str(staff.id), additional_claims={"user_type": "staff"})
  
  return None


def setup_jwt(app):
  jwt = JWTManager(app)

  # Always store a string user id in the JWT identity (sub),
  # whether a User object or a raw id is passed.
  @jwt.user_identity_loader
  def user_identity_lookup(identity):
    user_id = getattr(identity, "id", identity)
    return str(user_id) if user_id is not None else None

  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user_type = jwt_data.get("user_type")
    # Cast back to int primary key
    try:
      user_id = int(identity)
    except (TypeError, ValueError):
      return None
    
    if user_type == "admin":
      return db.session.get(Admin, user_id)
    elif user_type == "staff":
      return db.session.get(Staff, user_id)
    return None

  return jwt

def role_required(role):
  def wrapper(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
      # Ensure JWT is present
      verify_jwt_in_request()
      claims = get_jwt()
      user_type = claims.get("user_type")
      
      if user_type != role:
        return jsonify({"success": False, "error": f"{role.capitalize()} role required"}), 403
      
      return fn(*args, **kwargs)
    return decorated
  return wrapper
  
# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
          verify_jwt_in_request()
          identity = get_jwt_identity()
          claims = get_jwt()
          user_type = claims.get("user_type")
          user_id = int(identity) if identity is not None else None
          if user_id is not None:
                if user_type == "admin":
                    current_user = db.session.get(Admin, user_id)
                elif user_type == "staff":
                    current_user = db.session.get(Staff, user_id)
                    
          is_authenticated = current_user is not None
      except Exception as e:
          print(e)
          is_authenticated = False
          current_user = None
      return dict(is_authenticated=is_authenticated, current_user=current_user)