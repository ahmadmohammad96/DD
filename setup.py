from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in nizmet/__init__.py
from nizmet import __version__ as version

setup(
	name="nizmet",
	version=version,
	description="Nizmet Trading",
	author="craft",
	author_email="info@craftinteractive.ae",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
