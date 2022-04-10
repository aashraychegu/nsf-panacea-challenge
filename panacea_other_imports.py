import shelve
from platform import platform, system
import sys
from webbrowser import open_new as open_new_web_page
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import os
from plyer import notification


PREFS = "https://raw.githubusercontent.com/aashraychegu/nsf-panacea-challenge/main/grabthings"


class backend():
    def __init__(self, NOTS=True, SOURCE=PREFS, SAVEONEXIT=True) -> None:
        self.nots = NOTS
        self.source = SOURCE


def contains(l, i):
    #print(l, i)
    l.sort()
    for j in l:
        if i in j.lower():
            return True
    return False


BACKEND = backend()


db = shelve.open("resources/databases/panacea_internal_user_preferences_file")


def loadpref(uid):
    return db.get(uid)


def setpref(uid, value):
    db[uid] = value


def newpref(uid, value=[False, False]):
    db[uid] = value
    return loadpref(uid)


def delpref(uid):
    del db[uid]
    newpref(uid)
