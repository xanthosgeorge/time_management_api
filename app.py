from flask import Flask, request, jsonify
from db import Base, SessionLocal, engine
from datetime import datetime

from models.models import ActivityPeriod,Base

app = Flask(__name__)
Base.metadata.create_all(bind=engine)

@app.route('/activity', methods=['POST'])
def log_activity():
    data = request.get_json()
    start_time = datetime.fromisoformat(data['start_time'])
    end_time = datetime.fromisoformat(data['end_time'])
    status = data['status']

    db = SessionLocal()
    activity = ActivityPeriod(start_time=start_time, end_time=end_time, status=status)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    db.close()
    
    return jsonify({
        "id": activity.id,
        "start_time": activity.start_time.isoformat(),
        "end_time": activity.end_time.isoformat(),
        "status": activity.status
    })

@app.route('/activity', methods=['GET'])
def get_all_activity():
    db = SessionLocal()
    activities = db.query(ActivityPeriod).all()
    db.close()
    return jsonify([
        {
            "id": a.id,
            "start_time": a.start_time.isoformat(),
            "end_time": a.end_time.isoformat(),
            "status": a.status
        } for a in activities
    ])

if __name__ == '__main__':
    app.run(debug=True)