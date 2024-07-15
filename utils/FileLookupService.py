import os
from typing import List

from models.AppModel import AppModel


class FileLookupService:
    def __init__(self, app_model: AppModel) -> None:
        self.__app_model = app_model

    def find_app_related_files(self) -> List[str]:
        if not os.access("/private", os.R_OK):
            raise PermissionError("Python does not have read access to the /private folder.")

        search_paths = [
            '/'
        ]

        ignored_dirs = [
            '/System',
            os.path.expanduser('~/Library/WebKit')
        ]

        related_files = [self.__app_model.path]

        for path in search_paths:
            for root, dirs, files in os.walk(path):
                should_continue = self.__process_directory(root, related_files)
                if should_continue:
                    continue

                dirs[:] = self.__filter_dirs(root, dirs, ignored_dirs)
                for file in files:
                    filename = os.path.join(root, file)
                    if self.__app_model.identifier in filename or self.__app_model.relative_identifier in filename:
                        related_files.append(filename)

        return related_files

    @staticmethod
    def __filter_dirs(root: str, dirs: List[str], ignored_dirs: List[str]) -> List[str]:
        """
        Filter out directories from a given list of directories that do not start with any of the ignored directories.

        :param root: base path /root for os
        :param dirs: List of directories
        :param ignored_dirs: List of ignored directories
        :return: Filtered list of directories
        """
        filtered_dirs = list()

        for d in dirs:
            ignore_dir = False
            for dir_to_ignore in ignored_dirs:
                dirname = os.path.abspath(os.path.join(root, d))
                if dirname.startswith(dir_to_ignore):
                    ignore_dir = True
                    break

            if not ignore_dir:
                filtered_dirs.append(d)

        return filtered_dirs

    def __process_directory(self, root: str, related_files: List[str]) -> bool:
        if any(root.startswith(rel_file) for rel_file in related_files):
            return True
        elif self.__app_model.identifier in root or self.__app_model.relative_identifier in root:
            related_files.append(root)
            return True

        return False
