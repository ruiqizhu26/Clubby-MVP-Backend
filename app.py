from flask import Flask, Response, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import smtplib
import json

from db import db, InfoSession, Position, Club, Student


# Define db filename
db_filename = "data.db"
app = Flask(__name__)
CORS(app)

# Setup config
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# Initialize app
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/api/info_session/", methods=["POST"])
def create_info_session():
    body = json.loads(request.data)
    name = body['name']
    time = body['time']
    location = body['location']
    club_id = body['club_id']

    club = Club.query.filter_by(id=club_id).first()
    if club is not None:
        info_session = InfoSession(
            name=name,
            time=time,
            location=location,
            club_id=club_id,
        )
        db.session.add(info_session)
        db.session.commit()
        return json.dumps({"Success": True, "data": info_session.serialize()}), 201
    else:
        return json.dumps({"Success": False, "data": "Club does not exist!"}), 400


@app.route("/api/info_session/<int:info_session_id>/", methods=["POST"])
def delete_info_session(info_session_id):
    info_session = InfoSession.query.filter_by(id=info_session_id).first()
    if info_session is not None:
        db.session.delete(info_session)
        db.session.commit()
        return json.dumps({"Success": True, "data": info_session.serialize()}), 201
    else:
        return json.dumps({"Success": False, "data": "Info session does not exist!"}), 400


@app.route("/api/position/", methods=["POST"])
def create_position():
    body = json.loads(request.data)
    name = body['name']
    link = body['link']
    deadline = body['deadline']
    club_id = body['club_id']

    club = Club.query.filter_by(id=club_id).first()
    if club is not None:
        position = Position(
            name=name,
            link=link,
            deadline=deadline,
            club_id=club_id,
        )
        db.session.add(position)
        db.session.commit()
        return json.dumps({"Success": True, "data": position.serialize()}), 201
    else:
        return json.dumps({"Success": False, "data": "Club does not exist!"}), 400


@app.route("/api/position/<int:position_id>/", methods=["POST"])
def delete_position(position_id):
    position = Position.query.filter_by(id=position_id).first()
    if position is not None:
        db.session.delete(position)
        db.session.commit()
        return json.dumps({"Success": True, "data": position.serialize()}), 201
    else:
        return json.dumps({"Success": False, "data": "Position does not exist!"}), 400


####################
# SHOULD BE CALLED BY FRONTEND
####################
@app.route("/api/clubs/", methods=["GET"])
def get_all_clubs():
    return json.dumps({'Success': True, 'data': [c.serialize() for c in Club.query.all()]}), 200


@app.route("/api/club/<int:club_id>/", methods=["GET"])
def get_club(club_id):
    club = Club.query.filter_by(id=club_id).first()
    if club is not None:
        return json.dumps({"Success": True, "data": club.serialize()}), 201
    else:
        return json.dumps({"Success": False, "data": "Club does not exist!"}), 400


@app.route("/api/club/", methods=["POST"])
def create_club():
    body = json.loads(request.data)
    name = body['name']
    website = body['website']
    portal = body['portal']
    status = body['status']

    club = Club(
        name=name,
        website=website,
        portal=portal,
        status=status,
    )
    db.session.add(club)
    db.session.commit()

    return json.dumps({"Success": True, "data": club.serialize()}), 201


@app.route('/api/club/image/<int:club_id>/', methods=['POST'])
def update_club_image(club_id):
    club = Club.query.filter_by(id=club_id).first()
    if club is not None:
        image = request.files['image']
        filename = secure_filename(image.filename)
        mimetype = image.mimetype
        club.image = image.read()
        club.image_name = filename
        club.mime_type = mimetype
        db.session.commit()
        
        return json.dumps({"Success": True, "data": club.serialize()}), 201
    else:
        return json.dumps({"Success": False, "data": "Club does not exist!"}), 201


