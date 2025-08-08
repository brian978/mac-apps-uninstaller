#!/usr/bin/env python3
"""
Script to create an .icns file from our programmatic app icon.
This will save the icon as a PNG and then convert it to .icns format.
"""

import os
import subprocess
import sys
from PySide6.QtGui import QPixmap, QGuiApplication
from app_icon import create_app_icon

def main():
    # Initialize QGuiApplication before creating any QPixmap objects
    app = QGuiApplication(sys.argv)
    
    # Create the app icon
    icon = create_app_icon()
    
    # Create a temporary directory for icon creation
    if not os.path.exists('iconbuild'):
        os.makedirs('iconbuild')
    
    # Save the icon at different sizes
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for size in sizes:
        pixmap = icon.pixmap(size, size)
        pixmap.save(f'iconbuild/icon_{size}x{size}.png')
        print(f"Saved icon at {size}x{size}")
    
    # Use iconutil to create the .icns file (macOS only)
    try:
        # Create iconset directory
        iconset_dir = 'iconbuild/app_icon.iconset'
        if not os.path.exists(iconset_dir):
            os.makedirs(iconset_dir)
        
        # Copy files to iconset with required naming
        for size in sizes:
            if size <= 512:
                # Standard resolution
                os.system(f'cp iconbuild/icon_{size}x{size}.png {iconset_dir}/icon_{size}x{size}.png')
                # High resolution (retina)
                if size * 2 in sizes:
                    os.system(f'cp iconbuild/icon_{size*2}x{size*2}.png {iconset_dir}/icon_{size}x{size}@2x.png')
        
        # Convert iconset to icns
        os.system(f'iconutil -c icns {iconset_dir} -o app_icon.icns')
        print("Created app_icon.icns")
        
        # Clean up
        os.system('rm -rf iconbuild')
        print("Cleaned up temporary files")
        
    except Exception as e:
        print(f"Error creating .icns file: {e}")
        print("You may need to manually create an .icns file for your application icon.")

if __name__ == "__main__":
    main()