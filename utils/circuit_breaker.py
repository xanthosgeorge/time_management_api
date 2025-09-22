import logging
import pybreaker
from sqlalchemy.orm import Session
from models.models import User

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Custom exception for user not found
class UserNotFoundException(Exception):
    pass

# Hook to determine when to trip the breaker
def should_trip_cb(exception):
    logger.warning(f"Trip hook triggered by exception: {exception}")
    return isinstance(exception, UserNotFoundException)

# Singleton circuit breaker instance
breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=60,
    should_trip_hook=should_trip_cb
)

# Internal function to get user from DB
def _get_user(session: Session, user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        raise UserNotFoundException(f"User with ID {user_id} not found")
    return user

# Public function with circuit breaker protection
def get_user_with_circuit_breaker(session: Session, user_id: int):
    if breaker.current_state == pybreaker.STATE_OPEN:
        logger.error("Circuit breaker is OPEN. Request blocked.")
        raise Exception("Circuit breaker is open. Try again later.")
    try:
        return breaker.call(_get_user, session, user_id)
    except pybreaker.CircuitBreakerError as cb_err:
        logger.error(f"Circuit breaker error: {cb_err}")
        raise
    except Exception as e:
        logger.error(f"Error during user lookup: {e}")
        raise
