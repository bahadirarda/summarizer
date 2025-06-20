#!/usr/bin/env python3
"""
🔧 Configuration Management

This module handles configuration for the Summarizer Framework.
Enhanced with better error handling and environment support...
"""

import logging
import os
import warnings
import urllib3

# Suppress urllib3 warnings safely
try:
    urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)
except (AttributeError, ImportError):
    # For older urllib3 versions, disable all warnings
    urllib3.disable_warnings()

# Also suppress it via warnings module for extra safety
warnings.filterwarnings("ignore", "urllib3 v2 only supports OpenSSL 1.1.1+", UserWarning)

# Version Information
__version__ = "2.0.0"
__title__ = "Summarizer Framework"
__description__ = "AI-Powered Project Summarizer with Enterprise GUI and Terminal Commands"
__author__ = "Bahadir Arda"
__date__ = "2025-06-11"


class BaseConfig:
    DEBUG = False
    # Diğer temel yapılandırmalar buraya eklenebilir


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_TO_CONSOLE = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    LOG_LEVEL = logging.WARNING  # Veya daha yüksek: ERROR, CRITICAL
    LOG_FORMAT = (
        # Prod için daha basit format
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    LOG_TO_CONSOLE = False  # Önemli: Loglar görünmeyecek


def get_config():
    env = os.getenv("APP_ENV", "development").lower()
    if env == "production":
        return ProductionConfig()
    return DevelopmentConfig()


APP_CONFIG = get_config()


def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(APP_CONFIG.LOG_LEVEL)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()

    if APP_CONFIG.LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(APP_CONFIG.LOG_LEVEL)
        formatter = logging.Formatter(APP_CONFIG.LOG_FORMAT)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    else:
        # Yayın ortamında, konsol loglaması kapalıysa, kütüphanelerden gelebilecek
        # "No handlers could be found" uyarılarını engellemek için NullHandler eklenir.
        null_handler = logging.NullHandler()
        root_logger.addHandler(null_handler)

    # Loglama kurulumunu onaylamak için bir başlangıç log mesajı
    # (sadece konsol loglaması aktifse görünür)
    # logging.debug doğrudan root logger'ı kullanır.
    logging.debug(
        "Loglama kurulumu tamamlandı. APP_ENV: '%s', Config: '%s'",
        os.getenv("APP_ENV", "development"),
        APP_CONFIG.__class__.__name__,
    )
