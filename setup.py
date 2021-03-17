from setuptools import setup

setup(
    name='multi-webbing',
    version='0.1.0',    
    description='A multi-threaded libary for web scraping in python, built upon the python threading and requests modules.',
    url='https://github.com/adhardy/Multi-Webbing',
    author='Adam Hardy',
    author_email='adh167@gmail.com',
    license='BSD 2-clause',
    packages=['multi_webbing'],
    install_requires=['requests'],
    classifiers=[
    ],
)
