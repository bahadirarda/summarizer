"""
🔇 Warning Suppressor
This module should be imported first to suppress annoying warnings
"""

import warnings
import os
import sys

# Set environment variables before any imports
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['URLLIB3_WARNINGS_DISABLE'] = '1'

# Comprehensive warning suppression
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Specific urllib3 warnings
warnings.filterwarnings("ignore", "urllib3.*")
warnings.filterwarnings("ignore", ".*OpenSSL.*")
warnings.filterwarnings("ignore", ".*LibreSSL.*")

# Try to disable urllib3 warnings at module level
try:
    import urllib3
    urllib3.disable_warnings()
    # Disable all urllib3 warning categories
    from urllib3.exceptions import NotOpenSSLWarning, InsecureRequestWarning
    urllib3.disable_warnings(NotOpenSSLWarning)
    urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    pass
except Exception:
    pass

# Monkey patch warnings module for complete suppression
original_warn = warnings.warn
def silent_warn(*args, **kwargs):
    pass

warnings.warn = silent_warn
