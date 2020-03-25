"""
HSTSParser: Parse browser HSTS databases into forensic artifacts.

Usage:
  hstsparser table [--firefox|--chrome] [--sort=<column>] [<path>]
  hstsparser -h | --help
  hstsparser --version

Options:
  -h --help            Show this screen.
  --version            Show version.
  path                 Folder to search, or path to HSTS file.
  --sort=<column>      Sort a specified column [default: Last Accessed].
"""

__version__ = '1.2.0'

import importlib
import platform

from docopt import docopt

from hstsparser.utils import HSTSReader


system = platform.system()

if system == 'Windows':
    win32api = importlib.import_module('win32api')
    *drives, _ = win32api.GetLogicalDriveStrings().split('\000')
    print(drives)


def main() -> None:
    """Entry point for the command-line alias."""
    arguments = docopt(__doc__, version=f'hstsparser {__version__}')
    browser = 'firefox'
    if browser == 'chrome':
        pass
    else:
        pass
    print(arguments.get('--sort'))
