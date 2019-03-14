import os
import re
from setuptools import setup


def get_version(*file_paths):
    """Retrieves the version from specific file"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("djtest", "__init__.py")
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(name='djtest',
      version=version,
      description='Interactive test runner for Django projects',
      long_description=readme + '\n\n' + history,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django :: 2.0',
        'Topic :: Software Development :: Testing :: Unit',
      ],
      keywords='django test',
      url='https://github.com/morlandi/djtest',
      author='Mario Orlandi',
      author_email='morlandi@brainstorm.it',
      license='MIT',
      scripts=['bin/djtest'],
      packages=['djtest'],
      # install_requires=[
      #     'markdown',
      # ],
      include_package_data=False,
      zip_safe=False)
