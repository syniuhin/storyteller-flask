# Import flask dependencies
from flask import Blueprint, jsonify, request

# Import the database object from the main app module
from app import app

# Import module models (i.e. User)
# from app.mod_auth.models import User

from core.StoryModel import *

import hashlib
import os
import time

# Define the blueprint: 'auth', set its url prefix: app.url/auth
storyteller = Blueprint('storyteller', __name__, url_prefix='/storyteller')

story_model = MockModel()  # StoryModel()


@storyteller.route('/image/upload', methods=['POST'])
def upload_file():
  timestamp = int(time.time())
  time_hash = hashlib.sha1()
  time_hash.update(str(timestamp))
  image_file = request.files['image']
  image_filename = os.path.join(app.config['UPLOAD_FOLDER'],
                                time_hash.hexdigest())
  image_file.save(image_filename)
  return jsonify(id=timestamp), 201


@storyteller.route('/image/<string:image_id>/story', methods=['GET'])
def generate_story(image_id):
  if not story_model.is_loaded():
    story_model.load_model()
  time_hash = hashlib.sha1()
  time_hash.update(image_id)
  image_loc = os.path.join(app.config['UPLOAD_DIR'], time_hash.hexdigest())
  if not os.path.exists(image_loc):
    return jsonify(error='File does not exist'), 404
  story = story_model.generate_story(image_loc=image_loc)
  return jsonify(story=story), 200
