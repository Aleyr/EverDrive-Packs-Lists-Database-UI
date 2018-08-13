#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graphical User Iterface for build_pack and parse_pack scripts.
"""

import argparse

from tkinter import *
from tkinter import ttk

from utils import *
from buildframe import *
from parseframe import *
from menubar import *
from textmessage import *
from autoresized_notebook import Autoresized_Notebook
from pathlib import Path


__author__ = "aleyr"
__date__ = "2018/08/03"
__version__ = "$Revision: 0.8"


BUILD_SCRIPT_NAME = "build_pack.py"
PARSE_SCRIPT_NAME = "parse_pack.py"


# *********************************************************************#
#                                                                      #
#                             Classes                                  #
#                                                                      #
# *********************************************************************#


class App(Tk):
    def __init__(self, build_file, parse_file, *args, **kwargs):
        # call the parent constructor
        Tk.__init__(self, *args, **kwargs)

        self.build_file = build_file
        self.parse_file = parse_file
        self.text_label = StringVar()

        tab_control = Autoresized_Notebook(self)

        build_frame = BuildFrame(self, padding="3 3 12 12")
        build_frame.pack(side="top", fill="both", expand=True)
        tab_control.add(build_frame, text="Build Pack", sticky=N)

        parse_frame = ParseFrame(self, padding="3 3 12 12")
        parse_frame.pack(side="top", fill="both", expand=True)
        tab_control.add(parse_frame, text="Parse ROMs Folder", sticky=N)

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


# *********************************************************************#
#                                                                      #
#                            Functions                                 #
#                                                                      #
# *********************************************************************#


def is_pack_scripts_folder(scripts_folder):
    out = False
    if args.scripts_folder:
        folder = Path(scripts_folder)

        if folder.exists() and folder.is_dir():
            build_file = folder / BUILD_SCRIPT_NAME
            parse_file = folder / PARSE_SCRIPT_NAME

            if build_file.exists() and parse_file.exists():
                out = True

    return out


def get_pack_scripts_paths(scripts_folder):
    folder = Path(scripts_folder)
    build_file = folder / BUILD_SCRIPT_NAME
    parse_file = folder / PARSE_SCRIPT_NAME

    return (build_file, parse_file)


def main(build_file, parse_file):
    app = App(build_file, parse_file)
    app.title("EverDrive-Packs-Lists-Database")
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
                        help="set scripts folder")

    args = parser.parse_args()

    build_file = None
    parse_file = None
    if is_pack_scripts_folder(args.scripts_folder):
        build_file, parse_file = get_pack_scripts_paths(args)

    main(build_file, parse_file)
