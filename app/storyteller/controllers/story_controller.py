import datetime

from flask import jsonify, request

from app.storyteller.auth import HttpBasicAuthenticationStrategy, \
  AuthenticationHandler, FinalHandler
from app.storyteller.controllers import storyteller
from app.storyteller.models import Story

basic_auth = HttpBasicAuthenticationStrategy()


@storyteller.route('/story/list', methods=['GET'])
def list_stories():
  # Implement proper Auth here
  story_list = AuthenticationHandler(FinalHandler(), basic_auth).execute(
    fn=Story.list_for_user_wpic, bound_request=request,
    user_id=basic_auth.get_user_id(request.authorization))
  return jsonify(stories=story_list), 200


@storyteller.route('/story/list/since/<string:timestamp>', methods=['GET'])
def list_stories_since(timestamp):
  story_list = AuthenticationHandler(FinalHandler(), basic_auth).execute(
    fn=Story.list_for_user_wpic_since, bound_request=request,
    user_id=basic_auth.get_user_id(request.authorization),
    since=datetime.datetime.fromtimestamp(float(timestamp)))
  return jsonify(stories=story_list), 200
