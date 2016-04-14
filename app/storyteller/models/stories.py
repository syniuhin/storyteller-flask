from app import db


class Story(db.Model):
  """
  Class for representing story that was generated.

  As for now, story types are:
  0: for a story generated about single image;
  1: multiple images (e.g. album);
  2: location based multiple images (e.g. trip).

  They should be carefully reviewed and will change a lot.
  """
  __tablename__ = 'story'

  id = db.Column(db.Integer, primary_key=True)
  story_type = db.Column(db.Integer, nullable=False)
  text = db.Column(db.String, nullable=False)
  files = db.relationship('UploadedFile', backref='story', lazy='dynamic')

  def __init__(self, story_type, text):
    self.story_type = story_type
    self.text = text

  def __repr__(self):
    return '<Story %r>' % self.id
