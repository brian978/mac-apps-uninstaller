import sys
import os
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QListWidget, QListWidgetItem, 
                              QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, 
                              QMessageBox, QTextEdit, QSplitter, QDialog, QCheckBox,
                              QMenuBar, QMenu, QProgressBar)
from PySide6.QtCore import Qt, QSize, QThread, QObject, Signal, QRunnable, QThreadPool
from PySide6.QtGui import QIcon, QFont, QAction  # QAction moved to QtGui in PySide6

from models.AppModel import AppModel
from services.AppService import AppService
from services.FileLookupService import FileLookupService

# Try to import app_icon, but handle gracefully if it fails
try:
    from app_icon import create_app_icon
    HAS_APP_ICON = True
except ImportError:
    HAS_APP_ICON = False
    print("Warning: app_icon module not available, using default icon")


class AppLoaderSignals(QObject):
    """Signals for the AppLoader worker thread"""
    finished = Signal(object)  # Signal emitted when loading is complete, passes the loaded apps
    error = Signal(str)        # Signal emitted when an error occurs


class AppLoader(QThread):
    """Worker thread for loading applications"""
    def __init__(self, lookup_folder):
        super().__init__()
        self.lookup_folder = lookup_folder
        self.signals = AppLoaderSignals()
        
    def run(self):
        try:
            app_service = AppService(self.lookup_folder)
            apps = app_service.list_apps()
            self.signals.finished.emit(apps)
        except Exception as e:
            self.signals.error.emit(str(e))


class FileLookupSignals(QObject):
    """Signals for the FileLookup worker thread"""
    finished = Signal(list)    # Signal emitted when lookup is complete, passes the found files
    error = Signal(str)        # Signal emitted when an error occurs


