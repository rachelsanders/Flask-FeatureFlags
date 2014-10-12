import unittest

import flask_featureflags as feature_flags
from flask_featureflags.contrib.inline import InlineFeatureFlag

from tests.fixtures import app
from tests.fixtures import feature_setup


inline_feature_flag = InlineFeatureFlag()


class InlineFeatureFlagTest(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    feature_setup.add_handler(inline_feature_flag)

  @classmethod
  def tearDownClass(cls):
    feature_setup.clear_handlers()

  def setUp(self):
    self.app_ctx = app.app_context()
    self.app_ctx.push()
    app.config["FEATURE_FLAGS_ACTIVE"] = True
    app.config["FEATURE_FLAGS_INACTIVE"] = False

  def tearDown(self):
    self.app_ctx.pop()

  def test_flag_active(self):
    self.assertTrue(feature_flags.is_active("ACTIVE"))

  def test_flag_inactive(self):
    self.assertFalse(feature_flags.is_active("INACTIVE"))

  def test_flag_not_found(self):
    self.assertFalse(feature_flags.is_active("NOT_FOUND"))

  def test_flag_not_found_raise_handler_exception(self):
    self.assertRaises(feature_flags.NoFeatureFlagFound,
                      inline_feature_flag, "NOT_FOUND")
