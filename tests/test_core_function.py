
from flask import Flask, url_for, render_template_string
import flask_featureflags as feature
app = Flask(__name__)

feature_setup = feature.FeatureFlagExtension(app)

FEATURE_NAME = u"test_feature"

@app.route("/null")
def redirect_destination():
  return "OK"

@app.route("/decorator")
@feature.is_active_feature(FEATURE_NAME)
def feature_decorator():
  return "OK"

@app.route("/redirect")
@feature.is_active_feature(FEATURE_NAME, redirect_to='/null')
def redirect_with_decorator():
  return "OK"

@app.route("/view")
def view_based_feature_flag():
  if feature.is_active("test_feature"):
    return "OK"
  else:
    return "flag is off"

@app.route("/template")
def template_based_feature_flag():
  template_string = """
    {% if 'test_feature' is active_feature %}
      OK
    {% else %}
      flag is off
    {% endif %}"""

  return render_template_string(template_string)

class TestFeatureFlags():

  def setUp(self):
    app.config['FEATURE_FLAGS'] = { FEATURE_NAME : True}
    app.config['TESTING'] = True
    self.app = app
    self.test_client = app.test_client()


  def test_decorator_returns_200_if_feature_is_on(self):
    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      app.config['FEATURE_FLAGS'][FEATURE_NAME] = True

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code'
      assert 'OK' in response.data

  def test_decorator_returns_404_if_feature_is_off(self):

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      app.config['FEATURE_FLAGS'][FEATURE_NAME] = False

      response = self.test_client.get(url)
      assert response.status_code == 404, u'Unexpected status code'
      assert 'OK' not in response.data

  def test_decorator_redirects_to_url_if_redirect_is_set(self):
      with self.app.test_request_context('/'):
        url = url_for('redirect_with_decorator')

        app.config['FEATURE_FLAGS'][FEATURE_NAME] = False

        response = self.test_client.get(url)
        assert response.status_code == 302, u'Unexpected status code {0}'.format(response.status_code)
        assert response.location == url_for('redirect_destination', _external=True), u'Expected redirect to {1}, got {0} => '.format(response.location,url_for('redirect_destination') )

  def test_view_based_feature_flag_returns_normally_if_flag_is_on(self):
    with self.app.test_request_context('/'):
      url = url_for('view_based_feature_flag')

      app.config['FEATURE_FLAGS'][FEATURE_NAME] = True

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code {0}'.format(response.status_code)
      assert 'OK' in response.data

  def test_view_based_feature_flag_returns_alternate_text_if_flag_is_off(self):
    with self.app.test_request_context('/'):
      url = url_for('view_based_feature_flag')

      app.config['FEATURE_FLAGS'][FEATURE_NAME] = False

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code {0}'.format(response.status_code)
      assert "flag is off" in response.data

  def test_view_based_feature_flag_returns_normally_if_flag_is_on(self):
    with self.app.test_request_context('/'):
      url = url_for('view_based_feature_flag')

      app.config['FEATURE_FLAGS'][FEATURE_NAME] = True

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code {0}'.format(response.status_code)
      assert 'OK' in response.data

  def test_template_feature_flag_returns_normally_when_flag_is_on(self):
    with self.app.test_request_context('/'):
      url = url_for('template_based_feature_flag')

      app.config['FEATURE_FLAGS'][FEATURE_NAME] = True

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code {0}'.format(response.status_code)
      assert "OK" in response.data

  def test_template_feature_flag_returns_alternate_text_if_flag_is_off(self):
    with self.app.test_request_context('/'):
      url = url_for('template_based_feature_flag')

      app.config['FEATURE_FLAGS'][FEATURE_NAME] = False

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code {0}'.format(response.status_code)
      assert "flag is off" in response.data