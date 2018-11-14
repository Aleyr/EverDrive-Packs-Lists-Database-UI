import sys
import utils
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["py2app"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = utils.APP_NAME,
        version = utils.VERSION,
        description = "SmokeMonster everdrive pack list scripts UI",
        options = {"build_exe": build_exe_options},
        executables = [Executable("SmokeMonster-packs-UI.py", base=base)])