from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = Table("association", Base.metadata,
    Column("club_id", Integer, ForeignKey("club.id")),
    Column("user_id", Integer, ForeignKey("user.id"))
)

class Club(db.Model):
    __tablename__ = "club"
    id = db.Column(db.Integer, primaryKey=True)
    name = db.Column(db.String, nullable=False)
    users = db.relationship("Userß")

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")

    def serialize():
        return {
            "id": self.id,
            "name": self.name
        }

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primaryKey=True)
    email = db.Column(db.String, nullable=False)
    club_list = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.email = kwargs.get("email")
        self.club_list = kwargs.get("club_list")

    def serialize():
        return {
            "email": self.email,
            "club_list": self.club_list
        }