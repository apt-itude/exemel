from setuptools import setup

setup(
    name='exemel',
    version='0.1.0',
    description=(
        'Build XML documents easily and concisely using native Python data '
        'structures.'
    ),
    url='https://github.com/aptbosox/exemel',
    author='Alexander Thompson',
    author_email='aptbosox@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    py_modules=[
        'exemel'
    ],
    install_requires=[
        'lxml>=3.0'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'xmlunittest>=0.2.0'
    ]
)
