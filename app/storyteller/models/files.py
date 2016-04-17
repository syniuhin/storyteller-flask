from app import db


class UploadedFile(db.Model):
  """
  Class for representing uploaded file and bind it to user and story.
  """
  __tablename__ = 'uploaded_file'

  id = db.Column(db.Integer, primary_key=True)
  story_id = db.Column(db.Integer, db.ForeignKey('story.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  filename = db.Column(db.String(255), unique=True)

  def __init__(self, user_id, filename, story_id=None):
    self.story_id = story_id
    self.user_id = user_id
    self.filename = filename

  def __repr__(self):
    return '<UploadedFile %r %r>' % (self.story_id, self.user_id)


class UploadedFileTemp(db.Model):
  __tablename__ = 'uploaded_file_temp'

  id = db.Column(db.Integer, primary_key=True)
  filename = db.Column(db.String(255), unique=True)

  def __init__(self, filename):
    self.filename = filename

  def __repr__(self):
    return '<UploadedFileTemp %r>' % self.filename
