import os
from setuptools import setup
from sys import argv

here = os.path.abspath(os.path.dirname(__file__))

try:
  README = open(os.path.join(here, 'README.md')).read()
  CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except:
  README = ''
  CHANGES = ''

install_requires = ["Flask"]

if "develop" in argv:
  install_requires.append('Sphinx')
  install_requires.append('Sphinx-PyPI-upload')

setup(
  name='Flask-FeatureFlags',
  version='0.1',
  url='https://github.com/trustrachel/Flask-FeatureFlags',
  license='Apache',
  author='Rachel Sanders',
  author_email='rachel@trustrachel.com',
  maintainer='Rachel Sanders',
  maintainer_email='rachel@trustrachel.com',
  description='Enable or disable features in Flask apps based on configuration',
  long_description=README + '\n\n' + CHANGES,
  zip_safe=False,
  test_suite="tests",
  platforms='any',
  include_package_data=True,
  packages=['flask_featureflags'],
  install_requires=[
    'Flask',
    ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ]
)
