from flask import current_app
from flask_featureflags import FEATURE_FLAGS_CONFIG
from flask_featureflags import NoFeatureFlagFound
from flask_featureflags import log


class InlineFeatureFlag(object):
  def __call__(self, feature):
    if not current_app:
      log.warn(u"Got a request to check for {feature} but we're outside the request context. Returning False".format(feature=feature))
      return False

    feature_cfg = "{prefix}_{feature}".format(prefix=FEATURE_FLAGS_CONFIG, feature=feature)

    try:
      return current_app.config[feature_cfg]
    except KeyError:
      raise NoFeatureFlagFound()
