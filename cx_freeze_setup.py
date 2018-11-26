import os
import sys
import utils
from cx_Freeze import setup, Executable

PYTHON_INSTALL_DIR = os.path.dirname(sys.executable)
print("PYTHON_INSTALL_DIR = " + PYTHON_INSTALL_DIR)
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, '..\\tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, '..\\tcl', 'tk8.6')
print("os.environ['TCL_LIBRARY'] = " + os.environ['TCL_LIBRARY'])
# include_files = [(os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join('lib', 'tk86t.dll')),
#                  (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'), os.path.join('lib', 'tcl86t.dll'))]

# os.environ['TCL_LIBRARY'] = r'D:\Joel\Workspace\EverDrive-Packs-Lists-Database-UI\venv\tcl\tcl8.6'
# os.environ['TK_LIBRARY'] = r'D:\Joel\Workspace\EverDrive-Packs-Lists-Database-UI\venv\tcl\tk8.6'
include_files = [r'C:\Applications\Python37\DLLs\tk86t.dll',
                 r'C:\Applications\Python37\DLLs\tcl86t.dll',
                 r'logoapp.ico']
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {   "packages": ["os"],
                        "excludes": ["py2app"],
                        "includes": ["tkinter"],
                        "include_files" : include_files
                    }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = utils.APP_NAME,
        version = utils.VERSION,
        description = "SmokeMonster everdrive pack list scripts UI",
        options = {"build_exe": build_exe_options},
        executables = [Executable("SmokeMonster-packs-UI.py", base=base, icon="logoapp.ico"),
                       Executable("build_pack.py", icon="logoapp.ico"),
                       Executable("parse_pack.py", icon="logoapp.ico")])