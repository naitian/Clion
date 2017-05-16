from setuptools import setup

setup(
    name='clion',
    version='0.1',
    py_modules=['clion'],
    install_requires=[
        'Click',
        'requests',
        'colorama'
    ],
    entry_points='''
    [console_scripts]
    clion=clion:cli
    ''',
)
