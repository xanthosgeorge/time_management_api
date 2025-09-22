from utils.retry import get_activity_period_with_retry
from models.models import ActivityPeriod
from sqlalchemy.orm import Session

class DummySession:
    def __init__(self):
        self.attempts = 0

    def query(self, model):
        return self

    def filter_by(self, id):
        self.attempts += 1
        print(f"Attempt {self.attempts}")
        if self.attempts < 3:
            raise Exception("Simulated failure")
        return self

    def first(self):
        return ActivityPeriod(id=1, start_time="2025-09-22 10:00:00", end_time="2025-09-22 11:00:00", status="Reading")

if __name__ == "__main__":
    session = DummySession()
    result = get_activity_period_with_retry(session, 1)
    print("Result:", result)