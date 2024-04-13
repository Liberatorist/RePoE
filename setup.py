import os
from setuptools import find_packages, setup
import sys

# Package meta-data.
NAME = "RePoE-Liberatorist"
DESCRIPTION = "Repository of Path of Exile resources for tool developers"
URL = "https://github.com/Liberatorist/RePoE"
EMAIL = ""
AUTHOR = "Liberatorist"
REQUIRES_PYTHON = ">=3.11.0"
VERSION = "3.24.6"

# What packages are required for this module to be executed?
REQUIRED = []

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}
# traverse RePoE/data and add all files to data_files
data_files = []

for file in os.listdir("RePoE/data"):
    # not packing all stat translations for now
    if file.endswith(".min.json"):
        data_files.append(os.path.join("RePoE/data", file))
directory = "/".join(sys.prefix.split("/")[:-2]) + "/RePoE/data"

wiki_data_files = []

for file in os.listdir("RePoE/wikidata"):
    # not packing all stat translations for now
    if file.endswith(".min.json"):
        wiki_data_files.append(os.path.join("RePoE/wikidata", file))

wiki_directory = "/".join(sys.prefix.split("/")[:-2]) + "/RePoE/wikidata"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=["RePoE.poe_types", "RePoE.util", "RePoE.wikidata.__init__"],
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    license="proprietary",

    data_files=[
        (directory, data_files),
        (wiki_directory, wiki_data_files),
    ]

)
