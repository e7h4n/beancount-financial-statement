"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""


import pathlib
from setuptools import setup, find_packages
from beanstatement import __version__

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='beancount-financial-statement',

    version=__version__,

    description='A report generator for beancount financial statement.',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/e7h4n/beancount-financial-statement',

    author='e7h4n',

    author_email='ethan.pw@icloud.com',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Accounting',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='beancount, financial statement',

    package_dir={'beancount-financial-statement': 'src'},

    python_requires='>=3.6, <4',

    packages=find_packages(exclude=['experiments*']),

    package_data = {
        'beanstatement': ['templates/*.mustache'],
    },

    install_requires=[
        'logzero==1.7.0',
        'click==8.0.1',
        'pystache==0.6.0',
        'beancount==2.3.6',
    ],

    extras_require={
        'dev': [],
        'test': [
            'coverage',
            'pycodestyle',
            'pyflakes',
            'pylint',
            'flake8',
            'mypy',
            'pytest',
            'python-coveralls',
            'beautifulsoup4'
        ],
    },

    entry_points={
        'console_scripts': [
            'bean-statement=beanstatement.scripts.main:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/e7h4n/beancount-financial-statement/issues',
        'Source': 'https://github.com/e7h4n/beancount-financial-statement/',
    },
)
