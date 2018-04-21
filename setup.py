from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='djtest',
      version='0.0.1',
      description='Interactive test runner for Django projects',
      long_description=readme(),
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
