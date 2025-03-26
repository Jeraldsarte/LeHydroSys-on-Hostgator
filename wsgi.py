import sys
import os

# Add Flask project directory to system path
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application  # WSGI requires 'application'
