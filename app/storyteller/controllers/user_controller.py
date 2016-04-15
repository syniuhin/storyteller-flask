from flask import jsonify, request

from app import app, db

from app.storyteller.controllers import MockGenerator, storyteller, story_model
from app.storyteller.models import User

import re

EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')


@storyteller.route('/user/register', methods=['POST'])
def create_user():
  json = request.get_json()
  if 'email' not in json or not EMAIL_REGEX.match(json['email']):
    return 'Bad email', 403
  if 'password' not in json or len(json['password']) < 6:
    return 'Bad password', 403
  if 'username' not in json:
    json['username'] = json['email'].split('@')[1].capitalize()
  user = User(**json)
  db.session.add(user)
  db.session.commit()
  return jsonify(message='%s is registered.' % user.username,
                 user_id=user.id), 201


@storyteller.route('/user/login', methods=['POST'])
def login_user():
  user_json = request.get_json()
  potential_user = User.query.filter_by(email=user_json['email']).first()
  if potential_user is None or \
      not potential_user.check_password(user_json['password']):
    return 'Wrong email and/or password!', 401
  return jsonify(message='Welcome, %s!' % potential_user.username,
                 user_id=potential_user.id), 200
