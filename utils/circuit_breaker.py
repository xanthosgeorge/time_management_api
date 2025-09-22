import logging
import pybreaker
from sqlalchemy.orm import Session
from models.models import User

logger = logging.getLogger(__name__)

class UserNotFoundException(Exception):
    pass

# Custom subclass to override trip logic
class CustomCircuitBreaker(pybreaker.CircuitBreaker):
    def should_trip(self, exc):
        logger.warning(f"Trip check triggered by: {exc}")
        return isinstance(exc, UserNotFoundException)

# Singleton breaker instance
breaker = CustomCircuitBreaker(fail_max=5, reset_timeout=60)

def _get_user(session: Session, user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        raise UserNotFoundException(f"User with ID {user_id} not found")
    return user

def get_user_with_circuit_breaker(session: Session, user_id: int):
    return breaker.call(_get_user, session, user_id)
