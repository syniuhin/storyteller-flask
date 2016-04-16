from flask import jsonify, request

from app.storyteller.auth import HttpBasicAuthenticationStrategy, \
  AuthenticationHandler, AuthorizationHandler, FinalHandler, \
  StoryAuthorizationStrategy
from app.storyteller.controllers import storyteller
from app.storyteller.models import Story

basic_auth = HttpBasicAuthenticationStrategy()


@storyteller.route('/story/list', methods=['GET'])
def list_stories():
  # Implement proper Auth here
  story_list = AuthenticationHandler(FinalHandler(), basic_auth).execute(
    fn=Story.list_for_user, bound_request=request,
    user_id=basic_auth.get_user_id(request.authorization))
  return jsonify(stories=story_list), 200
