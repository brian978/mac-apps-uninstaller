import os

from models.AppModel import AppModel
from utils.detection_tools import list_apps, get_bundle_identifier, find_app_related_files


def main():
    applications_folder = '/Applications'
    apps = list_apps(applications_folder)

    print("List of installed applications:")
    for i, app in enumerate(apps, start=1):
        print(f"{i}) {app}")

    choice = int(input("Choose app to uninstall: ")) - 1
    if 0 <= choice < len(apps):
        app_path = os.path.join(applications_folder, apps[choice])
        bundle_identifier = get_bundle_identifier(app_path)

        if bundle_identifier:
            app_model = AppModel(apps[choice].strip(".app"), bundle_identifier)
            app_model.related_files = find_app_related_files(app_model)

            print(f"App name: {app_model.name}")
            print(f"Bundle identifier: {app_model.identifier}")
            print(f"Relative identifier: {app_model.relative_identifier}")
            print("Related files found:")
            for file in app_model.related_files:
                print(f"rm -rfv \"{file}\"")
        else:
            print("Failed to retrieve bundle identifier.")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
