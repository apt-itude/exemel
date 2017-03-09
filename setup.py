from setuptools import setup

setup(
    name='exemel',
    version='0.2.2',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    py_modules=[
        'exemel'
    ],
    install_requires=[
        'future>=0.15.2',
        'lxml>=3.0'
    ]
)
