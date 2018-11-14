import utils
from cx_Freeze import setup, Executable

setup(name = utils.APP_NAME,
      version = utils.VERSION,
      description = "SmokeMonster everdrive pack list scripts UI",
      executables = [Executable("SmokeMonster-packs-UI.py")])