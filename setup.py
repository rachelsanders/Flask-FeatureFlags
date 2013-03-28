import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

try:
  README = open(os.path.join(here, 'README.rst')).read()
  CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except:
  README = ''
  CHANGES = ''


setup(
  name='Flask-FeatureFlags',
  version='0.1',
  url='https://github.com/trustrachel/Flask-FeatureFlags',
  license='BSD',
  author='Rachel Sanders',
  author_email='rachel@trustrachel.com',
  maintainer='Rachel Sanders',
  maintainer_email='rachel@trustrachel.com',
  description='Enable or disable features based on configuration',
  long_description=README + '\n\n' + CHANGES,
  zip_safe=False,
  platforms='any',
  include_package_data=True,
  packages=['flask_featureflags'],
  install_requires=[
    'Flask>=0.8',
    ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ]
)