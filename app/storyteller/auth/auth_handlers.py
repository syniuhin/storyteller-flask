from flask import abort

from util import AuthUser


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

  def check_auth(self, request):
    if not request.authorization:
      return False
    auth_user = self.auth_strategy.check(request.authorization)
    if auth_user is AuthUser.unknown or auth_user is AuthUser.demo:
      return False
    return True

  def execute(self, fn, **kwargs):
    request = kwargs.get('bound_request')
    if not self.check_auth(request):
      abort(401)
    return self.successor.execute(fn, **kwargs)


class AuthenticationDemoHandler(AuthenticationHandler):
  def __init__(self, successor, authentication_strategy):
    super(AuthenticationDemoHandler, self).__init__(successor,
                                                    authentication_strategy)

  def check_auth(self, request):
    if not request.authorization:
      return False
    auth_user = self.auth_strategy.check(request.authorization)
    if auth_user is AuthUser.unknown or auth_user is AuthUser.auth:
      return False
    return True


class AuthorizationHandler(PredecessorHandler):
  def __init__(self, successor, authorization_strategy):
    super(AuthorizationHandler, self).__init__(successor)
    self.authorization_strategy = authorization_strategy

  def execute(self, fn, **kwargs):
    user_id = kwargs.get('user_id')
    if not self.authorization_strategy.check(user_id):
      abort(401)
    return self.successor.execute(fn, **kwargs)


class HandlerBuilder(object):
  def __init__(self):
    self.handler = FinalHandler()

  def add_handler(self, predecessor, **kwargs):
    self.handler = predecessor(successor=self.handler, **kwargs)
    return self

  def build(self):
    return self.handler
