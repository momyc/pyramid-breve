from setuptools import setup, find_packages

version = '0.3'

setup(name='pyramid_breve',
      version=version,
      description="Breve template engine renderer for Pyramid",
      long_description="""Just call config.include('pyramid_breve') and use Breve templates as Pyramid view renderers""",
      keywords='pyramid breve',
      author='Alexander Kulakov',
      author_email='a.kulakov@mail.ru',
      url='http://github.com/momyc/pyramid-breve',
      license='MIT',
      py_modules=['pyramid_breve'],
      install_requires=['breve', 'pyramid'],
      )
