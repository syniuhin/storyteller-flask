from flask import abort


class AbstractAuthorizer(object):
  def wrap(self, request, fn):
    pass


class Authorizer(AbstractAuthorizer):
  def wrap(self, request, fn):
    return fn(request)


class AuthorizerProxy(AbstractAuthorizer):
  authorizer = Authorizer()

  def __init__(self, auth_strategy):
    self.auth = auth_strategy

  def wrap(self, request, fn):
    result, data = self.auth.check(request.authorization)
    if result:
      return self.authorizer.wrap(request, fn)
    else:
      # raise AttributeError('%r is not authorized' % request_data)
      abort(401)
