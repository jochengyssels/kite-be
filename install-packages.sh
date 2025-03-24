#!/bin/bash

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install all packages from requirements.txt
pip install -r requirements.txt

# If neuralgcm is a custom package not available on PyPI, you might need to install it separately
# pip install -e /path/to/neuralgcm

# Verify installations
pip list

echo "Installation complete! Make sure your virtual environment is activated when running your app."

