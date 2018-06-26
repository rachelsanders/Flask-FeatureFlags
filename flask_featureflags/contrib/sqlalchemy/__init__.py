from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm.exc import NoResultFound
from flask import current_app
from flask_featureflags import NoFeatureFlagFound, log


class SQLAlchemyFeatureFlags(object):

  def __init__(self, db, model=None):
    if not model:
      model = self._make_model(db)
    self.model = model

  def __call__(self, feature=None):
    if not current_app:
      log.warn(u"Got a request to check for {feature} but we're outside the request context. Returning False".format(feature=feature))
      return False

    try:
      return self.model.check(feature)
    except NoResultFound:
      raise NoFeatureFlagFound()

  def _make_model(self, db):

    class FeatureFlag(db.Model):
      id = Column(Integer, primary_key=True)
      feature = Column(String(255), nullable=False, unique=True)
      is_active = Column(Boolean, default=False)

      @classmethod
      def check(cls, feature):
        r = cls.query.filter_by(feature=feature).one()
        return r.is_active

    return FeatureFlag
