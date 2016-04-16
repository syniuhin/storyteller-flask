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
  time_created = db.Column(db.DateTime, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  files = db.relationship('UploadedFile', backref='story', lazy='dynamic')

  def __init__(self, user_id, story_type, text, time_created):
    self.user_id = user_id
    self.story_type = story_type
    self.text = text
    self.time_created = time_created

  def __repr__(self):
    return '<Story %r>' % self.id

  def dict_serialize(self):
    return {
      'id': self.id,
      'story_type': self.story_type,
      'text': self.text,
      'time_created': self.time_created,
      'user_id': self.user_id
    }

  @staticmethod
  def list_for_user(user_id, **kwargs):
    return [s.dict_serialize() for s in
            Story.query.filter_by(user_id=user_id).all()]
