from setuptools import setup

setup(
    name='dict2xml',
    version='0.0.1',
    description='Converts a dictionary into an XML document',
    py_modules=[
        'dict2xml'
    ],
    install_requires=[
        'lxml'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'xmlunittest'
    ]
)
