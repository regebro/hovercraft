from setuptools import setup, find_packages

version = '1.0'

with open('README.rst', 'rt') as readme:
    description = readme.read()

with open('CHANGES.txt', 'rt') as changes:
    history = changes.read()
    

setup(name='hovercraft',
      version=version,
      description="Makes impress.js presentations from reStructuredText",
      long_description=description + '\n' + history,
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 4 - Beta',
                   'Topic :: Multimedia :: Graphics :: Presentation',
                   'Topic :: Text Processing',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   ], 
      keywords='presentations restructuredtext',
      author='Lennart Regebro',
      author_email='regebro@gmail.com',
      url='https://github.com/regebro/hovercraft',
      license='CC-0',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'docutils',
          'lxml',
          'svg.path',
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
