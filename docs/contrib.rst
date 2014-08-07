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

