from app import db

from werkzeug.security import generate_password_hash, check_password_hash


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
    self.set_password(password)

  def set_password(self, password):
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)

  def __repr__(self):
    return '<User %r %r>' % (self.email, self.username)
