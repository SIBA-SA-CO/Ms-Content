from . import db


class Content(db.Model):
    __tablename__="contents"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    standard_title = db.Column(db.String(255), unique=True, nullable=False)
    serial_episodes = db.relationship("Serial_episode")

class Serial_episode(db.Model):
    __tablename__ = "serial_episodes"
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey("contents.id"), nullable=False)
    serial_id = db.Column(db.Integer, db.ForeignKey("serials.id"), nullable=False)
    season = db.Column(db.Integer, nullable=False)
    episode = db.Column(db.Integer, nullable=False)

class Serial(db.Model):
    __tablename__ = "serials"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    standard_title = db.Column(db.String(255), unique=True, nullable=False)
    serial_episodes = db.relationship("Serial_episode")

class Title(db.Model):
    __tablename__ = "titles"
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey("contents.id"))
    title = db.Column(db.String(255), unique=False, nullable=False)



