from flask import jsonify, request

from app import app, db

from app.storyteller.controllers import MockGenerator, storyteller, story_model
from app.storyteller.models import User


@storyteller.route('/user/create', methods=['POST'])
def create_user():
  user = User(**request.get_json())
  db.session.add(user)
  db.session.commit()
  return jsonify(id=user.id), 201


@storyteller.route('/user/login', methods=['POST'])
def login_user():
  user_json = request.get_json()
  potential_user = User.query.filter_by(email=user_json['email']).first()
  if not potential_user.check_password(user_json['password']):
    return jsonify(error='Wrong email and/or password!'), 401
  return jsonify(message="Welcome!"), 200