class FileLookup(QThread):
    """Worker thread for finding related files"""
    def __init__(self, app_model):
        super().__init__()
        self.app_model = app_model
        self.signals = FileLookupSignals()
        
    def run(self):
        try:
            lookup_service = FileLookupService(self.app_model)
            related_files = lookup_service.find_app_related_files()
            self.signals.finished.emit(related_files)
        except Exception as e:
            self.signals.error.emit(str(e))



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Mac Apps Uninstaller")
        self.setMinimumSize(800, 600)
        self.resize(1000, 600)  # Default window size: 1000px width
        
        # Create menu bar
        self.create_menu_bar()
        
        # Set macOS style sheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f7;
            }
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #d2d2d7;
                border-radius: 8px;
                padding: 5px;
                font-size: 13px;
            }
            QListWidget::item {
                border-bottom: 1px solid #d2d2d7;
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #0071e3;
                color: white;
            }
            QLabel {
                font-size: 13px;
                color: #1d1d1f;
            }
            QLabel#titleLabel {
                font-size: 18px;
                font-weight: bold;
                color: #1d1d1f;
            }
            QPushButton {
                background-color: #0071e3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0077ed;
            }
            QPushButton:pressed {
                background-color: #0068d1;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #d2d2d7;
                border-radius: 8px;
                padding: 5px;
                font-size: 13px;
            }
        """)
        
        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - App list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        title_label = QLabel("Installed Applications")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        self.app_list = QListWidget()
        self.app_list.setMinimumWidth(250)
        self.app_list.currentItemChanged.connect(self.on_app_selected)
        left_layout.addWidget(self.app_list)
        
        # Loading progress bar for app list
        self.app_loading_progress = QProgressBar()
        self.app_loading_progress.setTextVisible(True)
        self.app_loading_progress.setFormat("Loading applications...")
        self.app_loading_progress.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.app_loading_progress)
        
        # Right panel - App details
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        self.details_title = QLabel("Select an application")
        self.details_title.setObjectName("titleLabel")
        right_layout.addWidget(self.details_title)
        
        self.app_details = QTextEdit()
        self.app_details.setReadOnly(True)
        right_layout.addWidget(self.app_details)
        
        # Loading progress bar for file lookup
        self.file_loading_progress = QProgressBar()
        self.file_loading_progress.setTextVisible(True)
        self.file_loading_progress.setFormat("Finding related files...")
        self.file_loading_progress.setAlignment(Qt.AlignCenter)
        self.file_loading_progress.hide()  # Initially hidden
        right_layout.addWidget(self.file_loading_progress)
        
        # Button to find related files
        self.find_files_button = QPushButton("Find Related Files")
        self.find_files_button.setEnabled(False)
        self.find_files_button.hide()  # Hide until an app is selected
        self.find_files_button.clicked.connect(self.find_related_files)
        right_layout.addWidget(self.find_files_button)
        
        self.uninstall_button = QPushButton("Uninstall")
        self.uninstall_button.setEnabled(False)
        self.uninstall_button.hide()  # Hide until related files are found
        self.uninstall_button.clicked.connect(self.uninstall_app)
        right_layout.addWidget(self.uninstall_button)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        
        main_layout.addWidget(splitter)
        self.setCentralWidget(central_widget)
        
        # Initialize data
        self.selected_app = None
        self.apps = None
        
        # Start loading apps in background
        self.load_apps()
    
    def create_menu_bar(self):
        # Create menu bar
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        # Refresh action
        refresh_action = QAction("&Refresh", self)
        refresh_action.setShortcut("Ctrl+R")
        refresh_action.triggered.connect(self.refresh_app_list)
        file_menu.addAction(refresh_action)
        
        # Quit action
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("&Edit")
        
        # About action in app menu (macOS specific)
        if sys.platform == "darwin":
            about_action = QAction("&About Mac Apps Uninstaller", self)
            about_action.triggered.connect(self.show_about)
            # On macOS, the About action is automatically moved to the application menu
            edit_menu.addAction(about_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        
        # Help action
        help_action = QAction("&Help", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        # If not on macOS, add About to Help menu
        if sys.platform != "darwin":
            about_action = QAction("&About", self)
            about_action.triggered.connect(self.show_about)
            help_menu.addAction(about_action)
    
    def load_apps(self):
        """Start loading applications in background thread"""
        # Show loading progress
        self.app_loading_progress.setRange(0, 0)  # Indeterminate progress
        self.app_loading_progress.show()
        
        # Disable app list during loading
        self.app_list.setEnabled(False)
        
        # Create and start the worker thread
        self.app_loader = AppLoader('/Applications')
        self.app_loader.signals.finished.connect(self.on_apps_loaded)
        self.app_loader.signals.error.connect(self.on_app_load_error)
        self.app_loader.start()
    
    def on_apps_loaded(self, apps):
        """Handler for when apps are loaded successfully"""
        self.apps = apps
        self.populate_app_list()
        
        # Hide progress and enable app list
        self.app_loading_progress.hide()
        self.app_list.setEnabled(True)
    
    def on_app_load_error(self, error_msg):
        """Handler for when app loading fails"""
        QMessageBox.critical(
            self,
            "Error Loading Applications",
            f"An error occurred while loading applications:\n{error_msg}"
        )
        self.app_loading_progress.hide()
        self.app_list.setEnabled(True)
    
    def refresh_app_list(self):
        self.app_list.clear()
        self.details_title.setText("Select an application")
        self.app_details.setText("")
        self.uninstall_button.setEnabled(False)
        self.uninstall_button.hide()  # Hide when refreshing app list
        self.find_files_button.setEnabled(False)
        self.find_files_button.hide()  # Hide when refreshing app list
        
        # Start loading apps again
        self.load_apps()
    
    def show_about(self):
        QMessageBox.about(
            self,
            "About Mac Apps Uninstaller",
            "Mac Apps Uninstaller\n\n"
            "A utility to make uninstalling apps on Mac easier without requiring paid software.\n\n"
            "Version 1.0"
        )
    
    def show_help(self):
        QMessageBox.information(
            self,
            "Help",
            "How to use Mac Apps Uninstaller:\n\n"
            "1. Select an application from the list on the left\n"
            "2. Review the application details and related files\n"
            "3. Click the Uninstall button to remove the application\n\n"
            "Note: Some operations may require administrator privileges."
        )
    
    def populate_app_list(self):
        # Sort apps alphabetically by name
        sorted_apps = sorted(self.apps.list(), key=lambda app: app.name.lower())
        for app in sorted_apps:
            item = QListWidgetItem(app.name)
            item.setData(Qt.UserRole, app)
            self.app_list.addItem(item)
    
    def on_app_selected(self, current, previous):
        if current is None:
            self.uninstall_button.setEnabled(False)
            self.uninstall_button.hide()  # Hide when no app selected
            self.find_files_button.setEnabled(False)
            self.find_files_button.hide()  # Hide when no app selected
            self.details_title.setText("Select an application")
            self.app_details.setText("")
            self.selected_app = None
            return
        
        self.selected_app = current.data(Qt.UserRole)
        self.details_title.setText(self.selected_app.name)
        
        # Display basic app details immediately
        details = f"App name: {self.selected_app.name}\n"
        details += f"Bundle identifier: {self.selected_app.identifier}\n"
        details += f"Relative identifier: {self.selected_app.relative_identifier}\n\n"
        details += "Click 'Find Related Files' to search for files related to this application."
        self.app_details.setText(details)
        
        # Show and enable the find files button
        self.find_files_button.setEnabled(True)
        self.find_files_button.show()
        
        # Hide uninstall button until files are found
        self.uninstall_button.setEnabled(False)
        self.uninstall_button.hide()
        
    def find_related_files(self):
        """Start the search for files related to the selected application"""
        if self.selected_app is None:
            return
            
        # Update the app details text
        details = f"App name: {self.selected_app.name}\n"
        details += f"Bundle identifier: {self.selected_app.identifier}\n"
        details += f"Relative identifier: {self.selected_app.relative_identifier}\n\n"
        details += "Searching for related files...\n"
        self.app_details.setText(details)
        
        # Disable the find files button while searching
        self.find_files_button.setEnabled(False)
        
        # Show file loading progress
        self.file_loading_progress.setRange(0, 0)  # Indeterminate progress
        self.file_loading_progress.show()
        
        # Start file lookup in background
        self.file_lookup = FileLookup(self.selected_app)
        self.file_lookup.signals.finished.connect(self.on_files_found)
        self.file_lookup.signals.error.connect(self.on_file_lookup_error)
        self.file_lookup.start()
    
    def on_files_found(self, related_files):
        """Handler for when related files are found successfully"""
        if self.selected_app is None:
            return
            
        # Store the related files
        self.selected_app.related_files = related_files
        
        # Update app details with found files
        details = f"App name: {self.selected_app.name}\n"
        details += f"Bundle identifier: {self.selected_app.identifier}\n"
        details += f"Relative identifier: {self.selected_app.relative_identifier}\n\n"
        details += "Related files found:\n"
        for file in self.selected_app.related_files:
            details += f"• {file}\n"
        
        self.app_details.setText(details)
        self.uninstall_button.setEnabled(True)
        self.uninstall_button.show()  # Show button when files are found
        
        # Hide progress bar
        self.file_loading_progress.hide()
        
        # Hide the find files button since files are already found
        self.find_files_button.hide()
    
    def on_file_lookup_error(self, error_msg):
        """Handler for when file lookup fails"""
        # Hide progress bar
        self.file_loading_progress.hide()
        
        if "Python does not have read access to the /private folder" in error_msg:
            self.app_details.setText("Error: Python does not have read access to the /private folder.\n"
                                    "Please run this application with sudo or as an administrator.")
        else:
            self.app_details.setText(f"Error finding related files:\n{error_msg}")
            
        self.uninstall_button.setEnabled(False)
        self.uninstall_button.hide()  # Hide when file lookup fails
        
        # Re-enable the find files button to allow retrying
        self.find_files_button.setEnabled(True)
    
    def uninstall_app(self):
        if self.selected_app is None:
            return
        
        # Show single confirmation dialog
        confirm = QMessageBox.question(
            self,
            "Confirm Uninstall",
            f"Are you sure you want to uninstall {self.selected_app.name}?\n\n"
            "This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            # Execute the actual file removal
            self.execute_uninstall(self.selected_app.related_files)
    
    def execute_uninstall(self, file_paths):
        """Execute the uninstall by removing files with rm -rf command"""
        # Update details panel to show uninstall progress
        self.app_details.setText(f"Uninstalling {self.selected_app.name}...\n\nExecuting rm -rf commands:")
        
        successfully_removed = []
        failed_removals = []
        output_lines = [f"Uninstalling {self.selected_app.name}:", ""]
        
        for file_path in file_paths:
            try:
                output_lines.append(f"Removing: {file_path}")
                
                # Use subprocess to execute rm -rf with quoted file paths
                result = subprocess.run(['rm', '-rf', file_path], 
                                       capture_output=True, 
                                       text=True, 
                                       check=False)
                
                if result.returncode == 0:
                    successfully_removed.append(file_path)
                    output_lines.append("✓ Successfully removed")
                else:
                    failed_removals.append(file_path)
                    output_lines.append("✗ Failed to remove (requires sudo)")
                    if result.stderr:
                        output_lines.append(f"Error: {result.stderr.strip()}")
                
                # Update display in real-time
                self.app_details.setText("\n".join(output_lines))
                # Force GUI update
                QApplication.processEvents()
                    
            except Exception as e:
                failed_removals.append(file_path)
                output_lines.append(f"✗ Failed to remove: {str(e)}")
                self.app_details.setText("\n".join(output_lines))
                QApplication.processEvents()
        
        # Final summary
        output_lines.append("")
        output_lines.append("=" * 50)
        output_lines.append("UNINSTALL SUMMARY")
        output_lines.append("=" * 50)
        
        if successfully_removed:
            output_lines.append(f"✓ Successfully removed {len(successfully_removed)} files")
            
        if failed_removals:
            output_lines.append(f"✗ {len(failed_removals)} files require manual removal")
            output_lines.append("")
            output_lines.append("Copy and paste these commands into Terminal:")
            output_lines.append("")
            
            # Add commands without bullet points for easy copy-paste
            for file_path in failed_removals:
                output_lines.append(f'sudo rm -rf "{file_path}"')
        else:
            output_lines.append("All files successfully removed!")
            # Refresh the app list to reflect changes
            self.refresh_app_list()
        
        # Show final output
        self.app_details.setText("\n".join(output_lines))


def main():
    try:
        # Enable macOS-specific features
        if sys.platform == "darwin":
            # Set the app ID
            QApplication.setApplicationName("Mac Apps Uninstaller")
            QApplication.setOrganizationName("Mac Apps Uninstaller")
            QApplication.setOrganizationDomain("com.macappsuninstaller")
            
            # High DPI scaling is enabled by default in PySide6
        
        app = QApplication(sys.argv)
        
        # Create and set the app icon if available
        if HAS_APP_ICON:
            try:
                app_icon = create_app_icon()
                app.setWindowIcon(app_icon)
            except Exception as e:
                print(f"Warning: Could not create app icon: {e}")
                app_icon = None
        else:
            app_icon = None
        
        # Set macOS dark mode support
        if hasattr(app, 'setStyle'):
            try:
                app.setStyle("macos")
            except Exception as e:
                print(f"Warning: Could not set macOS style: {e}")
        
        window = MainWindow()
        if app_icon is not None:
            window.setWindowIcon(app_icon)  # Also set the icon for the main window
        window.show()
        
        # In PySide6, exec_() was renamed to exec()
        if hasattr(app, 'exec'):
            sys.exit(app.exec())
        else:
            sys.exit(app.exec_())
            
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
