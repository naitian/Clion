from setuptools import setup

setup(
    name='clion',
    version='0.2c.dev',
    py_modules=['clion'],
    install_requires=[
        'Click',
        'requests',
        'colorama'
    ],
    entry_points='''
    [console_scripts]
    clion=clion.clion:cli
    ''',
    license='MIT',
    author='Naitian Zhou',
    author_email='2018nzhou@tjhsst.edu',
    description='A simple CLI for ion.tjhsst.edu',
)
