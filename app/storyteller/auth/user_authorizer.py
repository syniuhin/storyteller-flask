from flask import abort, jsonify, request

from app import app, db


class AbstractAuthorizer(object):
  def execute(self, request_data, fn):
    pass


class Authorizer(AbstractAuthorizer):
  def execute(self, request_data, fn):
    return fn(request_data)


class AuthorizerProxy(AbstractAuthorizer):
  authorizer = Authorizer()

  def __init__(self, auth_strategy):
    self.auth = auth_strategy

  def execute(self, request_data, fn):
    result, data = self.auth.check(request_data)
    if result:
      return self.authorizer.execute(data, fn)
    else:
      # raise AttributeError('%r is not authorized' % request_data)
      abort(401)
