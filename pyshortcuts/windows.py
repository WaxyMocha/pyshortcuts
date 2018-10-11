#!/usr/bin/env python
"""
Create desktop shortcuts for Windows
"""
from __future__ import print_function
import os
import sys

from .utils import get_homedir, get_paths

def make_shortcut(script, name, description=None, terminal=False,
                  icon_path=None, icon=None):
    """create windows shortcut"""
    from win32com.client import Dispatch

    if description is None:
        description = name

    homedir = get_homedir()
    desktop, target, icon_path = get_paths(script, icon_path)

    pyexe = os.path.join(sys.prefix, 'pythonw.exe')
    if terminal:
        pyexe = os.path.join(sys.prefix, 'python.exe')

    # add several checks for valid ways to run each script, including
    # accounting for Anaconda's automagic renaming and creation of exes.
    target_exe = '%s.exe' % target
    target_bat = '%s.bat' % target
    target_spy = '%s-script.py' % target

    if os.path.exists(target_exe):
        target = target_exe
    elif os.path.exists(target_spy):
        target = "%s %s" % (pyexe, target_spy)
    elif os.path.exists(target):
        fbat = open(target_bat, 'w')
        fbat.write("""@echo off

%s %%~dp0%%~n0 %%1 %%2 %%3 %%4 %%5

        """ % (pyexe))
        fbat.close()
        target = target_bat

    shortcut = Dispatch('WScript.Shell').CreateShortCut(
        os.path.join(desktop, name) +  '.lnk')
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = homedir
    shortcut.WindowStyle = 0
    shortcut.Description = description
    if icon is not None:
        shortcut.IconLocation = os.path.join(icon_path, icon + '.ico')
    shortcut.save()