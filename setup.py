import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'excludes': ['gtk', 'PyQt4', 'Tkinter', 'wx']
    }
}

executables = [
    Executable('main.py', base=base)
]

setup(
    name='OkayMoney',
    options=options,
    executables=executables,
)
