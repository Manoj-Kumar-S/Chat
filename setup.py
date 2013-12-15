from setuptools import setup

setup(
      name = 'pychat',
      version = '1.0.1',
      author = 'Sandeep Dasika',
      author_email = 'dasika.sandy@gmail.com',
      description = 'A simple lightweight chat client written purely in Python using the Twisted networking engine.',
      license = open('LICENSE.txt').read(),
      keywords = 'chat python',
      url = 'https://github.com/gravetii/Chat',
      packages = ['Chat',],
      long_description = open('README.md').read(),
      install_requires = ['twisted==13.2.0',],
      zip_safe = False,
      )