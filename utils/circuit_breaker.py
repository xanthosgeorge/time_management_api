import pybreaker
from sqlalchemy.orm import Session
from models.models import User

# Custom exception to track user lookup failures
class UserNotFoundException(Exception):
    pass

# Circuit breaker configuration
breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=60,
    expected_exception=UserNotFoundException
)

def get_user_with_circuit_breaker(session: Session, user_id: int):
    @breaker
    def _get():
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise UserNotFoundException("User not found")
        return user
    return _get()
