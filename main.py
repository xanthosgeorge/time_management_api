from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pybreaker import CircuitBreakerError

from db import get_db, Base, engine
from utils.circuit_breaker import get_user_with_circuit_breaker
from utils.retry import get_activity_period_with_retry
from models.models import User, ActivityPeriod

clear_db()

app = FastAPI()

# Serve files from the 'static' directory at /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create the database tables
Base.metadata.create_all(bind=engine)


@app.get("/activity/{activity_id}")
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = get_activity_period_with_retry(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@app.get("/user/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = get_user_with_circuit_breaker(db, user_id)
        if not user:
            # Simulate a failure for the breaker
            raise Exception("User not found")
        return user
    except CircuitBreakerError:
        raise HTTPException(status_code=503, detail="Service temporarily unavailable (circuit breaker open)")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


def seed_data():
    db = Session(bind=engine)
    # Add a test user if none exists
    if not db.query(User).first():
        user = User(username="testuser", hashed_password="testpass")
        db.add(user)
    # Add a test activity if none exists
    if not db.query(ActivityPeriod).first():
        activity = ActivityPeriod(
            start_time="2025-09-22 10:00:00",
            end_time="2025-09-22 11:00:00",
            status="Reading",
        )
        db.add(activity)
    db.commit()
    db.close()

seed_data()

def clear_db():
    db = Session(bind=engine)
    db.query(User).delete()
    db.query(ActivityPeriod).delete()
    db.commit()
    db.close()
