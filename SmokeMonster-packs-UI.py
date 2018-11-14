#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graphical User Iterface for build_pack and parse_pack scripts.
"""

import argparse
import configparser

from tkinter import *
from tkinter import ttk

from gui_pack import App
from utils import *
from utils import _is_pack_scripts_folder
from buildframe import *
from parseframe import *
from menubar import *
from textmessage import *
from autoresized_notebook import Autoresized_Notebook
from pathlib import Path
from dialog import *


__author__ = "Aleyr"
__date__ = "2018/11/10"
__version__ = "$Revision: 0.9.2"

# *********************************************************************#
#                                                                      #
#                            Functions                                 #
#                                                                      #
# *********************************************************************#


def main(folder, build_file, parse_file):
    app = App(folder, build_file, parse_file)
    app.title("EverDrive-Packs-Lists-Database")
    if not app.folder:
        app.lower()
        ssp = ScriptSelectionDialog(app, "Set Pack Scripts Folder")
    app.mainloop()


# *********************************************************************#
#                                                                      #
#                              Body                                    #
#                                                                      #
# *********************************************************************#


if __name__ == '__main__':
    args = {
        "scripts_folder": None,
        "save": False
    }

    folder = None
    build_file = None
    parse_file = None
    ini_file = get_ini_file()

    # Path pass as a parameter, used instead of the ini file value
    if is_pack_scripts_folder(args["scripts_folder"]):
        folder = Path(args["scripts_folder"])
        if args["save"]:
            save_ini_file(ini_file, "UI",
                          {"scripts_folder": get_abs_path(folder)})

    elif ini_file.exists():
        config = configparser.ConfigParser()
        config.read_file(ini_file.open())
        folder = Path(config["UI"]["scripts_folder"])

    # If the pack script folder was not provided verify current folder and path
    elif _is_pack_scripts_folder(Path()):
        folder = Path()

    # Look for the packs script on the parent folder
    elif _is_pack_scripts_folder(Path() /
                                 "../EverDrive-Packs-Lists-Database/"):
        folder = Path(Path() / "../EverDrive-Packs-Lists-Database/")

    if folder:
        build_file, parse_file = get_pack_scripts_paths(folder)

    main(folder, build_file, parse_file)
