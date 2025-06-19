"""
Changelog API Routes
Handles all changelog-related endpoints
"""

import sys
from datetime import datetime
from pathlib import Path

from flask import Blueprint, jsonify, request

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.helpers import (
    error_response,
    get_changelog_manager,
    paginate_results,
    success_response,
    validate_enum_parameter,
)

# Import enums
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from src.utils.json_changelog_manager import ChangeType, ImpactLevel

# Create Blueprint
bp = Blueprint("changelog", __name__, url_prefix="/api/changelog")


@bp.route("/", methods=["GET"])
def get_changelog():
    """
    Get changelog entries with optional filters

    Query Parameters:
    - limit: Number of entries to return (default: 20)
    - page: Page number for pagination (default: 1)
    - type: Filter by change type (feature, bugfix, refactor, docs, config, test, other)
    - impact: Filter by impact level (low, medium, high, critical)
    - tags: Comma-separated list of tags to filter by
    - since: ISO timestamp to filter entries since this date
    - search: Search keyword in summaries and file names
    """
    try:
        changelog_manager = get_changelog_manager()

        # Parse query parameters
        limit = request.args.get("limit", 20, type=int)
        page = request.args.get("page", 1, type=int)
        change_type = request.args.get("type")
        impact_level = request.args.get("impact")
        tags = (
            request.args.get("tags", "").split(",")
            if request.args.get("tags")
            else None
        )
        since = request.args.get("since")
        search = request.args.get("search", "").strip()

        # Validate enums
        change_type_enum = validate_enum_parameter(
            change_type, ChangeType, "change type"
        )
        impact_level_enum = validate_enum_parameter(
            impact_level, ImpactLevel, "impact level"
        )

        # Get filtered entries
        entries = changelog_manager.get_entries(
            limit=None,  # Get all first, then paginate
            change_type=change_type_enum,
            impact_level=impact_level_enum,
            tags=tags,
            since=since,
        )

        # Apply search filter
        if search:
            search_lower = search.lower()
            entries = [
                entry
                for entry in entries
                if (
                    search_lower in entry.ai_summary.lower()
                    or any(search_lower in file.lower() for file in entry.changed_files)
                    or any(search_lower in tag.lower() for tag in entry.tags)
                )
            ]

        # Convert to dict format
        entries_data = [entry.__dict__ for entry in entries]

        # Apply pagination
        paginated_data = paginate_results(entries_data, page, limit)

        return success_response(
            {
                **paginated_data,
                "metadata": changelog_manager.changelog.metadata.__dict__,
            }
        )

    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"Internal error: {str(e)}", 500)


@bp.route("/stats", methods=["GET"])
def get_stats():
    """Get changelog statistics"""
    try:
        changelog_manager = get_changelog_manager()
        stats = changelog_manager.get_stats()

        # Add additional stats
        entries = changelog_manager.get_entries()

        # Calculate trends
        recent_entries = [
            e
            for e in entries
            if (datetime.now() - datetime.fromisoformat(e.timestamp)).days <= 7
        ]

        enhanced_stats = {
            **stats,
            "recent_activity": {
                "last_7_days": len(recent_entries),
                "avg_daily": len(recent_entries) / 7,
                "most_active_day": None,  # Could calculate this
            },
        }

        return success_response(enhanced_stats)

    except Exception as e:
        return error_response(f"Error getting stats: {str(e)}", 500)


@bp.route("/entry/<entry_id>", methods=["GET"])
def get_entry(entry_id):
    """Get specific changelog entry by ID"""
    try:
        changelog_manager = get_changelog_manager()
        entries = changelog_manager.get_entries()
        entry = next((e for e in entries if e.id == entry_id), None)

        if not entry:
            return error_response("Entry not found", 404)

        return success_response(entry.__dict__)

    except Exception as e:
        return error_response(f"Error getting entry: {str(e)}", 500)


@bp.route("/export", methods=["GET"])
def export_changelog():
    """
    Export changelog in different formats

    Query Parameters:
    - format: Export format (json, markdown) - default: json
    """
    try:
        changelog_manager = get_changelog_manager()
        format_type = request.args.get("format", "json")

        if format_type not in ["json", "markdown"]:
            return error_response("Supported formats: json, markdown", 400)

        content = changelog_manager.export_to_format(format_type)

        # Return raw content with appropriate content type
        from flask import Response

        if format_type == "json":
            return Response(
                content,
                mimetype="application/json",
                headers={"Content-Disposition": "attachment; filename=changelog.json"},
            )
        else:  # markdown
            return Response(
                content,
                mimetype="text/markdown",
                headers={"Content-Disposition": "attachment; filename=CHANGELOG.md"},
            )

    except Exception as e:
        return error_response(f"Error exporting: {str(e)}", 500)


