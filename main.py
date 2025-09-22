import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pybreaker import CircuitBreakerError
import logging
from datetime import datetime, timedelta

from db import get_db, Base, engine
from utils.circuit_breaker import get_user_with_circuit_breaker, breaker
from utils.retry import get_activity_period_with_retry
from models.models import User, ActivityPeriod

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Serve static files (e.g., HTML, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/user/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Breaker state: {breaker.current_state}")
    try:
        user = get_user_with_circuit_breaker(db, user_id)
        return user
    except CircuitBreakerError:
        raise HTTPException(status_code=503, detail="Service temporarily unavailable (circuit breaker open)")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/activity/{activity_id}")
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    try:
        activity = get_activity_period_with_retry(db, activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        return activity
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def seed_data():
    db = Session(bind=engine)
    if not db.query(User).first():
        user = User(username="testuser", hashed_password="testpass")
        db.add(user)
    if not db.query(ActivityPeriod).first():
       now = datetime.now()
       period = ActivityPeriod(
       start_time=now,
       end_time=now + timedelta(hours=1),
       status="Reading")
    
    db.add(period)
    db.commit()
    db.close()

def clear_db():
    db = Session(bind=engine)
    db.query(User).delete()
    db.query(ActivityPeriod).delete()
    db.commit()
    db.close()

# Initialize database with sample data
clear_db()
seed_data()
