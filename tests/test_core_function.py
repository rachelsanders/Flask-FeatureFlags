from flask import url_for
from .fixtures import app, feature_setup, FEATURE_NAME

import flask_featureflags as feature_flags

class TestFeatureFlagCoreFunctionality():

  def setUp(self):
    app.config['FEATURE_FLAGS'] = { FEATURE_NAME : True}
    app.config['TESTING'] = True
    self.app = app
    self.test_client = app.test_client()

    # Make sure the handlers are what we expect
    feature_setup.clear_handlers()
    feature_setup.add_handler(feature_flags.AppConfigFlagHandler)

  def test_decorator_returns_the_view_if_feature_is_on(self):
    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      app.config['FEATURE_FLAGS'][FEATURE_NAME] = True

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code {0}'.format(response.status_code)
      assert 'OK' in response.data

  def test_decorator_returns_404_if_feature_is_off(self):

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      app.config['FEATURE_FLAGS'][FEATURE_NAME] = False

      response = self.test_client.get(url)
      assert response.status_code == 404, u'Unexpected status code {0}'.format(response.status_code)
      assert 'OK' not in response.data

  def test_decorator_redirects_to_url_if_redirect_is_set_and_feature_is_off(self):
      with self.app.test_request_context('/'):
        url = url_for('redirect_with_decorator')

        app.config['FEATURE_FLAGS'][FEATURE_NAME] = False

        response = self.test_client.get(url)
        assert response.status_code == 302, u'Unexpected status code {0}'.format(response.status_code)
        assert response.location == url_for('redirect_destination', _external=True), u'Expected redirect to {1}, got {0} => '.format(response.location,url_for('redirect_destination') )

  def test_view_based_feature_flag_returns_new_code_if_flag_is_on(self):
    with self.app.test_request_context('/'):
      url = url_for('view_based_feature_flag')

      app.config['FEATURE_FLAGS'][FEATURE_NAME] = True

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code {0}'.format(response.status_code)
      assert 'OK' in response.data

  def test_view_based_feature_flag_returns_old_code_if_flag_is_off(self):
    with self.app.test_request_context('/'):
      url = url_for('view_based_feature_flag')

      app.config['FEATURE_FLAGS'][FEATURE_NAME] = False

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code {0}'.format(response.status_code)
      assert "flag is off" in response.data

  def test_view_based_feature_flag_returns_new_code_if_flag_is_on(self):
    with self.app.test_request_context('/'):
      url = url_for('view_based_feature_flag')

      app.config['FEATURE_FLAGS'][FEATURE_NAME] = True

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code {0}'.format(response.status_code)
      assert 'OK' in response.data

  def test_template_feature_flag_returns_new_code_when_flag_is_on(self):
    with self.app.test_request_context('/'):
      url = url_for('template_based_feature_flag')

      app.config['FEATURE_FLAGS'][FEATURE_NAME] = True

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code {0}'.format(response.status_code)
      assert "OK" in response.data

  def test_template_feature_flag_returns_old_code_if_flag_is_off(self):
    with self.app.test_request_context('/'):
      url = url_for('template_based_feature_flag')

      app.config['FEATURE_FLAGS'][FEATURE_NAME] = False

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code {0}'.format(response.status_code)
      assert "flag is off" in response.data