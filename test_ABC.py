from abc import ABC, abstractmethod
from tkinter import *


class AbstractClassExample(ABC, Toplevel):

    def __init__(self, value):
        self.value = value
        super().__init__()

    @abstractmethod
    def do_something(self):
        pass

    def not_abs(self):
        pass


class DoAdd42(AbstractClassExample):
    def do_something(self):
        return self.value + 42


class DoMul42(AbstractClassExample):
    def do_something(self):
        return self.value * 42


x = DoAdd42(10)
y = DoMul42(10)
print(x.do_something())
print(y.do_something())