from flask import Flask, url_for, render_template_string
import flask_featureflags as feature
app = Flask(__name__)

feature_setup = feature.FeatureFlagExtension(app)

FEATURE_NAME = u"test_feature"

@app.route("/decorator")
@feature.is_active_feature(FEATURE_NAME)
def feature_decorator():
  return "OK"

class TestAddRemoveHandlers():

  def setUp(self):
    app.config['FEATURE_FLAGS'] = { FEATURE_NAME : True}
    app.config['TESTING'] = True
    self.app = app
    self.test_client = app.test_client()

  def test_can_clear_handlers(self):
    feature_setup.clear_handlers()
    assert len(feature_setup.handlers) == 0

  def test_can_add_handlers(self):
    feature_setup.clear_handlers()
    feature_setup.add_handler(feature.NullFlagHandler)
    feature_setup.add_handler(feature.AlwaysOnFlagHandler)
    assert len(feature_setup.handlers) == 2

  def test_can_remove_handlers(self):
    feature_setup.clear_handlers()
    feature_setup.add_handler(feature.NullFlagHandler)
    feature_setup.add_handler(feature.AlwaysOnFlagHandler)
    assert len(feature_setup.handlers) == 2

    feature_setup.remove_handler(feature.NullFlagHandler)
    assert len(feature_setup.handlers) == 1

    feature_setup.remove_handler(feature.AlwaysOnFlagHandler)
    assert len(feature_setup.handlers) == 0

  def test_removing_a_handler_that_wasnt_added_is_a_noop(self):
    feature_setup.clear_handlers()
    feature_setup.add_handler(feature.NullFlagHandler)

    feature_setup.remove_handler(lambda: True)

    assert len(feature_setup.handlers) == 1

class TestDefaultHandlers():

  def setUp(self):
    app.config['FEATURE_FLAGS'] = { FEATURE_NAME : True}
    app.config['TESTING'] = True
    self.app = app
    self.test_client = app.test_client()


  def test_null_handler_returns_false(self):
    feature_setup.clear_handlers()

    feature_setup.add_handler(feature.NullFlagHandler)

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      response = self.test_client.get(url)
      assert response.status_code == 404, u'Unexpected status code'
      assert 'OK' not in response.data

  def test_always_false_handler_returns_false(self):
    feature_setup.clear_handlers()

    feature_setup.add_handler(feature.AlwaysOffFlagHandler)

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      response = self.test_client.get(url)
      assert response.status_code == 404, u'Unexpected status code'
      assert 'OK' not in response.data

  def test_always_on_handler_returns_true(self):
    feature_setup.clear_handlers()

    feature_setup.add_handler(feature.AlwaysOnFlagHandler)

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code'
      assert 'OK' in response.data


class TestHandlerChaining():

  def setUp(self):
    app.config['FEATURE_FLAGS'] = { FEATURE_NAME : True}
    app.config['TESTING'] = True
    self.app = app
    self.test_client = app.test_client()


  def test_feature_flags_are_off_if_no_handlers_set(self):

    feature_setup.clear_handlers()

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      response = self.test_client.get(url)
      assert response.status_code == 404, u'Unexpected status code'
      assert 'OK' not in response.data


  def test_if_any_handler_returns_true_the_feature_flag_is_on(self):

    feature_setup.clear_handlers()
    feature_setup.add_handler(lambda switch: False)
    feature_setup.add_handler(lambda switch: True)

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code'
      assert 'OK' in response.data

  def test_the_first_handler_to_return_true_stops_the_chain(self):

    feature_setup.clear_handlers()
    feature_setup.add_handler(feature.AlwaysOnFlagHandler)
    feature_setup.add_handler(feature.AlwaysOffFlagHandler)

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code'
      assert 'OK' in response.data

  def test_raising_exception_stops_the_chain(self):

    feature_setup.clear_handlers()
    feature_setup.add_handler(feature.AlwaysOffFlagHandler)
    feature_setup.add_handler(feature.AlwaysOnFlagHandler)

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      response = self.test_client.get(url)
      assert response.status_code == 404, u'Unexpected status code'
      assert 'OK' not in response.data

