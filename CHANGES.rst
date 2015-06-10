Changes
=======

0.1 (April 17, 2013)
--------------------

Initial public offering.

0.2 (June 20, 2013)
--------------------

Revved the version number so I could re-upload to PyPI. No real changes other than that. :/

0.3 (June 27, 2013)
-------------------

* Dropped support for Python 2.5, and added support for Python 3.3 and Flask 0.10
* Now testing with PyPy in Travis!
* Added ``RAISE_ERROR_ON_MISSING_FEATURES`` configuration to throw an error in dev if a feature flag is missing.

0.4 (April 8, 2014)
-------------------

* General code cleanup and optimization
* Adding optional redirect to is_active_feature, thank you to michaelcontento 
* Fixed syntax error in docs, thank you to iurisilvio

0.5 (August 7, 2014)
-------------------

Official support for contributed modules, thank you to iurisilvio! He contributed the first for
SQLAlchemy, so you can store your flags in the database instead.

Other contributions welcome.


0.5.1 (October 13, 2014)
----------------------

Adding the ability to have feature flags inline instead of in a dictionary, to make it easier to interoperate with other Flask extensions, e.g. Flask-AppConfig.

A big thank you to Isman Firmansyah (@iromli) for the contribution!


0.6 (June 9, 2015)
------------------

Adding contrib modules to setup.py. Thank you @iromli and @pcraig3!


