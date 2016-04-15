from flask import jsonify, request

from app import app, db

from app.storyteller.controllers import MockGenerator, storyteller, story_model
from app.storyteller.models import Story, UploadedFile

import hashlib
import os
import time
import datetime


@storyteller.route('/image/upload', methods=['POST'])
def upload_file():
  timestamp = int(time.time())
  time_hash = hashlib.sha1()
  time_hash.update(str(timestamp))
  image_file = request.files['image']
  image_filename = time_hash.hexdigest()
  image_file.save(os.path.join(app.config['UPLOAD_DIR'],
                               image_filename))

  uploaded_file = UploadedFile(filename=image_filename, user_id=0)
  db.session.add(uploaded_file)
  db.session.commit()

  return jsonify(image_id=uploaded_file.id), 201


@storyteller.route('/image/<string:image_id>/story', methods=['GET'])
def generate_story(image_id):
  if not story_model.is_loaded():
    story_model.load_model()
  image_file = UploadedFile.query.filter_by(id=image_id).first()
  image_loc = os.path.join(app.config['UPLOAD_DIR'], image_file.filename)
  if not os.path.exists(image_loc):
    return jsonify(error='File does not exist'), 404
  story_text = story_model.generate_story(image_loc=image_loc)
  return jsonify(story=story_text), 200


@storyteller.route('/image/<string:image_id>/story/create', methods=['POST'])
def create_story(image_id):
  json = request.get_json()
  if 'story' not in json or len(json['story']) < 1:
    return 'Bad story', 403
  story = Story(user_id=0, story_type=0, text=json['story'],
                time_created=datetime.datetime.now())
  db.session.add(story)
  db.session.commit()

  image_file = UploadedFile.query.filter_by(id=image_id).first()
  image_file.story_id = story.id
  db.session.commit()
  return jsonify(story_id=story.id), 201
