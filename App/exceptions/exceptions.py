class NotFoundError(Exception):
    """Entity not found in database"""
    pass

class ValidationError(Exception):
    """Input data is invalid"""
    pass

class ConflictError(Exception):
    """Resource already exists or operation conflicts"""
    pass

class InternalError(Exception):
    """Unexpected server/database error"""
    pass