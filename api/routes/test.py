"""
Test Routes - Simple endpoints without complex imports
"""

from datetime import datetime

from flask import Blueprint, jsonify

# Create Blueprint
bp = Blueprint("test", __name__, url_prefix="/api")


@bp.route("/test", methods=["GET"])
def test_endpoint():
    """Simple test endpoint"""
    return jsonify(
        {
            "success": True,
            "message": "API is working!",
            "timestamp": datetime.now().isoformat(),
            "server": "Summarizer Framework API",
        }
    )


@bp.route("/ping", methods=["GET"])
def ping():
    """Ping endpoint"""
    return jsonify({"status": "pong"})
