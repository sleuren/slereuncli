#!/usr/bin/env python3

import os
import sys
import setuptools

here = os.path.abspath(os.path.dirname(__file__))

readme = open(os.path.join(here, 'README.md')).read()
install_requires = ['configparser', 'prettytable', 'requests']

setuptools.setup(
    name='sleurencli',
    version='1.0.2',
    description='Sleuren CLI',
    long_description_content_type='text/markdown',
    long_description=readme,
    url='https://github.com/sleuren/slereuncli',
    author='Sleuren',
    author_email='hello@sleuren.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Monitoring',
    ],
    keywords='sleuren system monitoring cli',
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'sleurencli=sleurencli.sleurencli:main',
        ],
    },
    data_files=[('share/doc/sleurencli', [
        'sleuren.ini',
        'LICENSE',
        'README.md',
    ])],
)
