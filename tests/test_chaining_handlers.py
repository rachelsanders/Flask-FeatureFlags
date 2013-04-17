from __future__ import with_statement

import unittest

from flask import url_for
from .fixtures import app, feature_setup, FEATURE_NAME, AlwaysOnFlagHandler, AlwaysOffFlagHandler, FEATURE_IS_ON


class TestHandlerChaining(unittest.TestCase):

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
      assert FEATURE_IS_ON not in response.data

  def test_if_any_handler_returns_true_the_feature_flag_is_on(self):

    feature_setup.clear_handlers()
    feature_setup.add_handler(lambda feature: False)
    feature_setup.add_handler(lambda feature: True)

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code'
      assert FEATURE_IS_ON in response.data

  def test_the_first_handler_to_return_true_stops_the_chain(self):

    feature_setup.clear_handlers()
    feature_setup.add_handler(AlwaysOnFlagHandler)
    feature_setup.add_handler(AlwaysOffFlagHandler)

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code'
      assert FEATURE_IS_ON in response.data

  def test_raising_exception_stops_the_chain_and_returns_false(self):

    feature_setup.clear_handlers()
    feature_setup.add_handler(AlwaysOffFlagHandler)
    feature_setup.add_handler(AlwaysOnFlagHandler)

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      response = self.test_client.get(url)
      assert response.status_code == 404, u'Unexpected status code'
      assert FEATURE_IS_ON not in response.data

  def test_if_no_handler_returns_true_the_chain_returns_false(self):

    feature_setup.clear_handlers()
    feature_setup.add_handler(lambda feature: 1==2)
    feature_setup.add_handler(lambda feature: 3>4)

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      response = self.test_client.get(url)
      assert response.status_code == 404, u'Unexpected status code'
      assert FEATURE_IS_ON not in response.data

