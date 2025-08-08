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

- Python 3.11 (recommended for building and packaging)
  - Note: Newer Python versions (e.g., 3.12/3.13) may not be fully compatible with py2app/PySide6/setuptools at the time of this release. Our CI uses Python 3.11 for reproducible, non-damaged .app bundles.
- PySide6 6.0.0 or higher

## Installation

### Option 1: Download the pre-built application (Recommended)

1. Download the latest release from the [Releases](https://github.com/yourusername/mac-apps-uninstaller/releases) page.
2. Extract the zip file.
3. Drag the MacAppUninstaller.app to your Applications folder.
4. When opening the app for the first time, you may see a security warning. This is normal for apps distributed outside the Mac App Store. Right-click on the app and select "Open" to bypass this warning.

### Option 2: Build from source

1. Clone the repository:
```
git clone https://github.com/yourusername/mac-apps-uninstaller.git
cd mac-apps-uninstaller
```

2. Install the required dependencies and build the application:
```
make install
make build
```

3. The built application will be available in the `dist` folder.

## Usage

### Using the .app application (Recommended)

1. Double-click the MacAppUninstaller.app in your Applications folder.
2. For full functionality (to access system files), right-click the app and select "Open" to bypass Gatekeeper.

### Running from source

If you prefer to run the application from source:

```
make
```

Or manually:

```
python main.py
```

For full functionality (to access system files), you may need to run with sudo:
```
sudo python main.py
```

## Building the Application

To build the standalone macOS application:

```
make build
```

This will create a standalone .app bundle in the `dist` directory that can be distributed and run without requiring Python or any dependencies to be installed.

For development and testing, you can use:

```
make dev-build
```

This creates a development build that's faster to compile but still requires the Python environment.

To see all available build options:

```
make help
```

## Why does CI use Python 3.11 (and not the latest)?

Short answer: Packaging stability. macOS app bundling with py2app and PySide6 has tight version coupling to Python and setuptools. At the moment, Python 3.13 has caused broken bundles (macOS reports the app as "damaged"). Python 3.11 is a well-supported baseline for these tools and consistently produces valid bundles.

Details:
- py2app and certain PySide6 wheels lag behind the newest Python releases.
- setuptools >=81 also introduced changes that affect py2app builds; we pin setuptools<81 in requirements.
- Using Python 3.11 in CI ensures deterministic, working artifacts for end users.

If you want to experiment locally with a newer Python:
- Try creating a venv with Python 3.12 and run `make build`.
- If the app launches fine and passes your tests, feel free to propose a CI bump via PR. We'll revisit the CI version as upstream tooling adds support.

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
