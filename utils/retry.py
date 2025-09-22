from tenacity import retry, stop_after_attempt, wait_fixed
from sqlalchemy.orm import Session
from models.models import ActivityPeriod

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_activity_period_with_retry(session: Session, activity_id: int):
    return session.query(ActivityPeriod).filter_by(id=activity_id).first()