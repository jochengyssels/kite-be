"""
Python script to install required packages.
Use this if you prefer Python over bash for installation.
"""

import subprocess
import sys
import os

def install_packages():
    # Check if virtual environment is active
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print("Warning: You're not running in a virtual environment.")
        response = input("Do you want to create and activate a virtual environment? (y/n): ")
        
        if response.lower() == 'y':
            # Create virtual environment
            subprocess.run([sys.executable, "-m", "venv", "venv"])
            print("Virtual environment created.")
            
            # Provide activation instructions
            if os.name == 'nt':  # Windows
                print("\nTo activate the virtual environment, run:")
                print("venv\\Scripts\\activate")
            else:  # Unix/Linux/Mac
                print("\nTo activate the virtual environment, run:")
                print("source venv/bin/activate")
            
            print("\nAfter activating, run this script again.")
            return
    
    print("Installing packages from requirements.txt...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Check if neuralgcm is installed
    try:
        import neuralgcm
        print("neuralgcm is already installed.")
    except ImportError:
        print("\nWarning: neuralgcm could not be imported.")
        print("If it's a custom package, you may need to install it manually:")
        print("pip install -e /path/to/neuralgcm")
    
    print("\nInstallation complete!")
    print("Run verify_imports.py to check if all imports are working correctly.")

if __name__ == "__main__":
    install_packages()

