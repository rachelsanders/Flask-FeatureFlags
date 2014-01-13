from __future__ import with_statement

import unittest

from flask import Flask, url_for
from .fixtures import app, feature_setup, FEATURE_NAME, FEATURE_IS_ON, FEATURE_IS_OFF, FLAG_CONFIG, RAISE_ERROR

import flask_featureflags as feature_flags


class TestFeatureFlagCoreFunctionality(unittest.TestCase):

  def setUp(self):
    app.config[FLAG_CONFIG] = {FEATURE_NAME: True}
    app.config['TESTING'] = True

    if RAISE_ERROR in app.config:
      del app.config[RAISE_ERROR]

    self.app = app
    self.test_client = app.test_client()
    self.app.debug = True

    # Make sure the handlers are what we expect
    feature_setup.clear_handlers()
    feature_setup.add_handler(feature_flags.AppConfigFlagHandler)

  def test_decorator_returns_the_view_if_feature_is_on(self):
    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      app.config[FLAG_CONFIG][FEATURE_NAME] = True

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code %s' % response.status_code
      assert FEATURE_IS_ON in response.data.decode(u'utf-8')

  def test_decorator_returns_404_if_feature_is_off(self):

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      app.config[FLAG_CONFIG][FEATURE_NAME] = False

      response = self.test_client.get(url)
      assert response.status_code == 404, u'Unexpected status code %s' % response.status_code
      assert FEATURE_IS_ON not in response.data.decode(u'utf-8')

  def test_decorator_redirects_to_url_if_redirect_is_set_and_feature_is_off(self):
      with self.app.test_request_context('/'):
        url = url_for('redirect_with_decorator')

        app.config[FLAG_CONFIG][FEATURE_NAME] = False

        response = self.test_client.get(url)
        assert response.status_code == 302, u'Unexpected status code %s' % response.status_code
        assert response.location == url_for('redirect_destination', _external=True), \
            u'Expected redirect to %s, got %s => ' % (url_for('redirect_destination'), response.location)

  def test_view_based_feature_flag_returns_new_code_if_flag_is_on(self):
    with self.app.test_request_context('/'):
      url = url_for('view_based_feature_flag')

      app.config[FLAG_CONFIG][FEATURE_NAME] = True

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code %s' % response.status_code
      assert FEATURE_IS_ON in response.data.decode(u'utf-8')

  def test_view_based_feature_flag_returns_old_code_if_flag_is_off(self):
    with self.app.test_request_context('/'):
      url = url_for('view_based_feature_flag')

      app.config[FLAG_CONFIG][FEATURE_NAME] = False

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code %s' % response.status_code
      assert FEATURE_IS_OFF in response.data.decode(u'utf-8')

  def test_template_feature_flag_returns_new_code_when_flag_is_on(self):
    with self.app.test_request_context('/'):
      url = url_for('template_based_feature_flag')

      app.config[FLAG_CONFIG][FEATURE_NAME] = True

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code %s' % response.status_code
      assert FEATURE_IS_ON in response.data.decode(u'utf-8')

  def test_template_feature_flag_returns_old_code_if_flag_is_off(self):
    with self.app.test_request_context('/'):
      url = url_for('template_based_feature_flag')

      app.config[FLAG_CONFIG][FEATURE_NAME] = False

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code %s' % response.status_code
      assert FEATURE_IS_OFF in response.data.decode(u'utf-8')

  def test_feature_is_off_if_flag_doesnt_exist(self):
    with self.app.test_request_context('/'):
      url = url_for('view_based_feature_flag')

      app.config[FLAG_CONFIG] = {}

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code %s' % response.status_code
      assert FEATURE_IS_OFF in response.data.decode(u'utf-8')

  def test_raise_exception_if_flag_doesnt_exist_but_config_flag_is_set(self):

    self.app.config[FLAG_CONFIG] = {}
    self.app.config[RAISE_ERROR] = True
    self.app.debug = True

    with self.app.test_request_context('/'):
      url = url_for('view_based_feature_flag')

    try:
      self.test_client.get(url)
    except KeyError:  # assertRaises no worky for some reason :/
      pass

  def test_do_not_raise_exception_if_we_are_not_in_dev_but_feature_is_missing_and_config_flag_is_set(self):
    """If a feature doesn't exist, only raise an error if we're in dev, no matter what the config says """
    with self.app.test_request_context('/'):
      url = url_for('view_based_feature_flag')

      app.config[FLAG_CONFIG] = {}
      app.config[RAISE_ERROR] = True
      app.debug = False

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code %s' % response.status_code
      assert FEATURE_IS_OFF in response.data.decode(u'utf-8')

  def test_feature_is_off_if_config_section_doesnt_exist(self):
    with self.app.test_request_context('/'):
      url = url_for('view_based_feature_flag')

      del app.config[FLAG_CONFIG]
      assert FLAG_CONFIG not in app.config

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code %s' % response.status_code
      assert FEATURE_IS_OFF in response.data.decode(u'utf-8')

  def test_raise_exception_if_config_section_doesnt_exist_and_config_flag_is_set(self):

    del self.app.config[FLAG_CONFIG]
    self.app.config[RAISE_ERROR] = True
    self.app.debug = True

    with self.app.test_request_context('/'):
      url = url_for('view_based_feature_flag')

    try:
      self.test_client.get(url)
    except KeyError:  # assertRaises no worky for some reason :/
      pass

  def test_do_not_raise_exception_if_we_are_not_in_dev_but_config_is_missing_and_config_flag_is_set(self):
    """If the config section doesn't exist, only raise an error if we're in dev, no matter what the config says """
    with self.app.test_request_context('/'):
      url = url_for('view_based_feature_flag')

      del app.config[FLAG_CONFIG]
      app.config[RAISE_ERROR] = True
      app.debug = False

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code %s' % response.status_code
      assert FEATURE_IS_OFF in response.data.decode(u'utf-8')


class TestAppFactory(unittest.TestCase):

  def test_deferred_initialization_works(self):

    test_app = Flask(__name__)
    test_app.config[FLAG_CONFIG] = {FEATURE_NAME: True}

    feature_flagger = feature_flags.FeatureFlag()
    feature_flagger.init_app(test_app)

    with test_app.test_request_context("/"):
      # Test a couple cases to make sure we're actually exercising the same setup
      self.assertTrue(feature_flags.is_active(FEATURE_NAME))
      self.assertFalse(feature_flags.is_active("DOES_NOT_EXIST"))
