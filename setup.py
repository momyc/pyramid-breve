from setuptools import setup, find_packages

version = '0.5.2'

setup(name='pyramid_breve',
      version=version,
      description="Breve template engine renderer for Pyramid",
      long_description="""Just call config.include('pyramid_breve') and use
      Breve templates as Pyramid view renderers""",
      keywords='pyramid breve',
      author='Alexander Kulakov',
      author_email='homo.programmerus@gmail.com',
      url='http://github.com/momyc/pyramid-breve',
      license='MIT',
      py_modules=['pyramid_breve'],
      install_requires=['breve', 'pyramid>=1.3'],
      )
