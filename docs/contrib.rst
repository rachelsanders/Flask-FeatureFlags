Third-party modules
===================

Sometimes you don't want to use the config file to store your feature flags. You can use these premade modules
to use other backends.

SQLAlchemy
----------

You'll need Flask-SQLAlchemy::

    pip install Flask-SQLAlchemy


Then, in your app, add the ``SQLAlchemyFeatureFlags`` handler::

    from flask import Flask
    from flask.ext.sqlalchemy import SQLAlchemy
    import flask_featureflags as feature_flags
    from flask_featureflags.contrib.sqlalchemy import SQLAlchemyFeatureFlags

    app = Flask(__name__)

    db = SQLAlchemy(app)

    ff = feature_flags.FeatureFlag(app)
    ff.add_handler(SQLAlchemyFeatureFlags(db))

It will automatically create a table to store your flags in, or you can override by passing in your own model::

    ff.add_handler(SQLAlchemyFeatureFlags(db, model=MyModel))


Inline
------

``InlineFeatureFlag`` checks for any flag in app's config with `FEATURE_FLAGS_X` format,
where `X` is the name of a specific feature.

The difference between this handler and default handler is,
instead of defining flag in ``dict``-style:

.. sourcecode:: python

    FEATURE_FLAGS {
        'finished': False,
    }

the feature name must use uppercased plain string:

.. sourcecode:: python

    FEATURE_FLAGS_FINISHED = False

The motivation behind this inline handler is to interopt with other Flask extensions
that rely on environment variable, e.g. `Flask-AppConfig <https://pypi.python.org/pypi/flask-appconfig>`_.

Usage
+++++

A typical usage is as trivial as the following snippet:

.. sourcecode:: python

    from flask import Flask
    import flask_featureflags as feature_flags
    from flask_featureflags.contrib.inline import InlineFeatureFlag

    # feature flags config
    FEATURE_FLAGS_FINISHED = False

    app = Flask(__name__)
    app.config.from_object(__name__)
    ff = feature_flags.FeatureFlag(app)
    ff.add_handler(InlineFeatureFlag())

    @app.route("/")
    def index():
        return "Homepage"

    @app.route("/new")
    @feature_flags.is_active_feature("FINISHED", redirect_to="/")
    def new():
        return "New feature"


Redis
-----

You'll need to have the `Flask-Redis` to be installed::

    pip install flask_redis


Then, in your app, add the ``RedisFeatureFlags`` handler::

    from flask import Flask
    from flask_redis import FlaskRedis
    from flask_featureflags.contrib.redis import RedisFeatureFlags
    from flask_featureflags import FeatureFlag, is_active_feature


    app = Flask(__name__)
    app.config['REDIS_URL'] = 'localhost:6379'
    redis = FlaskRedis(app)
    features = FeatureFlag(app)
    features.add_handler(RedisFeatureFlags(redis))


    @app.route('/features/<feature>')
    def test_feature(feature):
        if features.check(feature):
            return '%s: active' % (feature)
        else:
            return '%s: inactive' % (feature)


    @app.route('/my_feature')
    @feature_flags.is_active_feature("my_feature")
    def handler():
        return 'ACTIVE'
