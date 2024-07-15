import os

from repositories.AppRegistry import AppRegistry


class AppService:
    def __init__(self, lookup_folder):
        self.__lookup_folder = lookup_folder

    def create_app_path(self, app_name):
        return os.path.join(self.__lookup_folder, app_name)

    def list_apps(self) -> AppRegistry:
        app_list = AppRegistry()
        for root, dirs, files in os.walk(self.__lookup_folder):
            if self.__is_excluded(root):
                continue

            if self.__is_mac_app(root):
                app_list.append(root)
                continue

            for file in files:
                if file.endswith('.app'):
                    app_list.append(os.path.join(root, file))

        return app_list

    @staticmethod
    def __is_excluded(directory_path: str) -> bool:
        dirs = [
            '.app/',
            '/Python',
            'StarCraft II'
        ]

        return any(d in directory_path for d in dirs)

    @staticmethod
    def __is_mac_app(directory_path: str):
        return directory_path.endswith('.app')
