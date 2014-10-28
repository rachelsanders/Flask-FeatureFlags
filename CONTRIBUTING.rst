Contributing
============

Hi! Thanks so much for wanting to contribute.

Setting up for development
--------------------------

There's a few extra steps to set up for development.

Installing from source
``````````````````````

To install in development mode from source, download the source code, then run this::

    python setup.py develop

Installing libraries
````````````````````

To do development work, you'll need a few more libraries::

    pip install -r requirements-dev.txt
    pip install -r requirements-contrib.txt


Running the tests
`````````````````

Make sure you have the development libraries installed, then run::

    py.test tests

Building documentation
``````````````````````

Make sure you have the development libraries installed, then do::

    cd docs
    make html

The generated documentation will be in ``docs/_build/html/``.

Guidelines
----------

Style guide
```````````

The code follows `PEP8
<http://www.python.org/dev/peps/pep-0008/>`_ with the following exceptions:

* Indentation is 2 spaces (no tabs)
* Line length: use your best judgment. (We all have big monitors now, no need to limit to 80 columns.)

Your code should pass `flake8
<http://flake8.readthedocs.org/>`_ unless readability is hurt. Configuration is in ``setup.cfg``.

Supported versions
```````````````````

Your code should be compatible with Python 2.6, 2.7, and 3.3+, and Flask 0.8+. Travis CI will test all that for you
automatically.

Tests
`````

Submitted code should have tests covering the code submitted, and your code should pass the travis build.

If possible, use the fixtures in test/fixtures.py - there's a sample app with all the functionality that you can
use to test on.

Creating a contrib module
-------------------------

If you store your flags somewhere other than the config file, and want to share your code with others, fantastic!

Here's a couple guidelines:

1. Contrib code goes in ``flask_featureflags/contrib``

2. Tests for contrib modules go in ``tests/contrib``

3. Add a description and a quick example of how to use your module in ``docs/contrib.rst``

4. If your code has any package requirements, please put them in ``requirements-contrib.txt``

Thanks for contributing!
