# -*- coding: utf-8 -*-
import unittest
import mockredis
import flask_featureflags as feature_flags

from flask_featureflags.contrib.redis import RedisFeatureFlags
from tests.fixtures import app, feature_setup


class SQLAlchemyFeatureFlagTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = mockredis.mock_redis_client()
        redis_handler = RedisFeatureFlags(cls.db)
        feature_setup.add_handler(redis_handler)

    @classmethod
    def tearDownClass(cls):
        feature_setup.clear_handlers()

    def setUp(self):
        self.app_ctx = app.app_context()
        self.app_ctx.push()
        self.db.set('feature1', 'active')

    def tearDown(self):
        self.db.delete('feature1')
        self.app_ctx.pop()

    def test_flag_active(self):
        self.assertTrue(feature_flags.is_active('feature1'))

    def test_flag_not_found(self):
        self.assertFalse(feature_flags.is_active('not_found'))
