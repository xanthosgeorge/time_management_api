from functools import wraps
from flask import Flask, request, jsonify
from db import Base, SessionLocal, engine
from datetime import datetime
import bcrypt
import jwt



from models.models import ActivityPeriod,Base, User

app = Flask(__name__)
Base.metadata.create_all(bind=engine)

SECRET_KEY = "7e7241d23cc430ff7783018e384fc97078f00db9ed9beb35588ccaaf5c36e57b"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error": "Token is missing"}), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(user_id=user_id, *args, **kwargs)
    return decorated

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
def get_all_activities():
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


@app.route('/activity/<int:id>', methods=['GET'])
def get_activity(id):
    db = SessionLocal()
    activity = db.query(ActivityPeriod).filter(ActivityPeriod.id == id).first()
    db.close()
    
    if activity:
        return jsonify({
            "id": activity.id,
            "start_time": activity.start_time.isoformat(),
            "end_time": activity.end_time.isoformat(),
            "status": activity.status
        })
    else:
        return jsonify({"error": "Activity not found"}), 404
    

@app.route('/activity/<int:id>', methods=['DELETE'])
def delete_activity(id):
    db = SessionLocal()
    activity = db.query(ActivityPeriod).filter(ActivityPeriod.id == id).first()
    
    if activity:
        db.delete(activity)
        db.commit()
        db.close()
        return jsonify({"message": "Activity deleted successfully"})
    else:
        db.close()
        return jsonify({"error": "Activity not found"}), 404   



@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    db = SessionLocal()
    user = User(username=username, hashed_password=hashed_password.decode('utf-8'))
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return jsonify({"id": user.id, "username": user.username}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    db = SessionLocal()
    user = db.query(User).filter_by(username=username).first()
    db.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow().timestamp() + 3600  # Token valid for 1 hour
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    




if __name__ == '__main__':
    app.run(debug=True)