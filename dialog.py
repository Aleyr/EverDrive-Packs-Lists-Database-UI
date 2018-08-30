from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import *
from platform import system
from utils import *


class Dialog(ABC, Toplevel):
    def __init__(self, parent, title=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent
        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    @abstractmethod
    def body(self, master):
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        self.ok_btn = Button(box, text="OK", width=10, underline=0,
                             command=self.ok, default=ACTIVE)
        self.ok_btn.pack(side=LEFT, padx=5, pady=5)
        self.cancel_btn = Button(box, text="Cancel", width=10, underline=0,
                                 command=self.cancel)
        self.cancel_btn.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Alt_L><o>", self.ok)
        self.bind("<Alt_L><c>", self.cancel)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def close(self):
        self.parent.focus_set()
        self.destroy()

    #
    # standard button semantics

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.close()

    def cancel(self, event=None):
        self.cancel_action()
        self.close()

    #
    # command hooks

    @abstractmethod
    def cancel_action(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def apply(self):
        pass


class ScriptSelectionDialog(Dialog):
    def __init__(self, parent, title=None):
        super().__init__(parent, title)

    #
    # construction hooks

    def body(self, master):
        self.scripts_folder = StringVar()
        if self.parent.folder:
            self.scripts_folder.set(get_abs_path(self.parent.folder))
        else:
            self.scripts_folder.set("")

        textbox_path = Entry(master, width=50,
                             textvariable=self.scripts_folder)
        textbox_path.grid(column=2, row=1, sticky=E)
        ttk.Label(master, text="ROMs folder: "
                  ).grid(column=1, row=1, sticky=W)
        browse_btn = ttk.Button(master, text="Browse", underline=0,
                                command=lambda:
                                select_folder(self.scripts_folder,
                                              "Select Pack Scripts folder"))
        browse_btn.grid(column=3, row=1, sticky=W)

        self.bind("<Alt_L><b>",
                  lambda e: select_folder(self.scripts_folder,
                                          "Select Pack Scripts folder"))
        textbox_path.focus_set()

    #
    # standard button semantics

    def cancel_action(self):
        if len(self.scripts_folder.get()) > 0:
            # Enable build and parse buttons
            self.parent.toggle_action_buttons(True)
        else:
            # Disable build and parse buttons
            self.parent.toggle_action_buttons(False)

    #
    # command hooks

    def validate(self):
        out = False
        if (not self.scripts_folder.get() == ""):
            path = Path(self.scripts_folder.get())
            if path.exists() and path.is_dir():
                out = True
        else:
            # Mark the textbox has an error
            pass

        return out

    def apply(self):
        folder = Path(self.scripts_folder.get())
        build_file, parse_file = get_pack_scripts_paths(folder)
        self.parent.folder = folder
        self.parent.build_file = build_file
        self.parent.parse_file = parse_file

        save_ini_file(get_ini_file(), "UI",
                      {"scripts_folder": get_abs_path(folder)})


class SuccessDialog(Dialog):
    def __init__(self, parent, title=None, message="", size=10):
        self._message = message
        self._size = size
        super().__init__(parent, title)

    #
    # construction hooks

    def body(self, master):
        msg = tk.Text(master, height=1, width=40,
                      font=('courier', self._size, 'normal'))
        msg.grid(stick=tk.N, padx=(10, 10), pady=(10, 10))
        msg.insert("1.0", (self._message))

    def buttonbox(self):
        box = Frame(self)

        self.ok_btn = Button(box, text="OK", width=10, underline=0,
                             command=self.ok, default=ACTIVE)
        self.ok_btn.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Alt_L><o>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()
        self.ok_btn.focus_set()

    #
    # standard button semantics

    def cancel_action(self):
        pass

    #
    # command hooks

    def validate(self):
        return True

    def apply(self):
        pass


class CommandDialog(Dialog):
    def __init__(self, parent, title=None, message="", size=10):
        self._message = message
        self._size = size
        super().__init__(parent, title)

    #
    # construction hooks

    def body(self, master):
        msg = tk.Text(master, height=5, width=60,
                      font=('courier', self._size, 'normal'))
        msg.grid(stick=tk.N, padx=(10, 10), pady=(10, 10))
        msg.insert("1.0", (self._message))

    def buttonbox(self):
        box = Frame(self)

        self.ok_btn = Button(box, text="OK", width=10, underline=0,
                             command=self.ok, default=ACTIVE)
        self.ok_btn.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Alt_L><o>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()
        self.ok_btn.focus_set()

    #
    # standard button semantics

    def cancel_action(self):
        pass

    #
    # command hooks

    def validate(self):
        return True

    def apply(self):
        pass


class AboutDialog(Dialog):
    def __init__(self, parent, size=10):
        self._size = size
        # Fonts
        if "Darwin" in system():
            #    print("\nOS X detected")
            self.fontsize = 12
            self.pad_radio = 3
            self.but_size = -2
            self.res_size = -1
        else:
            #    print("\nWindows detected")
            self.fontsize = 10
            self.pad_radio = 0
            self.but_size = -2
            self.res_size = -2

        self.fontz = {
            "bold": ("TkDefaultFont", self.fontsize, "bold"),
            "normal_small": ("TkDefaultFont",
                             self.fontsize + self.but_size, "normal"),
            "italic_small": ("TkDefaultFont",
                             self.fontsize + self.but_size, "italic")}
        super().__init__(parent, "About")

    #
    # construction hooks

    def body(self, master):
        tk.Label(master,
                 text="""Smoke Monster Packs UI""",
                 justify=CENTER,
                 font=self.fontz["bold"]).grid(row=0, column=0, columnspan=2,
                                               pady=(5, 0), padx=(10, 10))
        tk.Label(master,
                 text="""by Aleyr""",
                 justify=CENTER,
                 font=self.fontz["bold"]).grid(row=1, column=0, columnspan=2,
                                               pady=(0, 0), padx=(10, 10))
        tk.Label(master,
                 text="""2018""",
                 justify=CENTER).grid(row=2, column=0, columnspan=2,
                                      pady=(5, 5), padx=(10, 10))
        tk.Label(master,
                 text="""Contact:""",
                 justify=CENTER).grid(row=3, column=0, columnspan=1,
                                      pady=(5, 5), padx=(10, 10))
        about_message = """aleyr@walla.com"""
        msg = tk.Text(master, height=1, width=18,
                      font=('courier', self._size, 'normal'))
        msg.grid(stick=tk.N, padx=(10, 10), pady=(10, 10))
        msg.insert("1.0", about_message)

    def buttonbox(self):
        box = Frame(self)

        self.ok_btn = Button(box, text="OK", width=10, underline=0,
                             command=self.ok, default=ACTIVE)
        self.ok_btn.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Alt_L><o>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()
        self.ok_btn.focus_set()

    #
    # standard button semantics

    def cancel_action(self):
        pass

    #
    # command hooks

    def validate(self):
        return True

    def apply(self):
        pass
