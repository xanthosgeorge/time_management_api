from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from db import get_db
from utils.circuit_breaker import get_user_with_circuit_breaker
from utils.retry import get_activity_period_with_retry

app = FastAPI()

# Serve files from the 'static' directory at /static
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/activity/{activity_id}")
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = get_activity_period_with_retry(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@app.get("/user/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_with_circuit_breaker(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user