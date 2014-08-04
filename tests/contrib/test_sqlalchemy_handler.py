# -*- coding: utf-8 -*-
import unittest

from flask.ext.sqlalchemy import SQLAlchemy

import flask_featureflags as feature_flags
from flask_featureflags.contrib.sqlalchemy import SQLAlchemyFeatureFlags

from tests.fixtures import app, feature_setup

db = SQLAlchemy(app)
SQLAlchemyHandler = SQLAlchemyFeatureFlags(db)


class SQLAlchemyFeatureFlagTest(unittest.TestCase):

  @classmethod
  def setupClass(cls):
    feature_setup.handlers = [SQLAlchemyHandler]

  @classmethod
  def tearDownClass(cls):
    feature_setup.clear_handlers()

  def setUp(self):
    self.app_ctx = app.app_context()
    self.app_ctx.push()
    db.create_all()
    m1 = SQLAlchemyHandler.model(feature='active', is_active=True)
    m2 = SQLAlchemyHandler.model(feature='inactive')
    db.session.add_all([m1, m2])
    db.session.commit()

  def tearDown(self):
    db.session.close()
    db.drop_all()
    self.app_ctx.pop()

  def test_flag_active(self):
    self.assertTrue(feature_flags.is_active('active'))

  def test_flag_inactive(self):
    self.assertFalse(feature_flags.is_active('inactive'))

  def test_flag_not_found(self):
    self.assertFalse(feature_flags.is_active('not_found'))

  def test_flag_not_found_raise_handler_exception(self):
    self.assertRaises(feature_flags.NoFeatureFlagFound,
                      SQLAlchemyHandler, 'not_found')
