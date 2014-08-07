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