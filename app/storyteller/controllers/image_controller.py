import datetime
import hashlib
import os
import time

from flask import jsonify, request, abort, send_file

from app import app, db
from app.storyteller.auth import HttpBasicAuthenticationStrategy, \
  AuthenticationHandler, AuthenticationDemoHandler, AuthorizationHandler, \
  FinalHandler, FileAuthorizationStrategy, DemoFileAuthorizationStrategy
from app.storyteller.controllers import storyteller, story_model
from app.storyteller.models import Story, UploadedFile, UploadedFileTemp

basic_auth = HttpBasicAuthenticationStrategy()


@storyteller.route('/demo/image/upload', methods=['POST'])
def upload_file_demo():
  res = AuthenticationDemoHandler(FinalHandler(), basic_auth).execute(
    upload_demo_file, bound_request=request)
  return jsonify(image_id=res), 201


def upload_demo_file(**kwargs):
  timestamp = int(time.time())
  time_hash = hashlib.sha1()
  time_hash.update(str(timestamp))
  image_file = request.files['image']
  image_filename = time_hash.hexdigest()
  image_file.save(os.path.join(app.config['UPLOAD_TEMP_DIR'],
                               image_filename))

  uploaded_file = UploadedFileTemp(filename=image_filename)
  db.session.add(uploaded_file)
  db.session.commit()
  return uploaded_file.id


@storyteller.route('/image/upload', methods=['POST'])
def upload_file_auth():
  res = AuthenticationHandler(FinalHandler(), basic_auth).execute(
    upload_file, bound_request=request,
    user_id=basic_auth.get_user_id(request.authorization))
  return jsonify(image_id=res), 201


def upload_file(user_id, **kwargs):
  timestamp = int(time.time())
  time_hash = hashlib.sha1()
  time_hash.update(str(timestamp))
  image_file = request.files['image']
  image_filename = time_hash.hexdigest()
  image_file.save(os.path.join(app.config['UPLOAD_DIR'],
                               image_filename))

  uploaded_file = UploadedFile(filename=image_filename, user_id=user_id)
  db.session.add(uploaded_file)
  db.session.commit()
  return uploaded_file.id


@storyteller.route('/image/<string:image_id>/download', methods=['GET'])
def download_file_auth(image_id):
  res = AuthenticationHandler(
    AuthorizationHandler(FinalHandler(), FileAuthorizationStrategy(image_id)),
    basic_auth).execute(download_file, bound_request=request, image_id=image_id)
  return res, 200


def download_file(image_id, **kwargs):
  file_record = UploadedFile.query.filter_by(id=image_id).first()
  if file_record is None:
    return None
  return send_file(os.path.join(app.config['UPLOAD_DIR'], file_record.filename),
                   mimetype='image/jpeg')


@storyteller.route('/image/<string:image_id>/story', methods=['GET'])
def generate_story_auth(image_id):
  res = AuthenticationHandler(
    AuthorizationHandler(FinalHandler(), FileAuthorizationStrategy(image_id)),
    basic_auth).execute(generate_story, bound_request=request,
                        image_id=image_id)
  return jsonify(text=res), 200


def generate_story(image_id, **kwargs):
  if not story_model.is_loaded():
    story_model.load_model()
  image_file = UploadedFile.query.filter_by(id=image_id).first()
  image_loc = os.path.join(app.config['UPLOAD_DIR'], image_file.filename)
  if not os.path.exists(image_loc):
    return jsonify(error='File does not exist'), 404
  story_text = story_model.generate_story(image_loc=image_loc)
  return story_text


@storyteller.route('/demo/image/<string:image_id>/story', methods=['GET'])
def generate_story_demo(image_id):
  res = AuthenticationDemoHandler(
    AuthorizationHandler(FinalHandler(),
                         DemoFileAuthorizationStrategy(image_id)),
    basic_auth).execute(generate_demo_story, bound_request=request,
                        image_id=image_id, user_id=-1)
  return jsonify(text=res), 200


def generate_demo_story(image_id, **kwargs):
  if not story_model.is_loaded():
    story_model.load_model()
  image_file = UploadedFileTemp.query.filter_by(id=image_id).first()
  image_loc = os.path.join(app.config['UPLOAD_TEMP_DIR'], image_file.filename)
  if not os.path.exists(image_loc):
    return jsonify(error='File does not exist'), 404
  story_text = story_model.generate_story(image_loc=image_loc)
  return story_text


@storyteller.route('/image/<string:image_id>/story/create', methods=['POST'])
def create_story_auth(image_id):
  res = AuthenticationHandler(
    AuthorizationHandler(FinalHandler(), FileAuthorizationStrategy(image_id)),
    basic_auth).execute(
    create_story, bound_request=request, image_id=image_id,
    user_id=basic_auth.get_user_id(request.authorization))
  return jsonify(id=res), 201


def create_story(bound_request, image_id, user_id, **kwargs):
  json = bound_request.get_json()

  if 'text' not in json or len(json['text']) < 1:
    abort(403)
  story = Story(user_id=user_id, story_type=0, text=json['text'],
                time_created=datetime.datetime.now())
  db.session.add(story)
  db.session.commit()

  image_file = UploadedFile.query.filter_by(id=image_id).first()
  image_file.story_id = story.id
  db.session.commit()
  return story.id
