
from setuptools import setup, find_packages

setup(
    name='code_profiler',
    version='0.0.1',
    packages=find_packages(),
    url='',
    license='MIT',
    description='Code Profiler, a python package to profile the code',
    author='Anuruddha Bandara',
    install_requires=[
        'line_profiler',  # Add 'line_profiler' to the list of dependencies
    ]
)
