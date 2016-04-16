from app import app, db
from app.storyteller.models import User


class AuthStrategy(object):
  def check(self, request_data):
    raise NotImplementedError('AuthStrategy is an abstraction!')


class HttpBasicAuthStrategy(AuthStrategy):
  def check(self, request_data):
    # May be confusing here, but usernames themselves are not unique and emails
    # are.
    potential_user = User.query.filter_by(email=request_data.username).first()
    if potential_user is None:
      return False, None
    return potential_user.check_password(
        request_data.password), {'user_id': potential_user.id}


# TODO: OpenID / OAuth2 strategies
