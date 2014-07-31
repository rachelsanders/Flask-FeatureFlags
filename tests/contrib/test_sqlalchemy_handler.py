# -*- coding: utf-8 -*-
import unittest

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import flask_featureflags as feature_flags
from flask_featureflags.contrib.sqlalchemy import SQLAlchemyFeatureFlags


app = Flask(__name__)
db = SQLAlchemy(app)
SQLAlchemyHandler = SQLAlchemyFeatureFlags(db)

feature_setup = feature_flags.FeatureFlag(app)
feature_setup.handlers = [SQLAlchemyHandler]


class SQLAlchemyFeatureFlagTest(unittest.TestCase):

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
