import sys
from setuptools import setup, find_packages

sys.path.insert(0, '.')

import pkg_info  # noqa: E402


setup(
    name='panda-analy',
    version=pkg_info.release_version,
    description='PanDA Analysis',
    long_description='''This package contains PanDA Analysis''',
    license='GPL',
    author='FaHui Lin',
    author_email='fahui.lin@cern.ch',
    url='https://github.com/mightqxc/panda-analy.git',
    python_requires='>=3.6',
    packages=find_packages(where='lib'),
    package_dir = {'': 'lib'},
    install_requires=[
                      'sqlalchemy',
                      'mysqlclient',
                      'pandas',
                      'PyYAML',
                      ],

    # optional pip dependencies
    extras_require={
        },

    data_files=[
            # config
            ('etc', ['templates/panda-analy_config.yaml.template',
                            ]
                ),
        ],

    scripts=[
             ]
    )
