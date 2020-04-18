#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graphical User Iterface for build_pack and parse_pack scripts.
"""


import configparser
import os
import sys

from tkinter import *
from tkinter import filedialog as fd
from pathlib import Path
from platform import system


__author__ = "Aleyr"
__date__ = "2018/11/10"
VERSION = "0.9.2"
__version__ = "$Revision: " + VERSION

BUILD_EXE_NAME = "build_pack.exe"
PARSE_EXE_NAME = "parse_pack.exe"

BUILD_SCRIPT_NAME = "build_pack.py"
PARSE_SCRIPT_NAME = "parse_pack.py"

APP_LOGO_ICO = "./logoapp.ico"

APP_NAME = "EverDrive-Packs-Lists-Database-UI"
INI_FILE_NAME = APP_NAME + ".cfg"
INI_DIR_MAC = "~/Library/Application Support/" + APP_NAME + "/"
INI_FILE_MAC = INI_DIR_MAC + APP_NAME + ".cfg"
if "LOCALAPPDATA" in os.environ:
    INI_DIR_WINDOWS = os.environ["LOCALAPPDATA"] + "\\" + APP_NAME + "\\"
    INI_FILE_WINDOWS = INI_DIR_WINDOWS + APP_NAME + ".cfg"
INI_DIR_UNIX = "~/"
INI_FILE_UNIX = INI_DIR_UNIX + APP_NAME + "/" + APP_NAME + ".cfg"

def select_folder(directory, title):
    path = fd.askdirectory(initialdir=os.getcwd(), title=title)
    if path:
        directory.set(path)


def select_file_open(filename, title):
    path = fd.askopenfilename(initialdir=os.getcwd(), title=title)
    if path:
        filename.set(path)


def select_file_save(filename, title):
    path = fd.asksaveasfilename(initialdir=os.getcwd(), title=title)
    if path:
        filename.set(path)


def create_command(build_file=None, parse_file=None,
                   folder=None, output=None, input_folder=None,
                   database=None, output_folder=None, missing=None,
                   file_strategy=None, skip_eisting=None):
    arr = create_command_array(build_file=build_file,
                               parse_file=parse_file,
                               folder=folder,
                               output=output,
                               input_folder=input_folder,
                               database=database,
                               output_folder=output_folder,
                               missing=missing,
                               file_strategy=file_strategy,
                               skip_eisting=skip_eisting,
                               new_line=False,
                               add_quotes=True)
    cmd = " ".join(arr)

    return cmd


def get_ini_file():
    tmp = INI_FILE_UNIX
    if "Darwin" in system():
        tmp = INI_FILE_MAC
    elif "Windows" in system():
        tmp = INI_FILE_WINDOWS

    # print("tmp " + tmp)
    out = Path(tmp)
    # print("out " + str(out))
    return out


def save_ini_file(ini_file, section, values, root=None):
    config = configparser.ConfigParser()
    config[section] = values
    # folder check
    ini_dir = INI_DIR_UNIX
    if "Darwin" in system():
        ini_dir = INI_DIR_MAC
    elif "Windows" in system():
        ini_dir = INI_DIR_WINDOWS
    ini_dir = Path(ini_dir)
    # print ("save_ini_file ini_dir " + str(ini_dir))
    # print ("save_ini_file ini_dir.exists() " + str(ini_dir.exists()))
    try:
        if not ini_dir.exists():
            # print("Will create ini directory")
            ini_dir.mkdir()
            # print("ini dir created!")
        with ini_file.open(mode="w") as configfile:
            config.write(configfile)
    except:
        # TODO create dialog with error
        print("Error when saving file")


def is_pack_scripts_folder(scripts_folder):
    out = False
    if scripts_folder:
        folder = Path(scripts_folder)

        out = _is_pack_scripts_folder(folder)

    return out


def _is_pack_scripts_folder(folder):
    out = False
    if folder.exists() and folder.is_dir():
        build_file = folder / BUILD_SCRIPT_NAME
        parse_file = folder / PARSE_SCRIPT_NAME

        build_exe = folder / BUILD_EXE_NAME
        parse_exe = folder / PARSE_EXE_NAME

        if build_file.exists() and parse_file.exists():
            out = True

        if build_exe.exists() and parse_exe.exists():
            out = True

    return out


def get_pack_scripts_paths(folder):
    build_file = folder / BUILD_SCRIPT_NAME
    parse_file = folder / PARSE_SCRIPT_NAME
    if "Windows" in system() and str(sys.executable).lower().find("python") == -1:
        build_file = Path(".") / BUILD_EXE_NAME
        parse_file = Path(".")   / PARSE_EXE_NAME

    return (build_file, parse_file)


def get_abs_path(path, add_quotes=False, quote="\""):
    out = os.path.abspath(str(path))
    if add_quotes:
        out = quote + out + quote

    return out


def create_command_array(build_file=None, parse_file=None,
                         folder=None, output=None, input_folder=None,
                         database=None, output_folder=None, missing=None,
                         file_strategy=None, skip_eisting=None, new_line=True,
                         add_quotes=False):
    python_path = Path(sys.executable)
    cmd = [get_abs_path(python_path, add_quotes)]
    if "Windows" in system() and cmd[0].lower().find("python") == -1:
        cmd = []
    if parse_file:
        cmd.append(get_abs_path(parse_file, add_quotes))
        cmd.append("-f")
        cmd.append(get_abs_path(Path(folder), add_quotes))
        cmd.append("-o")
        cmd.append(get_abs_path(Path(output), add_quotes))
    else:
        cmd.append(get_abs_path(build_file, add_quotes))
        cmd.append("-i")
        cmd.append(get_abs_path(Path(input_folder), add_quotes))
        cmd.append("-d")
        cmd.append(get_abs_path(Path(database), add_quotes))
        cmd.append("-o")
        cmd.append(get_abs_path(Path(output_folder), add_quotes))
        if missing and len(missing) > 0:
            cmd.append("-m")
            cmd.append(get_abs_path(Path(missing), add_quotes))
        if file_strategy == 0:
            cmd.append("--file_strategy")
            cmd.append("copy")
        else:
            cmd.append("--file_strategy")
            cmd.append("hardlink")
        if skip_eisting:
            cmd.append("--skip_existing")

    if new_line:
        cmd.append("--new_line")

    return cmd


def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return


def click_set_paths(parent, script_path):
    pass
