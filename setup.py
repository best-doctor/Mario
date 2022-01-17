from typing import Optional

from setuptools import setup, find_packages


package_name = 'super_mario'


def get_version() -> Optional[str]:
    with open(f'{package_name}/__init__.py', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('__version__'):
            return line.split('=')[-1].strip().strip("'")


def get_long_description() -> str:
    with open('README.md', encoding='utf8') as f:
        return f.read()


setup(
    name=package_name,
    description=(
        'Library for separating data input, output and processing in your business application.'
    ),
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Freely Distributable',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords='project structure',
    version=get_version(),
    author='Ilya Lebedev',
    author_email='melevir@gmail.com',
    install_requires=[
        'setuptools',
        'wrapt>=1.13.3',
        'typing-inspect>=0.7.1',
    ],
    url='https://github.com/best-doctor/Mario/',
    license='MIT',
    py_modules=[package_name],
    zip_safe=False,
)
