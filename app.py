from flask import Flask, request
from db import db, User
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

@app.route("/api/user/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    email = body["email"]
    club_list = body["club_list"]
    user = User(
        email = email,
        club_list = club_list
    )
    db.session.add(user)
    db.session.commit()

    return json.dumps({"Success": True, "data": user.serialize()})