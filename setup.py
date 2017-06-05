from setuptools import setup

setup(
	name = 'THSF Radio',
	version = '1.0.0',
	author = 'Thomas Sauze',
	author_email = 'thomas.sauze@seasonlabs.com',
	description = ("A simple webapp to quickly send RDS data"
					"to the RPI."),
	license = "BSD",
	packages = ['flask', 'flask-sqlalchemy', 'flask-wtf']
)