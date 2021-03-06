from setuptools import setup

setup(
    name='multi-webbing',
    version='0.2.0',    
    description='A multi-threaded libary for web scraping in python, built upon the python threading. Supports selenium and requests.',
    url='https://github.com/adhardy/Multi-Webbing',
    author='Adam Hardy',
    author_email='adamdhardy@icloud.com',
    license='MIT',
    packages=['multi_webbing'],
    install_requires=['requests'],
    keywords = ['web-scraping', 'multithreading', 'requests'], 
    classifiers=[
    ],
)
