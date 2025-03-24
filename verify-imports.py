"""
Run this script to verify that all imports are working correctly.
"""

try:
    from datetime import datetime, timedelta
    print("✅ datetime imported successfully")
except ImportError:
    print("❌ Failed to import datetime (this should be part of Python standard library)")

try:
    import numpy as np
    print("✅ numpy imported successfully")
except ImportError:
    print("❌ Failed to import numpy")

try:
    import os
    print("✅ os imported successfully")
except ImportError:
    print("❌ Failed to import os (this should be part of Python standard library)")

try:
    import aiohttp
    print("✅ aiohttp imported successfully")
except ImportError:
    print("❌ Failed to import aiohttp")

try:
    import logging
    print("✅ logging imported successfully")
except ImportError:
    print("❌ Failed to import logging (this should be part of Python standard library)")

try:
    import math
    print("✅ math imported successfully")
except ImportError:
    print("❌ Failed to import math (this should be part of Python standard library)")

try:
    import random
    print("✅ random imported successfully")
except ImportError:
    print("❌ Failed to import random (this should be part of Python standard library)")

try:
    from fastapi import FastAPI, Query, HTTPException
    print("✅ fastapi imported successfully")
except ImportError:
    print("❌ Failed to import fastapi")

try:
    from fastapi.middleware.cors import CORSMiddleware
    print("✅ fastapi.middleware.cors imported successfully")
except ImportError:
    print("❌ Failed to import fastapi.middleware.cors")

try:
    from pydantic import BaseModel
    print("✅ pydantic imported successfully")
except ImportError:
    print("❌ Failed to import pydantic")

try:
    from dotenv import load_dotenv
    print("✅ dotenv imported successfully")
except ImportError:
    print("❌ Failed to import dotenv")

try:
    from typing import Dict, Any, List, Optional
    print("✅ typing imported successfully")
except ImportError:
    print("❌ Failed to import typing (this should be part of Python standard library)")

try:
    from urllib.parse import quote
    print("✅ urllib.parse imported successfully")
except ImportError:
    print("❌ Failed to import urllib.parse (this should be part of Python standard library)")

try:
    import neuralgcm
    print("✅ neuralgcm imported successfully")
except ImportError:
    print("❌ Failed to import neuralgcm (this might be a custom package)")

# Try to import your custom modules
try:
    from app.utils.kite_window_calculator import calculate_golden_kitewindow
    print("✅ app.utils.kite_window_calculator imported successfully")
except ImportError:
    print("❌ Failed to import app.utils.kite_window_calculator (check your project structure)")

try:
    from app.routers import kitespots
    print("✅ app.routers.kitespots imported successfully")
except ImportError:
    print("❌ Failed to import app.routers.kitespots (check your project structure)")

print("\nImport verification complete. Fix any failed imports before running your application.")

