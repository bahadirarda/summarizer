"""
Summarizer Framework API Server
Modular REST API for changelog and code analysis
"""
from api.config import create_app
import sys
from pathlib import Path

# Add API directory to path
sys.path.insert(0, str(Path(__file__).parent / "api"))
# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def main():
    """Main entry point"""
    app = create_app()

    print("🚀 Starting Summarizer Framework API Server...")
    print("=" * 60)

    # Only run framework demo when not in debug reload mode
    import os
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        # Run framework demo only on first startup
        from src.main import summarizer
        summarizer()

    print("📊 Available Endpoints:")
    print()
    print("🔍 CHANGELOG API:")
    print("   GET  /api/changelog/          - Get changelog entries")
    print("   GET  /api/changelog/stats     - Get statistics")
    print("   GET  /api/changelog/entry/<id> - Get specific entry")
    print("   GET  /api/changelog/export    - Export (json/markdown)")
    print("   GET  /api/changelog/search    - Search entries")
    print("   GET  /api/changelog/timeline  - Get timeline view")
    print("   GET  /api/changelog/tags      - Get available tags")
    print()
    print("🏥 SYSTEM API:")
    print("   GET  /api/health              - Health check")
    print("   GET  /api/info                - API information")
    print()
    print("📖 DOCUMENTATION:")
    print("   GET  /                        - API Documentation")
    print()
    print("=" * 60)
    print("🌐 Server running on: http://localhost:5003")
    print("📚 Documentation: http://localhost:5003")
    print("=" * 60)
    print()

    app.run(debug=True, host='0.0.0.0', port=5003)


if __name__ == '__main__':
    main()