@bp.route("/search", methods=["GET"])
def search_changelog():
    """
    Search changelog entries by keyword

    Query Parameters:
    - q: Search query (required)
    - limit: Number of results to return (default: 20)
    """
    try:
        query = request.args.get("q", "").strip()
        if not query:
            return error_response("Query parameter 'q' is required", 400)

        limit = request.args.get("limit", 20, type=int)

        changelog_manager = get_changelog_manager()
        entries = changelog_manager.get_entries()

        # Search logic
        query_lower = query.lower()
        filtered_entries = []

        for entry in entries:
            score = 0

            # Score based on matches
            if query_lower in entry.ai_summary.lower():
                score += 3
            if any(query_lower in file.lower() for file in entry.changed_files):
                score += 2
            if any(query_lower in tag.lower() for tag in entry.tags):
                score += 1

            if score > 0:
                entry_dict = entry.__dict__
                entry_dict["relevance_score"] = score
                filtered_entries.append(entry_dict)

        # Sort by relevance score
        filtered_entries.sort(key=lambda x: x["relevance_score"], reverse=True)

        # Apply limit
        filtered_entries = filtered_entries[:limit]

        return success_response(
            {
                "query": query,
                "results": filtered_entries,
                "count": len(filtered_entries),
            }
        )

    except Exception as e:
        return error_response(f"Error searching: {str(e)}", 500)


@bp.route("/timeline", methods=["GET"])
def get_timeline():
    """
    Get changelog timeline grouped by date

    Query Parameters:
    - granularity: Group by 'day', 'week', 'month' (default: day)
    """
    try:
        changelog_manager = get_changelog_manager()
        entries = changelog_manager.get_entries()
        granularity = request.args.get("granularity", "day")

        if granularity not in ["day", "week", "month"]:
            return error_response("Granularity must be 'day', 'week', or 'month'", 400)

        # Group by specified granularity
        timeline = {}

        for entry in entries:
            dt = datetime.fromisoformat(entry.timestamp)

            if granularity == "day":
                key = dt.strftime("%Y-%m-%d")
            elif granularity == "week":
                # Get Monday of the week
                monday = dt - datetime.timedelta(days=dt.weekday())
                key = monday.strftime("%Y-%m-%d (Week)")
            else:  # month
                key = dt.strftime("%Y-%m")

            if key not in timeline:
                timeline[key] = {
                    "entries": [],
                    "stats": {"total": 0, "by_type": {}, "by_impact": {}},
                }

            entry_dict = entry.__dict__
            timeline[key]["entries"].append(entry_dict)
            timeline[key]["stats"]["total"] += 1

            # Update stats
            change_type = entry_dict["change_type"]
            impact_level = entry_dict["impact_level"]

            timeline[key]["stats"]["by_type"][change_type] = (
                timeline[key]["stats"]["by_type"].get(change_type, 0) + 1
            )
            timeline[key]["stats"]["by_impact"][impact_level] = (
                timeline[key]["stats"]["by_impact"].get(impact_level, 0) + 1
            )

        # Sort by date descending
        sorted_timeline = dict(sorted(timeline.items(), reverse=True))

        return success_response(
            {
                "timeline": sorted_timeline,
                "granularity": granularity,
                "total_periods": len(sorted_timeline),
                "total_entries": len(entries),
            }
        )

    except Exception as e:
        return error_response(f"Error creating timeline: {str(e)}", 500)


@bp.route("/tags", methods=["GET"])
def get_tags():
    """Get all available tags with usage counts"""
    try:
        changelog_manager = get_changelog_manager()
        entries = changelog_manager.get_entries()

        tag_counts = {}
        for entry in entries:
            for tag in entry.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # Sort by usage count
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)

        return success_response(
            {
                "tags": [{"name": tag, "count": count} for tag, count in sorted_tags],
                "total_unique_tags": len(tag_counts),
            }
        )

    except Exception as e:
        return error_response(f"Error getting tags: {str(e)}", 500)
