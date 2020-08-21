from flask import Flask, request
from db import db, InfoSession, Position, Club, Student
import json

# Define db filename
db_filename = "data.db"
app = Flask(__name__)

# Setup config
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# Initialize app
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/api/position/", methods=["POST"])
def create_position():
    body = json.loads(request.data)
    name = body['name']
    link = body['link']
    deadline = body['deadline']
    club_id = body['club_id']

    position = Position(
        name=name,
        link=link,
        deadline=deadline,
        club_id=club_id,
    )
    db.session.add(position)
    db.session.commit()

    return json.dumps({"Success": True, "data": position.serialize()}), 201


@app.route("/api/position/<int:position_id>", methods=["POST"])
def delete_position(position_id):
    position = Position.query.filter_by(id=position_id).first()
    if position is not None:
        db.session.delete(position)
        db.session.commit()
        return json.dumps({"Success": True, "data": position.serialize()}), 201
    else:
        return json.dumps({"Success": False, "data": "position_id doesn't exist"}), 400


@app.route("/api/info_session/", methods=["POST"])
def create_info_session():
    body = json.loads(request.data)
    name = body['name']
    time = body['time']
    location = body['location']
    club_id = body['club_id']

    info_session = InfoSession(
        name=name,
        time=time,
        location=location,
        club_id=club_id,
    )
    db.session.add(info_session)
    db.session.commit()

    return json.dumps({"Success": True, "data": info_session.serialize()}), 201


@app.route("/api/info_session/<int:info_session_id>", methods=["POST"])
def delete_info_session(info_session_id):
    info_session = InfoSession.query.filter_by(id=info_session_id).first()
    if info_session is not None:
        db.session.delete(info_session)
        db.session.commit()
        return json.dumps({"Success": True, "data": info_session.serialize()}), 201
    else:
        return json.dumps({"Success": False, "data": "info_session_id doesn't exist"}), 400


@app.route("/api/club/", methods=["POST"])
def create_club():
    body = json.loads(request.data)
    name = body['name']
    website = body['website']
    image = body['image']
    portal = body['portal']
    status = body['status']

    club = Club(
        name=name,
        website=website,
        image=image,
        portal=portal,
        status=status,
    )
    db.session.add(club)
    db.session.commit()

    return json.dumps({"Success": True, "data": club.serialize()}), 201
    

@app.route("/api/club/<int:club_id>", methods=["POST"])
def delete_club(club_id):
    club = Club.query.filter_by(id=club_id).first()
    if club is not None:
        db.session.delete(club)
        db.session.commit()
        return json.dumps({"Success": True, "data": club.serialize()}), 201
    else:
        return json.dumps({"Success": False, "data": "club_id doesn't exist"}), 400


# Called by frontend
@app.route("/api/clubs/", methods=["GET"])
def get_all_clubs():
    return json.dumps({'Success': True, 'data': [c.serialize() for c in Club.query.all()]}), 200


# Called by frontend
@app.route("/api/user/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    email = body["email"]
    club_ids = body["club_ids"]

    user = User(
        email=email
    )

    existing_user = User.query.filter_by(email=email).first()
    if existing_user is not None:
        db.session.delete(existing_user)
    for id in club_ids:
        club = Club.query.filter_by(id=id).first()
        user.club_list.append(club)
    db.session.add(user)
    db.session.commit()

    return json.dumps({"Success": True, "data": user.serialize()}), 201

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)