import logging
from pathlib import Path
from typing import Optional

from .file_tracker import (  # Import for getting changed files
    get_changed_files_since_last_run,
    get_file_line_changes,
    get_aggregate_line_stats,
    create_file_backups,
)
from .json_changelog_manager import JsonChangelogManager, ImpactLevel, ChangeType

logger_changelog = logging.getLogger(__name__)


def _detect_impact_level(summary: str, changed_files: list) -> ImpactLevel:
    """Auto-detect impact level based on summary and files"""
    summary_lower = summary.lower()

    # Critical indicators
    critical_keywords = [
        "critical",
        "hotfix",
        "security",
        "urgent",
        "emergency"]
    if any(keyword in summary_lower for keyword in critical_keywords):
        return ImpactLevel.CRITICAL

    # High impact indicators
    high_keywords = ["major", "breaking", "api", "database", "migration"]
    if any(keyword in summary_lower for keyword in high_keywords):
        return ImpactLevel.HIGH

    # Low impact indicators
    low_keywords = ["typo", "comment", "documentation", "readme", "formatting"]
    if any(keyword in summary_lower for keyword in low_keywords):
        return ImpactLevel.LOW

    # Based on file count
    if len(changed_files) > 10:
        return ImpactLevel.HIGH
    elif len(changed_files) <= 2:
        return ImpactLevel.LOW

    return ImpactLevel.MEDIUM


def update_changelog(project_root: Optional[Path] = None):
    """Update changelog with AI-generated summaries using JSON format"""
    if project_root is None:
        project_root = Path(__file__).resolve().parent.parent.parent
        logger_changelog.warning(
            f"project_root not provided to update_changelog, guessed as {project_root}")

    # Initialize JSON changelog manager
    json_manager = JsonChangelogManager(project_root)

    # Get changed files - check for different possible source directories
    changed_files = []
    try:
        # First try 'src' directory (for main project)
        if (project_root / "src").exists():
            changed_files = get_changed_files_since_last_run(
                project_root, "src")
        # If no src directory, scan current directory for Python files
        else:
            # Look for any Python files in the current directory
            python_files = list(project_root.glob("*.py"))
            if python_files:
                # For demo projects, track all Python files in the root
                changed_files = get_changed_files_since_last_run(
                    project_root, ".")
            else:
                logger_changelog.info("No Python files found to track.")

        if changed_files:
            logger_changelog.info(
                f"Detected changed files since last run: {changed_files}"
            )
        else:
            logger_changelog.info("No file changes detected since last run.")
            # Don't add fake files, just return if no changes
            return
    except Exception as e:
        logger_changelog.error(
            f"Error detecting changed files for changelog: {e}", exc_info=True
        )
        # Return if there's an error, don't create fake entries
        return

    # Analyze line changes
    line_changes = {}
    total_lines_added = 0
    total_lines_removed = 0

    try:
        line_changes = get_file_line_changes(project_root, changed_files)
        aggregate_stats = get_aggregate_line_stats(line_changes)
        total_lines_added = aggregate_stats["total_lines_added"]
        total_lines_removed = aggregate_stats["total_lines_removed"]

        logger_changelog.info(
            f"Line changes analysis: +{total_lines_added} -{total_lines_removed} "
            f"across {len(changed_files)} files"
        )

    except Exception as e:
        logger_changelog.error(
            f"Error analyzing line changes: {e}",
            exc_info=True)

    # Get AI summary using RequestManager
    try:
        from ..services.request_manager import RequestManager

        request_manager = RequestManager()
        gemini_client = request_manager.get_client("GeminiClient")
    except ValueError:
        logger_changelog.warning("GeminiClient not found in RequestManager.")
        gemini_client = None

    summary = "Genel güncelleme veya çalıştırma."
    impact_level = ImpactLevel.MEDIUM
    change_type = ChangeType.OTHER

    if gemini_client and gemini_client.is_ready():
        try:
            prompt = f"Aşağıdaki dosyalarda değişiklikler yapıldı: {', '.join(changed_files) if changed_files else 'Genel güncellemeler'}"
            ai_summary = gemini_client.generate_summary(
                text_prompt=prompt, changed_files=changed_files
            )
            summary = ai_summary
            logger_changelog.info(f"AI tarafından oluşturulan özet: {summary}")

            # Auto-detect impact level based on summary and files
            impact_level = _detect_impact_level(ai_summary, changed_files)

        except Exception as e:
            logger_changelog.error(
                f"GeminiClient'tan özet alınırken hata oluştu: {e}",
                exc_info=True)
            summary = "AI özeti alınamadı. Değişiklikler uygulandı."
    else:
        logger_changelog.warning(
            "GeminiClient kullanılamıyor. Varsayılan özet kullanılıyor."
        )

    # Add entry to JSON changelog
    entry_id = json_manager.add_entry(
        ai_summary=summary,
        changed_files=changed_files,
        impact_level=impact_level,
        change_type=change_type,
        lines_added=total_lines_added,
        lines_removed=total_lines_removed,
    )

    logger_changelog.info(f"Changelog entry added with ID: {entry_id}")

    # Create backups for next run comparison
    try:
        create_file_backups(project_root, "src")
        logger_changelog.debug("File backups created for future line analysis")
    except Exception as e:
        logger_changelog.error(
            f"Error creating file backups: {e}",
            exc_info=True)


