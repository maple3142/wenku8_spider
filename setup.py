# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name='wenku8_spider',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = wenku8_spider.settings']}
)
