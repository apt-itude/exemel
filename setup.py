from setuptools import setup

setup(
    name='exemel',
    version='0.0.1',
    description=(
        'Build XML documents easily and concisely using native Python data '
        'structures.'
    ),
    py_modules=[
        'exemel'
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
