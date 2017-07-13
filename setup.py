'''
Created on Jul 13, 2017

@author: idgar
'''
from setuptools import setup

setup(name='personal-lab',
      version='0.1',
      description='personal cloud lab',
      url='http://github.com/oridgar/personalab',
      author='Or Idgar',
      author_email='idgar@virtualoco.com',
      license='GPL',
      packages=['personal-lab'],
      install_requires=['SQLAlchemy'],
      zip_safe=False)