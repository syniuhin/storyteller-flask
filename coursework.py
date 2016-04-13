from flask import Flask, jsonify, request

from neural import generate

import hashlib
import os
import time

import caffe

UPLOAD_FOLDER = '/Users/infm/Coding/study/s4/oop/coursework/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

z = None
time_hash = hashlib.sha1()


@app.route('/')
def hello_world():
  generate.story(z, './neural/images/ex1.jpg')
  return 'Hello World!'


@app.route('/image/upload', methods=['POST'])
def upload_file():
  timestamp = int(time.time())
  time_hash.update(str(timestamp))
  print request.files
  image_file = request.files['image']
  image_filename = os.path.join(app.config['UPLOAD_FOLDER'],
                                time_hash.hexdigest())
  print image_filename
  image_file.save(image_filename)
  print 'Saved'
  return jsonify(status='OK', id=timestamp)


def load_model():
  return generate.load_all()


if __name__ == '__main__':
  app.run(port=4000)
