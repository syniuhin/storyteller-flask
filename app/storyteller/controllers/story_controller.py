from flask import jsonify, request

from app import app, db

from app.storyteller.controllers import MockGenerator, storyteller, story_model
from app.storyteller.models import User, Story
from app.storyteller.auth import AuthorizerProxy, HttpBasicAuthStrategy

authorizer = AuthorizerProxy(HttpBasicAuthStrategy())


@storyteller.route('/story/list', methods=['GET'])
def list_stories():
  auth = request.authorization
  if not auth:
    return 401

  story_list = authorizer.execute(auth, fn=(lambda data: Story
                                            .list_for_user(data['user_id'])))
  return jsonify(stories=story_list), 200
