import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_system.settings')

# Import Django and configure
import django
django.setup()

# --- RUN MIGRATIONS ON SERVERLESS START ---
from django.core.management import call_command
call_command('migrate', interactive=False)

# Import the WSGI application
from credit_system.wsgi import application

# This is the entry point for Vercel
app = application 