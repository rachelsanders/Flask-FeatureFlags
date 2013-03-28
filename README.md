Flask FeatureFlags
===================

This lets you enable or disable features based on configuration. Very useful when you're deploying from trunk.

You can also extend this to add your own functionality, for simple a/b testing or whitelisting.


Installation
============

Installing is simple with pip::

    $ pip install flask_featureflags


Setup
=====

Setup is also simple::

    from flask import Flask
    from flask_featureflags import FeatureFlagExtension

    app = Flask(__name__)

    feature_flags = FeatureFlagExtension(app)

In your Flask app.config, create a ``FEATURE_FLAG`` dictionary, and add any features you want as keys.

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

The redirect_to parameter is optional. If you don't specify, the url will return a 404.

If your needs are more complicated, you can check inside the view:

    from flask import Flask
    import flask_featureflags as feature

    def index():
        if feature.is_active('unfinished_feature') and some_other_condition():
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


Customizing
===========

If you want custom behavior, or to store your feature flags somewhere else, you can write your own feature flag handler.

A feature flag handler is simply a function that takes the feature name as input, and returns True (the feature is on) or False (the feature is off).

For example, if you want to enable features only on Tuesdays::

    from datetime import date

    def is_it_tuesday(feature):
      return date.today().weekday() == 2:

You can register the handler like so::

    from flask import Flask
    from flask_featureflags import FeatureFlagExtension
    from myapp import is_it_tuesday

    app = Flask(__name__)

    feature_flags = FeatureFlagExtension(app)
    feature_flags.add_handler(is_it_tuesday)

If you want to unregister a handler for any reason, you can do this::

    switches.remove_handler(is_it_tuesday)

If you try to remove a handler that was never added, the code will silently ignore you.

To clear all handlers (thus effectively turning all features off)::

    switches.clear_handlers()

