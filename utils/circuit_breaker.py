import pybreaker
from sqlalchemy.orm import Session
from models.models import User

breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)

def get_user_with_circuit_breaker(session: Session, user_id: int):
    @breaker
    def _get():
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            # Raise exception inside breaker so it counts as a failure
            raise Exception("User not found")
        return user
    return _get()