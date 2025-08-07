import os
import subprocess

from models.AppModel import AppModel


class AppRegistry:
    def __init__(self):
        self.__apps = []

    def length(self):
        return len(self.__apps)

    def list(self):
        return self.__apps

    def choice(self, idx):
        return self.__apps[idx]

    def append(self, app_path):
        identifier = self.__find_bundle_identifier(app_path)
        if identifier is None:
            return None

        name = os.path.basename(app_path)
        # Remove .app extension from displayed name
        if name.endswith('.app'):
            name = name[:-4]
        self.__apps.append(AppModel(name, identifier, app_path))

        return self

    @staticmethod
    def __find_bundle_identifier(app_path):
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
