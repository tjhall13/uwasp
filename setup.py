from setuptools import setup, find_packages

VERSION = '0.1.0.dev0'

setup(
    name='uwasp',
    version=VERSION,
    url='https://github.com/tjhall13/uwasp',
    author='Trevor Hall',
    author_email='trevor.jacob.hall@gmail.com',
    description=("Asynchronous uwsgi websocket network library"),
    long_description=open("README.md").read(),
    download_url="https://github.com/tjhall13/uwasp",
    packages=find_packages(),
    license=open('LICENSE').read(),
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
