from setuptools import setup, find_packages

version = '0.1'

with open('README.rst', 'tr') as readme:
    description = readme.read()

with open('CHANGES.txt', 'tr') as changes:
    history = changes.read()
    

setup(name='hovercraft',
      version=version,
      description="Makes impress.js presentations from reStructuredText",
      long_description=description + '\n' + history,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='presentations restructuredtext',
      author='Lennart Regebro',
      author_email='regebro@gmail.com',
      url='',
      license='CC-0',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      scripts=['hovercraft/hovercraft'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'docutils',
          'lxml',
      ],
      test_suite='hovercraft.tests',
      )
