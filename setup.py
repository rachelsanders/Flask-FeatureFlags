import codecs
import os
import re
from setuptools import setup
from setuptools import find_packages
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


def find_version(*file_paths):
  here = os.path.abspath(os.path.dirname(__file__))
  with codecs.open(os.path.join(here, *file_paths), 'r') as f:
    version_file = f.read()
  version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                            version_file, re.M)
  if version_match:
    return version_match.group(1)
  raise RuntimeError('Unable to find version string.')


setup(
  name='Flask-FeatureFlags',
  version=find_version('flask_featureflags', '__init__.py'),
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
  packages=find_packages(exclude=["tests*"]),
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
