import os
from setuptools import setup, find_packages

version = '0.7.0'


def load(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(name='pyramid-breve',
      version=version,
      description="Breve template engine renderer for Pyramid Web Framework",
      long_description=load('README.rst'),
      keywords='pyramid breve',
      author='Alexander Kulakov',
      author_email='a.kulakov@mail.ru',
      url='http://github.com/momyc/pyramid-breve',
      license='MIT',
      packages=['pyramid_breve'],
      test_suite='pyramid_breve.tests',
      install_requires=['breve', 'pyramid>=1.3', 'zope.interface'],
      )
