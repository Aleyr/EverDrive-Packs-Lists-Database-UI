"""
 py2app/py2exe build script for MyApplication.

 Will automatically ensure that all build prerequisites are available
 via ez_setup

 Usage (Mac OS X):
     python setup.py py2app

 Usage (Windows) does not work on Python 3.5+, but I leave it here:
     python setup.py py2exe
"""

# import ez_setup
import sys
import utils
from setuptools import setup

NAME = utils.APP_NAME
MAIN_SCRIPT = 'SmokeMonster-packs-UI.py'
APP = [MAIN_SCRIPT]
DATA_FILES = ['LICENSE']
OPTIONS = {
	'iconfile':'logoapp.icns',
	'argv_emulation': True,
	'packages': ['certifi'],

}

if sys.platform == 'darwin':
    extra_options = dict(
        setup_requires=['py2app'],
        app=APP,
		data_files=DATA_FILES,
        # Cross-platform applications generally expect sys.argv to
        # be used for opening files.
        options=dict(py2app=OPTIONS),
    )
elif sys.platform == 'win32':
	# ez_setup.use_setuptools()
    extra_options = dict(
        setup_requires=['py2exe'],
        app=APP,
    )
else:
    extra_options = dict(
        # Normally unix-like platforms will use "setup.py install"
        # and install the main script as such
        scripts=[MAIN_SCRIPT],
    )

setup(
    name="MyApplication",
    **extra_options
)