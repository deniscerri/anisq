from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.3.0'
DESCRIPTION = 'Streaming / Downloading Albanian Subtitled Anime'

# Setting up
setup(
    name="anisq",
    version=VERSION,
    author="deniscerri (Denis Çerri)",
    author_email="64997243+deniscerri@users.noreply.github.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['bs4', 'lxml', 'cloudscraper', 'requests'],
    keywords=['python', 'video', 'stream', 'anime', 'albanian'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points = {
        "console_scripts": [
            "anisq = anisq.anisq:main",
        ]
    }
)