import os
import subprocess


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
