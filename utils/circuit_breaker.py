import pybreaker
from sqlalchemy.orm import Session
from models.models import User

class UserNotFoundException(Exception):
    pass

def should_trip_cb(exception):
    return isinstance(exception, UserNotFoundException)

breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=60,
    should_trip=should_trip_cb
)

def get_user_with_circuit_breaker(session: Session, user_id: int):
    @breaker
    def _get():
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise UserNotFoundException("User not found")
        return user
    return _get()
