from setuptools import setup, find_packages

version = '1.2.dev0'

with open('README.rst', 'rt') as readme:
    description = readme.read()

with open('CHANGES.txt', 'rt') as changes:
    history = changes.read()
    

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
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
                   ], 
      keywords='presentations restructuredtext',
      author='Lennart Regebro',
      author_email='regebro@gmail.com',
      url='https://github.com/regebro/hovercraft',
      license='CC0 1.0 Universal',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'docutils >= 0.9',
          'lxml>=3.1.0',
          'svg.path',
          'pygments',
          'configparser'
      ],
      tests_require=[
          'manuel',
      ],
      test_suite='hovercraft.tests',
      entry_points={
               'console_scripts': [
                   'hovercraft = hovercraft:main',
               ],
      },
)
