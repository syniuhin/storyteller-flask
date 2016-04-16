from flask import jsonify, request

from app.storyteller.auth import HttpBasicAuthStrategy, AuthenticateFnDecorator, \
  ConcreteFn
from app.storyteller.controllers import storyteller
from app.storyteller.models import Story

auth_strategy = HttpBasicAuthStrategy()


@storyteller.route('/story/list', methods=['GET'])
def list_stories():
  story_list = AuthenticateFnDecorator(ConcreteFn(), auth_strategy).execute(
    fn=Story.list_for_user, bound_request=request,
    user_id=auth_strategy.get_user_id(request.authorization))
  return jsonify(stories=story_list), 200
