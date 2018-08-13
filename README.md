# EverDrive-Packs-Lists-Database-UI

The EverDrive Packs List Database UI is Graphical User Interface for the
EverDrive Packs Lists Project for easier usage.

The UI uses file dialogs to help on selecting folders and files, performs
some basic validation, then you have the option of obtaining the command to
copy and pasted on a console to run it from there, or execute the command from
within the UI itself.

The interface consistf 2 tabs, one for build_pack.py (default tab) and the other for 
parse_pack.py.

**Build tab**

The first 3 input fields are required, the 4th is optional also the advanced options
are present and preselected to default values, be careful with this ones.

**Parse tab**

The 2 input fields are required.

## GUI

**gui_pack.py** Graphical User Interface for parse_pack.py and build_pack.py:
```DOS .bat
"C:\XXX\gui_pack.py"
```

`-s` (or `--scripts`) indicates the folder were the `build_pack.py` and 
`parse_pack.py` scripts are located.

Depending on your python installation, you may need to begin your
command with the location of `python.exe` (for example,
`C:\Users\XXX\AppData\Local\Programs\Python\Python36-32\python.exe`).

## Wiki

[wiki](https://github.com/Aleyr/EverDrive-Packs-Lists-Database-UI/wiki).

## Requirements

[EverDrive-Packs-Lists-Database scripts](https://github.com/SmokeMonsterPacks/EverDrive-Packs-Lists-Database)

[python](https://www.python.org) 3.5 or newer

Linux, MacOS, or Windows

Python 3 is a requirement the installer for Mac and Windows include tkinter by
default, however on \*nix systems python3-tk is also a requirement.

(Linux and MacOS users might need to convert the script and SMDB files
first with the command `dos2unix`)

## Coding

[@Aleyr](https://github.com/Aleyr).

## Similar tools

- [clrmamepro](https://mamedev.emulab.it/clrmamepro/),
- [romcenter](http://www.romcenter.com/),
- [romvault](http://www.romvault.com/)
