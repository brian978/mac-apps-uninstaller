import os
import subprocess
from typing import List

from models.AppModel import AppModel


def find_app_related_files(app_model: AppModel) -> List[str]:
    """
    :type app_model: AppModel
    """
    search_paths = [
        os.path.expanduser('~/Library/Application Support/'),
        os.path.expanduser('~/Library/Caches/'),
        os.path.expanduser('~/Library/Preferences/'),
        os.path.expanduser('~/Library/Logs/'),
        '/Library/Application Support/',
        '/Library/Caches/',
        '/Library/Preferences/',
        '/Library/Logs/',
        '/'
    ]

    related_files = []

    for path in search_paths:
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d != 'System']
            for file in files:
                if app_model.identifier in file or app_model.relative_identifier in file:
                    related_files.append(os.path.join(root, file))

    return related_files


def list_apps(applications_folder):
    apps = [f for f in os.listdir(applications_folder) if f.endswith('.app')]
    return apps


def get_bundle_identifier(app_path):
    try:
        # Use the 'defaults' command to read the Info.plist of the app
        result = subprocess.run(
            ['defaults', 'read', f'{app_path}/Contents/Info', 'CFBundleIdentifier'],
            capture_output=True,
            text=True
        )

        return result.stdout.strip()
    except Exception as e:
        print(f"Error reading bundle identifier: {e}")
        return None
