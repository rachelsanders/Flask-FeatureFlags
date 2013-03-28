Flask FeatureFlags
===================

This allows you to enable or disable features based on configuration


Installation
============

Installing is simple with pip::

    $ pip install flask_featureflags


Setup
=====

Setup is simple::

    from flask import Flask
    from flask_featureflags import FeatureFlagExtension

    app = Flask(__name__)

    feature_flags = FeatureFlagExtension(app)


Adding feature flags
--------------------

By default, Flask-FeatureFlags check your application configuration for enabled flags.

To create new feature flags, create a ``FEATURE_FLAG`` dictionary in your app.config.

For example, to have 'unfinished_feature' hidden in production but active in development::

    class ProductionConfig(Config):

        FEATURE_FLAGS = {
            'unfinished_feature' : False,
        }


    class DevelopmentConfig(Config):

        FEATURE_FLAGS = {
          'unfinished_feature' : True,
        }

If a feature doesn't exist, it is assumed to be inactive.

Custom feature flag handlers
----------------------------

Adding custom feature flag handlers is easy.

For example, say you want to store your feature flags in your database. You write a function called ``is_feature_active_in_db`` that
checks the feature flag in the db given the name. You can register the handler like so::

    from flask import Flask
    from flask_featureflags import FeatureFlagExtension

    app = Flask(__name__)

    feature_flags = FeatureFlagExtension(app)
    switches.register_handler(is_feature_active_in_db)

When feature flags are checked, your function will be called with the name of the feature flag being checked. Your function should return either True or False::

    def is_feature_active_in_db(switch):
      # check the db here...
      return True

If you want to unregister a handler for any reason, you can do this::

    switches.unregister_handler(is_feature_active_in_db)

Unregistering a handler that was never added is a no-op.

If you want to clear all handlers::

    switches.clear_handlers()

Usage
=====

Controllers/Views
-----------------

If you want to protect an entire view::

    from flask import Flask
    import flask_featureflags as feature

    @feature.is_active_feature('unfinished_feature', redirect_to='/old/url')
    def index():
        # unfinished view code here

The redirect_to parameter is optional. If you don't specify, the url will return a 404 instead.

If your needs are more complicated, you can check inside the view:

    from flask import Flask
    import flask_featureflags as switch

    def index():
        if feature.is_active('unfinished_feature'):
            # do new stuff
        else:
            # do old stuff

Templates
---------

You can also check for features in template code::

    {% if 'unfinished_feature' is active_feature %}
        new behavior here!
    {% else %}
        old behavior...
    {% endif %}
