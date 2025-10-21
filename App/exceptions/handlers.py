from flask import jsonify
from App.exceptions.exceptions import NotFoundError, ValidationError, ConflictError, InternalError

def register_error_handlers(blueprint):
    @blueprint.errorhandler(NotFoundError)
    def handle_not_found(e):
        return jsonify({"success": False, "error": str(e)}), 404

    @blueprint.errorhandler(ValidationError)
    def handle_validation(e):
        return jsonify({"success": False, "error": str(e)}), 400

    @blueprint.errorhandler(ConflictError)
    def handle_conflict(e):
        return jsonify({"success": False, "error": str(e)}), 409

    @blueprint.errorhandler(InternalError)
    def handle_internal(e):
        return jsonify({"success": False, "error": "Internal server error"}), 500
