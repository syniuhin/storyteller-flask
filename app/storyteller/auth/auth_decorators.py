from flask import abort


class FnComponent(object):
  def execute(self, fn, **kwargs):
    pass


class ConcreteFn(FnComponent):
  def execute(self, fn, **kwargs):
    return fn(**kwargs)


class FnDecorator(FnComponent):
  def __init__(self, component):
    self.component = component

  def execute(self, fn, **kwargs):
    return self.component.execute(fn, **kwargs)


class AuthFnDecorator(FnDecorator):
  def __init__(self, component, auth_strategy):
    super(AuthFnDecorator, self).__init__(component)
    self.auth_strategy = auth_strategy

  def execute(self, fn, **kwargs):
    request = kwargs.get('bound_request')
    if not request.authorization or \
        not self.auth_strategy.check(request.authorization):
      abort(401)
    return self.component.execute(fn, **kwargs)
