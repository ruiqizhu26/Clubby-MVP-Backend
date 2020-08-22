from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table('association', db.Model.metadata,
    db.Column('club_id', db.Integer, db.ForeignKey('club.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'))
)

class InfoSession(db.Model):
    __tablename__ = 'info_session'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.time = kwargs.get('time', '')
        self.location = kwargs.get('location', '')
        self.club_id = kwargs.get('club_id', '')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'time': self.time,
            'location': self.location,
            'club_id': self.club_id
        }


class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String, nullable=False)
    deadline = db.Column(db.String, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id')) 

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.link = kwargs.get('link', '')
        self.deadline = kwargs.get('deadline', '')
        self.club_id = kwargs.get('club_id', '')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'link': self.link,
            'deadline': self.deadline,
            'club_id': self.club_id
        }


class Club(db.Model):
    __tablename__ = "club"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    website = db.Column(db.String, nullable=False)
    portal = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    info_sessions = db.relationship('InfoSession', cascade='delete')
    positions = db.relationship('Position', cascade='delete')
    students = db.relationship("Student", secondary=association_table, back_populates='clubs')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.image = kwargs.get('image', '')
        self.website = kwargs.get('website', '')
        self.portal = kwargs.get('portal', '')
        self.status = kwargs.get('status', '')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            'image': self.image,
            'website': self.website,
            'portal': self.portal,
            'status': self.status,
            'info_sessions': [s.serialize() for s in self.info_sessions],
            'positions': [p.serialize() for p in self.positions],
            'students': [t.id for t in self.students]
        }

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    clubs = db.relationship('Club', secondary=association_table, back_populates='students')

    def __init__(self, **kwargs):
        self.email = kwargs.get('email')

    def serialize(self):
        return {
            'email': self.email,
            'clubs': [c.id for c in self.clubs]
        }