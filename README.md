# Mac Apps Uninstaller

A native macOS application to make uninstalling apps on Mac easier without requiring paid software.

## Features

- Native macOS look and feel using PySide6
- Lists all installed applications from the /Applications directory
- Displays detailed information about selected applications
- Finds all related files for complete uninstallation
- Provides a confirmation dialog before uninstallation
- Supports macOS dark mode
- Background processing for improved responsiveness
- Progress indicators for long-running operations
- Non-blocking UI during application loading and file scanning

## Requirements

- Python 3.6 or higher
- PySide6 6.0.0 or higher

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/mac-apps-uninstaller.git
cd mac-apps-uninstaller
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

Run the application:
```
python main.py
```

For full functionality (to access system files), you may need to run with sudo:
```
sudo python main.py
```

## How It Works

1. The application scans your /Applications directory to find installed applications
   - This operation runs in a background thread to keep the UI responsive
   - A progress indicator shows that the application is working
2. When you select an application, basic information about the app is displayed
   - The app name, bundle identifier, and other details are shown immediately
3. Click the "Find Related Files" button to search for files related to the selected application
   - File scanning happens in a background thread
   - A progress indicator shows that files are being searched
4. Once related files are found, you can review them before proceeding
5. You can then click the "Uninstall" button to proceed with removal
6. For safety, the application shows the commands that would be executed but doesn't actually remove files

The application uses multithreading to ensure that long-running operations like scanning for applications and finding related files don't block the user interface. This makes the application feel responsive even when performing intensive file system operations.

## Screenshots

(Screenshots would be added here)

## License

See the LICENSE file for details.
