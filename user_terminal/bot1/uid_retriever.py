import inspect
import os
import random


def idnum(username):
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = os.path.splitext(os.path.basename(module.__file__))[0]
    return int("".join(str(ord(c)) for c in username+filename)+str(random.randint(0,10000)))