"""
This is a minimal setup.py script for packaging the Mac Apps Uninstaller
as a standalone macOS application using py2app.
"""

import os
from setuptools import setup

# Use proper ad-hoc code signing instead of disabling it completely
# This ensures the app has valid signatures that macOS accepts

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'app_icon.icns',
    'plist': {
        'CFBundleName': 'MacAppUninstaller',
        'CFBundleDisplayName': 'MacAppUninstaller',
        'CFBundleIdentifier': 'com.macappsuninstaller',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': '© 2025',
        'NSHighResolutionCapable': True,
    },
    'packages': ['PySide6'],
    'includes': ['models', 'services', 'repositories'],
}

setup(
    name='MacAppsUninstaller',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
)