from app.storyteller.models import User


class AuthStrategy(object):
  def check(self, request_data):
    raise NotImplementedError('AuthStrategy is an abstraction!')

  def get_user_id(self, request_data):
    raise NotImplementedError('AuthStrategy is an abstraction!')


class HttpBasicAuthStrategy(AuthStrategy):
  def check(self, request_data):
    # May be confusing here, but usernames themselves are not unique and emails
    # are.
    potential_user = User.query.filter_by(email=request_data.username).first()
    return potential_user is not None and \
        potential_user.check_password(request_data.password)

  def get_user_id(self, request_data):
    potential_user = User.query.filter_by(email=request_data.username).first()
    if potential_user is not None:
      return potential_user.id
    return -1


# TODO: OpenID / OAuth2 strategies
