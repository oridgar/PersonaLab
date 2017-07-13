'''
Created on Jul 13, 2017

@author: idgar
'''
from setuptools import setup, find_packages

setup(name='personalab',
      version='0.1',
      description='personal cloud lab',
      url='http://github.com/oridgar/personalab',
      author='Or Idgar',
      author_email='idgar@virtualoco.com',
      license='GPL',
      packages=find_packages(),
      install_requires=['SQLAlchemy','os_client_config','docker','python-openstackclient'],
      zip_safe=False)
