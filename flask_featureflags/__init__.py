from functools import wraps
import logging

from flask import abort, current_app, g, redirect

__version__ = u'0.1'

log = logging.getLogger(u'flask-featureflags')

class StopCheckingFeatureFlags(Exception):
  pass

def NullFlagHandler(feature):
  """ This handler always returns True """
  return False

def AlwaysOffFlagHandler(feature):
  """ This handler always returns False """
  raise StopCheckingFeatureFlags

def AlwaysOnFlagHandler(feature):
  """ This handler always returns True """
  return True

def AppConfigFlagHandler(feature=None):
  """ This checks in the current app configuration for an FEATURE_FLAGS dictionary. Each feature is a key in that dictionary.

  For example, to have 'unfinished_feature' hidden in production but active in development:

  config.py

  class ProductionConfig(Config):

    FEATURE_FLAGS = {
      'unfinished_feature' : False,
    }


  class DevelopmentConfig(Config):

    FEATURE_FLAGS = {
      'unfinished_feature' : True,
    }

   """
  if current_app is None:
    log.warn(u"Got a request to check for {feature} but we're outside the request context. Returning False".format(feature=feature))
    return False

  try:
    return current_app.config[u'FEATURE_FLAGS'][feature]
  except (AttributeError, KeyError):
    log.info(u"No feature flag defined for {feature}".format(feature=feature))
    return False

class FeatureFlagExtension(object):

  def __init__(self, app):
    if app is not None:
      self.init_app(app)

    # Enable
    self.handlers = [AppConfigFlagHandler]

  def init_app(self, app):
    """ Inject ourself into the request setup and add a jinja function test """
    app.before_request(self.process_request)
    app.jinja_env.tests[u'active_feature'] = self.check

  def process_request(self):
    """ Load ourselves into the globals """
    g.feature_flags = self

  def clear_handlers(self):
    self.handlers = []

  def add_handler(self, function):
    """ Add a function to the handler  """
    self.handlers.append(function)

  def remove_handler(self, function):
    try:
      self.handlers.remove(function)
    except ValueError: # handler wasn't in the list, just ignore
      pass

  def check(self, feature):
    """ Loop through all our feature flag checkers and return true if any of them are true.

    If you want to return False and stop the chain, raise the StopCheckingFeatureFlags exception."""
    for handler in self.handlers:
      try:
        if handler(feature): return True
      except StopCheckingFeatureFlags:
        return False
    else:
      return False


def is_active(feature):

  if hasattr(g, u'feature_flags') and isinstance(g.feature_flags, FeatureFlagExtension):
    return g.feature_flags.check(feature)
  else:
    log.warn(u'Got a request to check for {feature} but no handlers are configured. Check your setup. Returning False'.format(feature=feature))
    return False

def is_active_feature(feature, redirect_to=None):
  """
  Decorator which enables/disables views based on active features.
  """
  def _is_active_feature(func):
    @wraps(func)
    def wrapped(*args, **kwargs):

      if not is_active(feature):
        if redirect_to:
          log.debug(u'Feature {0} is off, redirecting to {1}'.format(feature, redirect_to))
          return redirect(redirect_to, code=302)
        else:
          log.debug(u'Feature {0} is off, aborting request'.format(feature))
          abort(404)

      return func(*args, **kwargs)
    return wrapped
  return _is_active_feature