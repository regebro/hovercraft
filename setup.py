from io import open
from setuptools import setup, find_packages
from setuptools.command.install import install
import sys

version = '2.6'

with open('README.rst', 'rt', encoding='utf8') as readme:
    description = readme.read()

with open('CHANGES.txt', 'rt', encoding='utf8') as changes:
    history = changes.read()

class CustomInstall(install):
    def initialize_options(self):
        if sys.version < '3':
            print("Hovercraft requires Python 3.5 or higher.")
            sys.exit(1)

        return install.initialize_options(self)

setup(name='hovercraft',
      version=version,
      description="Makes impress.js presentations from reStructuredText",
      long_description=description + '\n' + history,
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Topic :: Multimedia :: Graphics :: Presentation',
                   'Topic :: Text Processing',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3 :: Only',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'License :: OSI Approved :: MIT License',
                   ],
      keywords='presentations restructuredtext',
      author='Lennart Regebro',
      author_email='regebro@gmail.com',
      url='https://github.com/regebro/hovercraft',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'docutils >= 0.9',
          'lxml>=3.1.0',
          'svg.path',
          'pygments',
          'watchdog',
      ],
      tests_require=[
          'manuel',
      ],
      test_suite='tests',
      entry_points={
               'console_scripts': [
                   'hovercraft = hovercraft:main',
               ],
      },
      cmdclass={'install': CustomInstall}
)
