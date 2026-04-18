"""
Configuration management for NFT Market Analytics API
======================================================

Handles:
- Environment variables loading (.env)
- API key validation
- Data paths
- Server settings
- Never hardcodes secrets
"""

import os
from dotenv import load_dotenv
from functools import lru_cache

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Configuration settings loaded from environment variables"""
    
    # ─────────────────────────────────────────────────────────────────────────
    # API KEYS (loaded from environment)
    # ─────────────────────────────────────────────────────────────────────────
    
    # Two API keys for two separate mobile apps
    API_KEY_APP1: str = os.getenv("API_KEY_APP1", "")
    API_KEY_APP2: str = os.getenv("API_KEY_APP2", "")
    
    # ─────────────────────────────────────────────────────────────────────────
    # DATA PATHS
    # ─────────────────────────────────────────────────────────────────────────
    
    # Directory containing CSV files
    DATA_PATH: str = os.getenv("DATA_PATH", "data")
    
    # ─────────────────────────────────────────────────────────────────────────
    # SERVER SETTINGS
    # ─────────────────────────────────────────────────────────────────────────
    
    # Port to run API on
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Host to bind to
    HOST: str = os.getenv("HOST", "0.0.0.0")
    
    # Environment (development, staging, production)
    ENV: str = os.getenv("ENV", "development")
    
    # ─────────────────────────────────────────────────────────────────────────
    # VALIDATION
    # ─────────────────────────────────────────────────────────────────────────
    
    @staticmethod
    def validate():
        """Validate all required settings are configured"""
        errors = []
        
        if not Settings.API_KEY_APP1:
            errors.append("API_KEY_APP1 not set in environment")
        
        if not Settings.API_KEY_APP2:
            errors.append("API_KEY_APP2 not set in environment")
        
        if not os.path.exists(Settings.DATA_PATH):
            errors.append(f"DATA_PATH '{Settings.DATA_PATH}' does not exist")
        
        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(errors))
    
    @staticmethod
    def summary():
        """Print configuration summary (safe - no keys shown)"""
        print("""
╔════════════════════════════════════════════════════════════╗
║          NFT Market Analytics API Configuration          ║
╚════════════════════════════════════════════════════════════╝

📋 Settings:
  • Environment: {}
  • Port: {}
  • Host: {}
  • Data Path: {}

🔐 API Keys:
  • API_KEY_APP1: {'✓ Set' if Settings.API_KEY_APP1 else '✗ Not set'}
  • API_KEY_APP2: {'✓ Set' if Settings.API_KEY_APP2 else '✗ Not set'}

════════════════════════════════════════════════════════════════
        """.format(Settings.ENV, Settings.PORT, Settings.HOST, Settings.DATA_PATH))


# Instantiate settings
settings = Settings()


# ═══════════════════════════════════════════════════════════════════════════════
# API KEY VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

@lru_cache(maxsize=1000)
def validate_api_key(key: str) -> bool:
    """
    Validate API key against configured keys.
    
    Args:
        key: API key to validate
    
    Returns:
        bool: True if key is valid, False otherwise
    
    Notes:
        - Uses caching for performance (~0ms)
        - Supports two separate keys (one per mobile app)
        - Case-sensitive comparison
    """
    if not key:
        return False
    
    valid_keys = [settings.API_KEY_APP1, settings.API_KEY_APP2]
    return key in valid_keys


def get_app_name(key: str) -> str:
    """
    Get app name from API key for logging.
    
    Args:
        key: API key
    
    Returns:
        str: App name (e.g., "Mobile App 1")
    """
    if key == settings.API_KEY_APP1:
        return "Mobile App 1"
    elif key == settings.API_KEY_APP2:
        return "Mobile App 2"
    return "Unknown"


# ═══════════════════════════════════════════════════════════════════════════════
# STARTUP CHECKS
# ═══════════════════════════════════════════════════════════════════════════════

try:
    settings.validate()
except ValueError as e:
    print(f"⚠️  Configuration Error: {e}")
    raise
