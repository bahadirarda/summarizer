"""
API Utility Functions
"""
from flask import jsonify
from pathlib import Path
import sys

# Add src to path for imports  
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.utils.json_changelog_manager import JsonChangelogManager, ImpactLevel, ChangeType


def get_changelog_manager():
    """Get initialized changelog manager"""
    project_root = Path(__file__).parent.parent.parent
    return JsonChangelogManager(project_root)


def validate_enum_parameter(value, enum_class, param_name):
    """Validate and convert string parameter to enum"""
    if not value:
        return None
        
    try:
        return enum_class(value.lower())
    except ValueError:
        valid_values = [e.value for e in enum_class]
        raise ValueError(f"Invalid {param_name}: {value}. Valid values: {valid_values}")


def success_response(data, message=None, status_code=200):
    """Create standardized success response"""
    response = {"success": True, "data": data}
    if message:
        response["message"] = message
    return jsonify(response), status_code


def error_response(message, status_code=400, error_code=None):
    """Create standardized error response"""
    response = {
        "success": False,
        "error": message
    }
    if error_code:
        response["error_code"] = error_code
    return jsonify(response), status_code


def paginate_results(results, page=1, per_page=20):
    """Paginate results"""
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated = results[start:end]
    
    return {
        "items": paginated,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": len(results),
            "pages": (len(results) + per_page - 1) // per_page,
            "has_next": end < len(results),
            "has_prev": page > 1
        }
    }
