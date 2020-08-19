from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = Table('association', Base.metadata,
    Column('club_id', Integer, ForeignKey('club.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)

class InfoSession(db.Model):
    __tablename__ = 'info_session'
    id = db.Column(db.Integer, primaryKey=True)
    time = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    club_id = db.Column(db.Integer, foreignKey='club.id')
    club = db.relationship('Club', back_populates='info_session')

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.time = kwargs.get('time')
        self.location = kwargs.get('location')

    def serialzie(self):
        return {
            'id': self.id,
            'time': self.time,
            'location': self.location
        }


class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primaryKey=True)
    name = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String, nullable=False)
    deadline = db.Column(db.String, nullable=False)
    club_id = db.Column(db.Integer, foreignKey='club.id') 
    club = db.relationship('Club', back_populates='position')

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.link = kwargs.get('link')
        self.deadline = kwargs.get('deadline')

    def serialze():
        return {
            'id': self.id,
            'name': self.name,
            'link': self.link,
            'deadline': self.deadline
        }


class Club(db.Model):
    __tablename__ = "club"
    id = db.Column(db.Integer, primaryKey=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    website = db.Column(db.String, nullable=False)
    portal = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    info_sessions = db.relationship('InfoSession', back_populates='club')
    positions = db.relationship('Position', back_populates='club')
    students = db.relationship("Student", secondary=association_table, back_populates='club')

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')

    def serialize():
        return {
            "id": self.id,
            "name": self.name,
            'image': self.image,
            'website': self.website,
            'portal': self.portal,
            'status': self.status
        }

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primaryKey=True)
    email = db.Column(db.String, nullable=False)
    clubs = db.relationship('Club', secondary=association_table, back_populates='student')

    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.clubs = kwargs.get('clubs')

    def serialize():
        return {
            'email': self.email,
            'clubs': self.clubs
        }