"""
API Configuration and Base Setup
"""

import sys
from pathlib import Path

from flask import Flask

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)

    # Configuration
    app.config["JSON_SORT_KEYS"] = False
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

    # Register blueprints automatically
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    return app


def register_blueprints(app):
    """Automatically register all blueprints from routes directory"""
    import importlib
    from pathlib import Path

    routes_dir = Path(__file__).parent / "routes"

    # Scan for route files
    for route_file in routes_dir.glob("*.py"):
        if route_file.name.startswith("_"):
            continue

        module_name = f"api.routes.{route_file.stem}"

        try:
            # Import the module
            module = importlib.import_module(module_name)

            # Look for blueprint in the module
            if hasattr(module, "bp"):
                app.register_blueprint(module.bp)
                print(f"✅ Registered blueprint: {module_name}")
            else:
                print(f"⚠️  No blueprint found in {module_name}")

        except Exception as e:
            print(f"❌ Error loading {module_name}: {e}")


def register_error_handlers(app):
    """Register global error handlers"""
    from flask import jsonify

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "error": "Endpoint not found",
                    "message": "The requested URL was not found on the server.",
                }
            ),
            404,
        )

    @app.errorhandler(500)
    def internal_error(error):
        return (
            jsonify(
                {
                    "error": "Internal server error",
                    "message": "An internal error occurred. Please try again later.",
                }
            ),
            500,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {
                    "error": "Bad request",
                    "message": "The request was invalid or cannot be served.",
                }
            ),
            400,
        )
