from flask import Flask, jsonify, request

import hashlib
import os
import time

import caffe
from core.StoryModel import *

UPLOAD_FOLDER = '/Users/infm/Coding/study/s4/oop/coursework/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True

story_model = MockModel()  # StoryModel()


@app.route('/image/upload', methods=['POST'])
def upload_file():
  timestamp = int(time.time())
  time_hash = hashlib.sha1()
  time_hash.update(str(timestamp))
  image_file = request.files['image']
  image_filename = os.path.join(app.config['UPLOAD_FOLDER'],
                                time_hash.hexdigest())
  image_file.save(image_filename)
  return jsonify(id=timestamp), 201


@app.route('/image/<string:image_id>/story', methods=['GET'])
def generate_story(image_id):
  if not story_model.is_loaded():
    story_model.load_model()
  time_hash = hashlib.sha1()
  time_hash.update(image_id)
  image_loc = os.path.join(app.config['UPLOAD_FOLDER'], time_hash.hexdigest())
  if not os.path.exists(image_loc):
    return jsonify(error='File does not exist'), 404
  story = story_model.generate_story(image_loc=image_loc)
  return jsonify(story=story), 200


if __name__ == '__main__':
  app.run(port=4000)
