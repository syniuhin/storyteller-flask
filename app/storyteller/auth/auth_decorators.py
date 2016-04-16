from flask import abort

from app.storyteller.models import User


class Handler(object):
  def execute(self, fn, **kwargs):
    raise NotImplementedError()


class FinalHandler(Handler):
  def execute(self, fn, **kwargs):
    return fn(**kwargs)


class PredecessorHandler(Handler):
  def __init__(self, successor):
    self.successor = successor

  def execute(self, fn, **kwargs):
    raise NotImplementedError()


class AuthenticationHandler(PredecessorHandler):
  def __init__(self, successor, authentication_strategy):
    super(AuthenticationHandler, self).__init__(successor)
    self.auth_strategy = authentication_strategy

  def execute(self, fn, **kwargs):
    request = kwargs.get('bound_request')
    if not request.authorization or \
        not self.auth_strategy.check(request.authorization):
      abort(401)
    kwargs_updated = kwargs.copy()
    kwargs_updated.update({'user_id': User.query.filter_by(
      email=request.authorization.username).first().id})
    return self.successor.execute(fn, **kwargs_updated)


class AuthorizationHandler(PredecessorHandler):
  def __init__(self, successor, authorization_strategy):
    super(AuthorizationHandler, self).__init__(successor)
    self.authorization_strategy = authorization_strategy

  def execute(self, fn, **kwargs):
    user_id = kwargs.get('user_id')
    if not self.authorization_strategy.check(user_id):
      abort(401)
    return self.successor.execute(fn, **kwargs)
