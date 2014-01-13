from __future__ import with_statement

import unittest

import flask_featureflags as feature_flags


class TestEdgeCases(unittest.TestCase):

  def test_checking_is_active_outside_request_context_does_something_reasonable(self):

    self.assertFalse(feature_flags.is_active("BOGUS_FEATURE_FLAG"))

  def test_default_handler_does_something_reasonable_outside_request_context(self):
    self.assertFalse(feature_flags.AppConfigFlagHandler("BOGUS_FEATURE_FLAG"))
