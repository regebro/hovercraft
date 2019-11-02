import sys
from setuptools import setup
from setuptools.command.install import install


class CustomInstall(install):
    def initialize_options(self):
        if sys.version < "3":
            print("Hovercraft requires Python 3.5 or higher.")
            sys.exit(1)

        return install.initialize_options(self)

setup(cmdclass={"install": CustomInstall})
