from flask import current_app
from flask.ext.featureflags import NoFeatureFlagFound, log


class RedisFeatureFlags(object):

    def __init__(self, db):
        self.db = db

    def __call__(self, feature):
        if not current_app:
            log.warn(
                u"Got a request to check for {feature} but we're outside the request"
                u"context. Returning False".format(feature=feature))
            return False
        if self.db.get(feature):
            return True
        raise NoFeatureFlagFound
