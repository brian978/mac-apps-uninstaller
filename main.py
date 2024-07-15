from models.AppModel import AppModel
from services.AppService import AppService
from services.FileLookupService import FileLookupService


def main():
    app_service = AppService('/Applications')
    apps = app_service.list_apps()

    print("List of installed applications:")
    for i, app in enumerate(apps.list(), start=1):
        print(f"{i}) {app.name}")

    choice = int(input("Choose app to uninstall: ")) - 1
    if 0 <= choice < apps.length():
        selected_app = apps.choice(choice)
        lookup_service = FileLookupService(selected_app)

        selected_app.related_files = lookup_service.find_app_related_files()

        print(f"App name: {selected_app.name}")
        print(f"Bundle identifier: {selected_app.identifier}")
        print(f"Relative identifier: {selected_app.relative_identifier}")
        print("Related files found:")
        for file in selected_app.related_files:
            print(f"rm -rfv \"{file}\"")

        print("\nThe related files were NOT removed! You need to run the commands manually\n")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
