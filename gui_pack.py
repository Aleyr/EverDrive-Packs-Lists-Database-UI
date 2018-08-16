#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graphical User Iterface for build_pack and parse_pack scripts.
"""

import argparse
import configparser

from tkinter import *
from tkinter import ttk

from utils import *
from utils import _is_pack_scripts_folder
from buildframe import *
from parseframe import *
from menubar import *
from textmessage import *
from autoresized_notebook import Autoresized_Notebook
from pathlib import Path
from dialog import Dialog


__author__ = "aleyr"
__date__ = "2018/08/03"
__version__ = "$Revision: 0.8"


# *********************************************************************#
#                                                                      #
#                             Classes                                  #
#                                                                      #
# *********************************************************************#


class App(Tk):
    def __init__(self, folder, build_file, parse_file, *args, **kwargs):
        # call the parent constructor
        Tk.__init__(self, *args, **kwargs)

        self.folder = folder
        self.build_file = build_file
        self.parse_file = parse_file
        self.text_label = StringVar()

        tab_control = Autoresized_Notebook(self)

        self.build_frame = BuildFrame(self, padding="3 3 12 12")
        self.build_frame.pack(side="top", fill="both", expand=True)
        tab_control.add(self.build_frame, text="Build Pack", sticky=N)

        self.parse_frame = ParseFrame(self, padding="3 3 12 12")
        self.parse_frame.pack(side="top", fill="both", expand=True)
        tab_control.add(self.parse_frame, text="Parse ROMs Folder", sticky=N)

        tab_control.pack(side="top", fill="both", expand=True)

        # status_frame = ttk.Frame(self, padding="3 3 3 3")
        status_label = ttk.Label(self, borderwidth=2, relief="ridge",
                                 textvariable=self.text_label)
        status_label.pack(fill="both", expand=True)
        # status_frame.pack(fill="both", expand=True)

        self.progress = ttk.Progressbar(self, orient="horizontal",
                                        mode="determinate")
        self.progress.pack(fill="both", expand=True)

        menu_bar = MenuBar(self)

        self.config(menu=menu_bar)

    def toggle_action_buttons(self, enable):
        if enable:
            self.build_frame.change_state('normal',
                                          [self.build_frame.build_btn])
            self.parse_frame.change_state('normal',
                                          [self.parse_frame.parse_btn])
        else:
            self.build_frame.change_state('disabled',
                                          [self.build_frame.build_btn])
            self.parse_frame.change_state('disabled',
                                          [self.parse_frame.parse_btn])


# *********************************************************************#
#                                                                      #
#                            Functions                                 #
#                                                                      #
# *********************************************************************#


def main(folder, build_file, parse_file):
    app = App(folder, build_file, parse_file)
    app.title("EverDrive-Packs-Lists-Database")
    if not app.folder:
        Dialog(app, "Set Pack Scripts Folder")
    app.mainloop()


# *********************************************************************#
#                                                                      #
#                              Body                                    #
#                                                                      #
# *********************************************************************#


if __name__ == '__main__':
    """
    Parse arguments from command line.
    """
    parser = argparse.ArgumentParser(
        description="use a database to identify and organize files.")

    parser.add_argument("-s", "--scripts_folder",
                        dest="scripts_folder",
                        default=None,
                        help="Provides the folder where the pack scripts"
                             "are located.")

    parser.add_argument("--save",
                        dest="save",
                        default=False,
                        help="Saves the provided pack script folder to"
                             "the ini file.")

    args = parser.parse_args()

    folder = None
    build_file = None
    parse_file = None
    ini_file = get_ini_file()

    # Path pass as a parameter, used instead of the ini file value
    if is_pack_scripts_folder(args.scripts_folder):
        folder = Path(args.scripts_folder)
        if args.save:
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
