from setuptools import setup

version = '0.1'

setup(name='pyramid_breve',
      version=version,
      description="Breve template engine renderer for Pyramid",
      long_description="""Just call config.include('pyramid_breve') and use Breve templates as Pyramid view renderers""",
      keywords='pyramid breve',
      author='Alexander Kulakov',
      author_email='a.kulakov@mail.ru',
      url='http://github.com/momyc/pyramid-breve',
      license='MIT',
      packages=['pyramid_breve'],
      test_suite='pyramid_breve.tests',
      include_package_data=False,
      zip_safe=True,
      )
