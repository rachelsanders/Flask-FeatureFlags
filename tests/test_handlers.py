from __future__ import with_statement

import unittest

from flask import url_for
from .fixtures import app, feature_setup, FEATURE_NAME, FEATURE_IS_ON, NullFlagHandler, AlwaysOnFlagHandler, AlwaysOffFlagHandler

class TestAddRemoveHandlers(unittest.TestCase):

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
    feature_setup.add_handler(NullFlagHandler)
    feature_setup.add_handler(AlwaysOnFlagHandler)
    assert len(feature_setup.handlers) == 2

  def test_can_remove_handlers(self):
    feature_setup.clear_handlers()
    feature_setup.add_handler(NullFlagHandler)
    feature_setup.add_handler(AlwaysOnFlagHandler)
    assert len(feature_setup.handlers) == 2

    feature_setup.remove_handler(NullFlagHandler)
    assert len(feature_setup.handlers) == 1

    feature_setup.remove_handler(AlwaysOnFlagHandler)
    assert len(feature_setup.handlers) == 0

  def test_removing_a_handler_that_wasnt_added_is_a_noop(self):
    feature_setup.clear_handlers()
    feature_setup.add_handler(NullFlagHandler)

    feature_setup.remove_handler(AlwaysOffFlagHandler)

    assert len(feature_setup.handlers) == 1

class TestDefaultHandlers(unittest.TestCase):

  def setUp(self):
    app.config['FEATURE_FLAGS'] = { FEATURE_NAME : True}
    app.config['TESTING'] = True
    self.app = app
    self.test_client = app.test_client()


  def test_null_handler_returns_false(self):
    feature_setup.clear_handlers()

    feature_setup.add_handler(NullFlagHandler)

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      response = self.test_client.get(url)
      assert response.status_code == 404, u'Unexpected status code'
      assert FEATURE_IS_ON not in response.data

  def test_always_false_handler_returns_false(self):
    feature_setup.clear_handlers()

    feature_setup.add_handler(AlwaysOffFlagHandler)

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      response = self.test_client.get(url)
      assert response.status_code == 404, u'Unexpected status code'
      assert FEATURE_IS_ON not in response.data

  def test_always_on_handler_returns_true(self):
    feature_setup.clear_handlers()

    feature_setup.add_handler(AlwaysOnFlagHandler)

    with self.app.test_request_context('/'):
      url = url_for('feature_decorator')

      response = self.test_client.get(url)
      assert response.status_code == 200, u'Unexpected status code'
      assert FEATURE_IS_ON in response.data



