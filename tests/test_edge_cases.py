from __future__ import with_statement

import unittest

from flask import Flask
import flask_featureflags as feature_flags


class TestOutsideRequestContext(unittest.TestCase):

  def test_checking_is_active_outside_request_context_returns_false(self):

    self.assertFalse(feature_flags.is_active("BOGUS_FEATURE_FLAG"))

  def test_default_handler_returns_false_outside_request_context(self):

    self.assertFalse(feature_flags.AppConfigFlagHandler("BOGUS_FEATURE_FLAG"))


class TestBadlyConfiguredApplication(unittest.TestCase):

  def test_checking_is_active_on_an_app_that_was_never_set_up_raises_assertion(self):
    # This simulates somebody calling is_active on a Flask app that was never
    # set up with this extension. Since this is somebody likely trying to install it,
    # make sure they get a nice, helpful error message

    test_app = Flask(__name__)

    with test_app.test_request_context("/"):
      self.assertRaises(AssertionError, feature_flags.is_active, "BOGUS_FEATURE_FLAG")

  def test_running_default_handler_on_app_that_was_never_set_up_returns_false(self):
    # This case should only happen if somebody's being especially creative, but
    # I want to make sure it's well-behaved anyways.

    test_app = Flask(__name__)

    with test_app.test_request_context("/"):
      self.assertRaises(feature_flags.NoFeatureFlagFound,
                        feature_flags.AppConfigFlagHandler, "BOGUS_FEATURE_FLAG")
