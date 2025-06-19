"""
Health Check and System Status Routes
"""

import sys
from datetime import datetime
from pathlib import Path

from flask import Blueprint

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.helpers import error_response, success_response

# Create Blueprint
bp = Blueprint("health", __name__, url_prefix="/api")


@bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    try:
        return success_response(
            {
                "status": "healthy",
                "service": "Summarizer Framework API",
                "version": "1.0.0",
                "timestamp": datetime.now().isoformat(),
                "components": {
                    "changelog_manager": "operational",
                    "file_tracker": "operational",
                    "ai_analysis": "operational",
                },
            }
        )
    except Exception as e:
        return error_response(f"Health check failed: {str(e)}", 500)


@bp.route("/info", methods=["GET"])
def get_info():
    """Get API information and available endpoints"""
    return success_response(
        {
            "name": "Summarizer Framework API",
            "version": "1.0.0",
            "description": "AI-powered changelog and code analysis API",
            "endpoints": {
                "changelog": {
                    "base": "/api/changelog",
                    "methods": ["GET"],
                    "description": "Access changelog entries with filtering and search",
                },
                "health": {
                    "base": "/api/health",
                    "methods": ["GET"],
                    "description": "Health check and system status",
                },
            },
            "features": [
                "AI-powered code analysis",
                "Automatic changelog generation",
                "File change tracking",
                "Semantic code categorization",
                "RESTful API access",
            ],
        }
    )