def get_recent_changelog_entries(project_root: Path, count: int = 5) -> list:
    """Get the most recent changelog entries from JSON format"""
    try:
        json_manager = JsonChangelogManager(project_root)
        entries = json_manager.get_entries(limit=count)
        return [entry.__dict__ for entry in entries]
    except Exception as e:
        logger_changelog.error(f"Error reading changelog entries: {e}")
        return []


def get_changelog_stats(project_root: Path) -> dict:
    """Get changelog statistics"""
    try:
        json_manager = JsonChangelogManager(project_root)
        return json_manager.get_stats()
    except Exception as e:
        logger_changelog.error(f"Error getting changelog stats: {e}")
        return {}


def export_changelog(project_root: Path, format_type: str = "json") -> str:
    """Export changelog in specified format"""
    try:
        json_manager = JsonChangelogManager(project_root)
        return json_manager.export_to_format(format_type)
    except Exception as e:
        logger_changelog.error(f"Error exporting changelog: {e}")
        return ""


def demo_framework_analysis(
    project_root: Path, key_files: list, ai_summary: str
) -> str:
    """
    Demo function to showcase framework capabilities
    Creates a changelog entry for framework demonstration
    """
    logger_changelog.info("Running framework demonstration analysis...")

    try:
        # Initialize JSON changelog manager
        json_manager = JsonChangelogManager(project_root)

        # Calculate lines for demo files
        total_lines_added = 0
        total_lines_removed = 0

        try:
            line_changes = get_file_line_changes(key_files, project_root)
            aggregate_stats = get_aggregate_line_stats(line_changes)
            total_lines_added = aggregate_stats["total_lines_added"]
            total_lines_removed = aggregate_stats["total_lines_removed"]
        except Exception as e:
            logger_changelog.warning(
                f"Could not analyze line changes for demo: {e}")

        # Add demo entry to changelog
        entry_id = json_manager.add_entry(
            ai_summary=ai_summary,
            changed_files=key_files,
            impact_level=ImpactLevel.HIGH,
            change_type=ChangeType.DEMO,
            lines_added=total_lines_added,
            lines_removed=total_lines_removed,
            tags=["framework-demo", "api-server", "self-analysis"],
        )

        logger_changelog.info(
            f"Demo changelog entry added with ID: {entry_id}")
        return entry_id

    except Exception as e:
        logger_changelog.error(
            f"Error in demo framework analysis: {e}",
            exc_info=True)
        return ""
