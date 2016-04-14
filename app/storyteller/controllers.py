# Import flask dependencies
from flask import Blueprint, jsonify, request

# Import the database object from the main app module
from app import app, db

# Import module models (i.e. User)
# from app.mod_auth.models import User

from core.story_generator import *
from models.files import *
from models.users import *

import hashlib
import os
import time

# Define the blueprint: 'auth', set its url prefix: app.url/auth
storyteller = Blueprint('storyteller', __name__, url_prefix='/storyteller')

story_model = MockGenerator()  # StoryModel()


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

  file_id = UploadedFile.query.filter_by(filename=image_filename).first().id
  return jsonify(id=file_id), 201


@storyteller.route('/image/<string:image_id>/story', methods=['GET'])
def generate_story(image_id):
  if not story_model.is_loaded():
    story_model.load_model()
  image_filename = UploadedFile.query.filter_by(id=image_id).first().filename
  image_loc = os.path.join(app.config['UPLOAD_DIR'], image_filename)
  if not os.path.exists(image_loc):
    return jsonify(error='File does not exist'), 404
  story = story_model.generate_story(image_loc=image_loc)
  return jsonify(story=story), 200
