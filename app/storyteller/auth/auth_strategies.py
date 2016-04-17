from app.storyteller.models import User, UploadedFile, Story
from util import AuthUser


class AuthenticationStrategy(object):
  def check(self, request_data):
    raise NotImplementedError('AuthStrategy is an abstraction!')

  def get_user_id(self, request_data):
    raise NotImplementedError('AuthStrategy is an abstraction!')


class HttpBasicAuthenticationStrategy(AuthenticationStrategy):
  def check(self, request_data):
    # May be confusing here, but usernames themselves are not unique and emails
    # are.
    if request_data.username == 'foo@example.com' \
        and request_data.password == 'bar':
      print 'DEMO'
      return AuthUser.demo
    potential_user = User.query.filter_by(email=request_data.username).first()
    if potential_user is not None and \
        potential_user.check_password(request_data.password):
      return AuthUser.auth
    return AuthUser.unknown

  def get_user_id(self, request_data):
    potential_user = User.query.filter_by(email=request_data.username).first()
    if potential_user is not None:
      return potential_user.id
    return -1


# TODO: OpenID / OAuth2 strategies


class AuthorizationStrategy(object):
  def check(self, user_id):
    raise NotImplementedError('AuthStrategy is an abstraction!')


class FileAuthorizationStrategy(AuthorizationStrategy):
  def __init__(self, file_id):
    self.file_id = file_id

  def check(self, user_id):
    return UploadedFile.query.filter_by(id=self.file_id,
                                        user_id=user_id).first() is not None


class DemoFileAuthorizationStrategy(FileAuthorizationStrategy):
  def check(self, user_id):
    return user_id == -1


class StoryAuthorizationStrategy(AuthorizationStrategy):
  def __init__(self, story_id):
    self.story_id = story_id

  def check(self, user_id):
    return Story.query.filter_by(id=self.story_id,
                                 user_id=user_id).first() is not None
