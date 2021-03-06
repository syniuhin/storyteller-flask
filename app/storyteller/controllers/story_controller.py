import datetime

from flask import jsonify, request

from app.storyteller.auth import HttpBasicAuthenticationStrategy, \
  AuthenticationHandler, FinalHandler, HandlerBuilder
from app.storyteller.controllers import storyteller
from app.storyteller.models import Story

basic_auth = HttpBasicAuthenticationStrategy()


@storyteller.route('/story/list', methods=['GET'])
def list_stories():
  # Implement proper Auth here
  story_list = HandlerBuilder() \
    .add_handler(AuthenticationHandler, authentication_strategy=basic_auth) \
    .build() \
    .execute(fn=Story.list_for_user_wpic, bound_request=request,
             user_id=basic_auth.get_user_id(request.authorization))
  return jsonify(stories=story_list), 200


@storyteller.route('/story/list/since/<string:timestamp>', methods=['GET'])
def list_stories_since(timestamp):
  story_list = HandlerBuilder() \
    .add_handler(AuthenticationHandler, authentication_strategy=basic_auth) \
    .build() \
    .execute(fn=Story.list_for_user_wpic_since, bound_request=request,
             user_id=basic_auth.get_user_id(request.authorization),
             since=datetime.datetime.fromtimestamp(float(timestamp)))
  return jsonify(stories=story_list), 200


@storyteller.route('/story/list/after/<int:after_id>', methods=['GET'])
def list_stories_afte(after_id):
  story_list = HandlerBuilder() \
    .add_handler(AuthenticationHandler, authentication_strategy=basic_auth) \
    .build() \
    .execute(fn=Story.list_for_user_wpic_after, bound_request=request,
             user_id=basic_auth.get_user_id(request.authorization),
             after_id=after_id)
  return jsonify(stories=story_list), 200
