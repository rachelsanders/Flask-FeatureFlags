"""
(c) 2013 Rachel Sanders.  All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
   limitations under the License.
"""

from functools import wraps
import logging

from flask import abort, current_app, url_for
from flask import redirect as _redirect
from flask.signals import Namespace

__version__ = '1.0'

log = logging.getLogger(u'flask-featureflags')

RAISE_ERROR_ON_MISSING_FEATURES = u'RAISE_ERROR_ON_MISSING_FEATURES'
FEATURE_FLAGS_CONFIG = u'FEATURE_FLAGS'

EXTENSION_NAME = "FeatureFlags"


class StopCheckingFeatureFlags(Exception):
  """ Raise this inside of a feature flag handler to immediately return False and stop any further handers from running """
  pass


class NoFeatureFlagFound(Exception):
  """ Raise this when the feature flag does not exist. """
  pass


_ns = Namespace()
missing_feature = _ns.signal('missing-feature')


def AppConfigFlagHandler(feature=None):
  """ This is the default handler. It checks for feature flags in the current app's configuration.

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
  if not current_app:
    log.warn(u"Got a request to check for {feature} but we're outside the request context. Returning False".format(feature=feature))
    return False

  try:
    return current_app.config[FEATURE_FLAGS_CONFIG][feature]
  except (AttributeError, KeyError):
    raise NoFeatureFlagFound()


class FeatureFlag(object):

  JINJA_TEST_NAME = u'active_feature'

  def __init__(self, app=None):
    if app is not None:
      self.init_app(app)

    # The default out-of-the-box handler looks up features in Flask's app config.
    self.handlers = [AppConfigFlagHandler]

  def init_app(self, app):
    """ Add ourselves into the app config and setup, and add a jinja function test """

    app.config.setdefault(FEATURE_FLAGS_CONFIG, {})
    app.config.setdefault(RAISE_ERROR_ON_MISSING_FEATURES, False)

    if hasattr(app, "add_template_test"):
      # flask 0.10 and higher has a proper hook
      app.add_template_test(self.check, name=self.JINJA_TEST_NAME)
    else:
      app.jinja_env.tests[self.JINJA_TEST_NAME] = self.check

    if not hasattr(app, 'extensions'):
      app.extensions = {}
    app.extensions[EXTENSION_NAME] = self

  def clear_handlers(self):
    """ Clear all handlers. This effectively turns every feature off."""
    self.handlers = []

  def add_handler(self, function):
    """ Add a new handler to the end of the chain of handlers. """
    self.handlers.append(function)

  def remove_handler(self, function):
    """ Remove a handler from the chain of handlers.  """
    try:
      self.handlers.remove(function)
    except ValueError:  # handler wasn't in the list, pretend we don't notice
      pass

  def check(self, feature):
    """ Loop through all our feature flag checkers and return true if any of them are true.

    The order of handlers matters - we will immediately return True if any handler returns true.

    If you want to a handler to return False and stop the chain, raise the StopCheckingFeatureFlags exception."""
    found = False
    for handler in self.handlers:
      try:
        if handler(feature):
           return True
      except StopCheckingFeatureFlags:
        return False
      except NoFeatureFlagFound:
        pass
      else:
        found = True

    if not found:
      message = u"No feature flag defined for {feature}".format(feature=feature)
      if current_app.debug and current_app.config.get(RAISE_ERROR_ON_MISSING_FEATURES, False):
        raise KeyError(message)
      else:
        log.info(message)
        missing_feature.send(self, feature=feature)

    return False


def is_active(feature):
  """ Check if a feature is active """

  if current_app:
    feature_flagger = current_app.extensions.get(EXTENSION_NAME)
    if feature_flagger:
      return feature_flagger.check(feature)
    else:
      raise AssertionError("Oops. This application doesn't have the Flask-FeatureFlag extention installed.")

  else:
    log.warn(u"Got a request to check for {feature} but we're running outside the request context. Check your setup. Returning False".format(feature=feature))
    return False


def is_active_feature(feature, redirect_to=None, redirect=None):
  """
  Decorator for Flask views. If a feature is off, it can either return a 404 or redirect to a URL if you'd rather.
  """
  def _is_active_feature(func):
    @wraps(func)
    def wrapped(*args, **kwargs):

      if not is_active(feature):
        url = redirect_to
        if redirect:
          url = url_for(redirect)

        if url:
          log.debug(u'Feature {feature} is off, redirecting to {url}'.format(feature=feature, url=url))
          return _redirect(url, code=302)
        else:
          log.debug(u'Feature {feature} is off, aborting request'.format(feature=feature))
          abort(404)

      return func(*args, **kwargs)
    return wrapped
  return _is_active_feature


# Silence that annoying No handlers could be found for logger "flask-featureflags"
class NullHandler(logging.Handler):
  def emit(self, record):
    pass


log.addHandler(NullHandler())
