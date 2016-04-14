from app import db


class User(db.Model):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(255), nullable=False)
  files = db.relationship('UploadedFile', backref='user', lazy='dynamic')
  stories = db.relationship('Story', backref='user', lazy='dynamic')

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = password

  def __repr__(self):
    return '<User %r %r>' % (self.email, self.username)