@app.route('/api/club/image/<int:club_id>/', methods=["GET"])
def get_club_image(club_id):
    club = Club.query.filter_by(id=club_id).first()
    if club is not None:
        return Response(club.image, mimetype=club.mime_type)
    else:
        return json.dumps({"Success": False, "data": "Club does not exist!"}), 201


@app.route("/api/club/update/<int:club_id>/", methods=["POST"])
def update_club(club_id):
    club = Club.query.filter_by(id=club_id).first()
    if club is not None:
        body = json.loads(request.data)
        name = body['name']
        website = body['website']
        portal = body['portal']
        status = body['status']

        if name != '':
            club.name = name
        if website != '':
            club.website = website
        if portal != '':
            club.portal = portal
        if status != '':
            club.status = status

        db.session.commit()
        return json.dumps({"Success": True, "data": club.serialize()}), 201
    else:
        return json.dumps({"Success": False, "data": "Club does not exist!"}), 201


@app.route("/api/club/delete/<int:club_id>/", methods=["POST"])
def delete_club(club_id):
    club = Club.query.filter_by(id=club_id).first()
    if club is not None:
        db.session.delete(club)
        db.session.commit()
        return json.dumps({"Success": True, "data": club.serialize()}), 201
    else:
        return json.dumps({"Success": False, "data": "Club does not exist!"}), 400


@app.route("/api/students/", methods=["GET"])
def get_all_students():
    return json.dumps({'Success': True, 'data': [t.serialize() for t in Student.query.all()]}), 200


@app.route("/api/student/<int:student_id>/", methods=["GET"])
def get_student(student_id):
    student = Student.query.filter_by(id=student_id).first()
    if student is not None:
        return json.dumps({"Success": True, "data": student.serialize()}), 201
    else:
        return json.dumps({"Success": False, "data": "Student does not exist!"}), 400


####################
# SHOULD BE CALLED BY FRONTEND
####################
@app.route("/api/student/", methods=["POST"])
def create_student():
    body = json.loads(request.data)
    email = body["email"]
    club_ids = body["club_ids"]

    student = Student(
        email=email
    )

    existing_student = Student.query.filter_by(email=email).first()
    if existing_student is not None:
        db.session.delete(existing_student)
    for id in club_ids:
        club = Club.query.filter_by(id=id).first()
        if club is not None:
            student.clubs.append(club)
        else:
            return json.dumps({"Success": False, "data": "Club does not exist!"}), 201
    db.session.add(student)
    db.session.commit()

    return json.dumps({"Success": True, "data": student.serialize()}), 201


@app.route("/api/student/delete/<int:student_id>/", methods=["POST"])
def delete_student(student_id):
    student = Student.query.filter_by(id=student_id).first()
    if student is not None:
        db.session.delete(student)
        db.session.commit()
        return json.dumps({"Success": True, "data": student.serialize()}), 201
    else:
        return json.dumps({"Success": False, "data": "Student does not exist!"}), 400


@app.route("/api/email/<int:club_id>/", methods=["POST"])
def send_email(club_id):
    club = Club.query.filter_by(id=club_id).first()
    if club is not None:
        students = club.serialize().get("students")
        contacts = []
        for student_id in students:
            print("student_id is: ")
            print(student_id)
            student = Student.query.filter_by(id=student_id).first()
            if student is not None:
                print("inside")
                contacts.append(student.email)

        EMAIL_ADDRESS = 'rz327@cornell.edu'
        EMAIL_PASSWORD = 'jiqlphyelbbuioam'

        smtplibObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtplibObj.ehlo()
        smtplibObj.starttls()
        smtplibObj.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject = 'Clubby Email Notification'
        body = 'Clubby email notification is working now.'

        msg = f'Subject: {subject}\n\n{body}'

        print(contacts)

        for a in contacts:
            smtplibObj.sendmail(EMAIL_ADDRESS, a, msg)
            
        return json.dumps({"Success": True, "data": "Emails successfully sent!"}), 201
    
    else:
        return json.dumps({"Success": False, "data": "Club does not exist!"}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
