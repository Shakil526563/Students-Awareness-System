"""
Script to set up frontend directories and ensure they exist
"""

import os
import shutil
from pathlib import Path

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent

def ensure_directories():
    """Ensure required directories exist"""
    directories = [
        os.path.join(BASE_DIR, 'templates'),
        os.path.join(BASE_DIR, 'templates', 'awareness'),
        os.path.join(BASE_DIR, 'static'),
        os.path.join(BASE_DIR, 'static', 'css'),
        os.path.join(BASE_DIR, 'static', 'img'),
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directory exists: {directory}")

if __name__ == "__main__":
    ensure_directories()
    print("Frontend directory setup complete!")
