"""
Environment and dependency validation system.
Prevents runtime failures by validating all prerequisites before execution.
"""
import importlib
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

class EnvironmentValidator:
    """Validates all system dependencies and environment variables."""
    
    REQUIRED_ENV_VARS = {
        'GOOGLE_APPLICATION_CREDENTIALS': 'Firebase service account JSON path',
        'FIREBASE_PROJECT_ID': 'Firebase project identifier',
        'DEEPSEEK_API_KEY': 'Optional: DeepSeek API key for fallback',
        'TELEGRAM_BOT_TOKEN': 'Optional: For emergency notifications',
        'TELEGRAM_CHAT_ID': 'Optional: Telegram recipient ID',
    }
    
    REQUIRED_PACKAGES = [
        'firebase_admin',
        'google.cloud.firestore',
        'requests',
        'tenacity',
        'pydantic',
        'structlog',
        'dotenv',
    ]
    
    REQUIRED_DIRS = [
        'logs',
        'state',
        'backups',
    ]
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.validation_results: Dict[str, bool] = {}
        self.missing_items: Dict[str, List[str]] = {
            'env_vars': [],
            'packages': [],
            'directories': [],
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Configure structured logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/validation.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def validate_all(self) -> Tuple[bool, Dict[str, List[str]]]: