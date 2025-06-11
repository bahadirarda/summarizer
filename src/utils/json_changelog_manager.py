"""
JSON Changelog Manager
Manages structured changelog data in JSON format for API consumption
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ImpactLevel(Enum):
    """Impact level of changes"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ChangeType(Enum):
    """Type of change made"""

    FEATURE = "feature"
    BUGFIX = "bugfix"
    REFACTOR = "refactor"
    DOCS = "docs"
    CONFIG = "config"
    TEST = "test"
    DEMO = "demo"
    OTHER = "other"


@dataclass
class ChangelogEntry:
    """Structured changelog entry"""

    id: str
    timestamp: str
    ai_summary: str
    changed_files: List[str]
    impact_level: str = ImpactLevel.MEDIUM.value
    change_type: str = ChangeType.OTHER.value
    tags: List[str] = None
    file_count: int = 0
    lines_added: int = 0
    lines_removed: int = 0
    commit_hash: Optional[str] = None
    author: Optional[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.file_count == 0:
            self.file_count = len(self.changed_files)


@dataclass
class ChangelogMetadata:
    """Metadata for the changelog"""

    version: str = "1.0"
    project_name: str = "Summarizer Framework"
    created_at: str = ""
    last_updated: str = ""
    total_entries: int = 0

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.last_updated = datetime.now().isoformat()


@dataclass
class JsonChangelog:
    """Complete JSON changelog structure"""

    metadata: ChangelogMetadata
    entries: List[ChangelogEntry]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "metadata": asdict(self.metadata),
            "entries": [asdict(entry) for entry in self.entries],
        }


class JsonChangelogManager:
    """Manager for JSON-based changelog system"""

    def __init__(self, project_root: Optional[Path] = None):
        self.logger = logging.getLogger(__name__)
        self.project_root = project_root or Path.cwd()
        self.json_file = self.project_root / "changelog.json"
        self.markdown_file = self.project_root / "CHANGELOG.md"

        # Load existing changelog or create new one
        self.changelog = self._load_changelog()

    def _load_changelog(self) -> JsonChangelog:
        """Load existing changelog or create new one"""
        if self.json_file.exists():
            try:
                with open(self.json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                metadata = ChangelogMetadata(**data.get("metadata", {}))
                entries = [ChangelogEntry(**entry)
                           for entry in data.get("entries", [])]

                self.logger.info(
                    f"Loaded changelog with {len(entries)} entries")
                return JsonChangelog(metadata=metadata, entries=entries)

            except Exception as e:
                self.logger.error(f"Error loading changelog: {e}")

        # Create new changelog
        metadata = ChangelogMetadata()
        return JsonChangelog(metadata=metadata, entries=[])

    def _save_changelog(self) -> None:
        """Save changelog to JSON file"""
        try:
            # Update metadata
            self.changelog.metadata.last_updated = datetime.now().isoformat()
            self.changelog.metadata.total_entries = len(self.changelog.entries)

            # Save to JSON
            with open(self.json_file, "w", encoding="utf-8") as f:
                json.dump(
                    self.changelog.to_dict(),
                    f,
                    indent=2,
                    ensure_ascii=False)

            self.logger.info(f"Changelog saved to {self.json_file}")

        except Exception as e:
            self.logger.error(f"Error saving changelog: {e}")
            raise

    def add_entry(
        self,
        ai_summary: str,
        changed_files: List[str],
        impact_level: ImpactLevel = ImpactLevel.MEDIUM,
        change_type: ChangeType = ChangeType.OTHER,
        tags: Optional[List[str]] = None,
        lines_added: int = 0,
        lines_removed: int = 0,
        commit_hash: Optional[str] = None,
        author: Optional[str] = None,
    ) -> str:
        """Add new changelog entry"""

        # Generate unique ID
        timestamp = datetime.now()
        entry_id = f"entry_{timestamp.strftime('%Y%m%d_%H%M%S')}"

        # Auto-detect change type from files
        detected_type = self._detect_change_type(changed_files)
        if change_type == ChangeType.OTHER:
            change_type = detected_type

        # Auto-generate tags
        auto_tags = self._generate_tags(changed_files, ai_summary)
        if tags:
            auto_tags.extend(tags)
        tags = list(set(auto_tags))  # Remove duplicates

        # Create entry
        entry = ChangelogEntry(
            id=entry_id,
            timestamp=timestamp.isoformat(),
            ai_summary=ai_summary,
            changed_files=changed_files,
            impact_level=impact_level.value,
            change_type=change_type.value,
            tags=tags,
            lines_added=lines_added,
            lines_removed=lines_removed,
            commit_hash=commit_hash,
            author=author,
        )

        # Add to changelog
        self.changelog.entries.insert(0, entry)  # Latest first

        # Save and regenerate markdown
        self._save_changelog()
        self._generate_markdown()

        self.logger.info(f"Added changelog entry: {entry_id}")
        return entry_id

    def _detect_change_type(self, files: List[str]) -> ChangeType:
        """Auto-detect change type from file paths"""
        file_patterns = {
            ChangeType.TEST: [
                "test_",
                "tests/",
                "_test.py",
                ".test."],
            ChangeType.DOCS: [
                "README",
                "CHANGELOG",
                ".md",
                "docs/",
                "documentation"],
            ChangeType.CONFIG: [
                "config",
                ".json",
                ".yaml",
                ".yml",
                ".env",
                "settings"],
            ChangeType.FEATURE: [
                "src/",
                "lib/",
                "app/"],
        }

        for file_path in files:
            file_lower = file_path.lower()
            for change_type, patterns in file_patterns.items():
                if any(pattern in file_lower for pattern in patterns):
                    return change_type

        return ChangeType.OTHER

    def _generate_tags(self, files: List[str], summary: str) -> List[str]:
        """Auto-generate tags from files and summary"""
        tags = []

        # Extract from file paths
        for file_path in files:
            parts = Path(file_path).parts
            for part in parts:
                if part not in ["src", "lib", "app", "__pycache__"]:
                    tags.append(part.replace(".py", "").replace("_", "-"))

        # Extract from summary (simple keyword detection)
        keywords = [
            "api",
            "gui",
            "config",
            "database",
            "client",
            "manager",
            "utils"]
        summary_lower = summary.lower()
        for keyword in keywords:
            if keyword in summary_lower:
                tags.append(keyword)

        return list(set(tags))[:10]  # Limit to 10 tags

    def _generate_markdown(self) -> None:
        """Generate markdown changelog from JSON data"""
        try:
            lines = []
            lines.append("# Changelog")
            lines.append("")
            lines.append("Bu dosya otomatik olarak generate edilmiştir.")
            lines.append(
                "Düzenlemeler için `changelog.json` dosyasını kullanın.")
            lines.append("")

            for entry in self.changelog.entries:
                # Header with timestamp
                dt = datetime.fromisoformat(entry.timestamp)
                lines.append(f"## {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                lines.append("")

                # Summary
                lines.append(entry.ai_summary)
                lines.append("")

                # Metadata
                lines.append(
                    f"**Değişen Dosyalar:** {', '.join(entry.changed_files)}")
                lines.append(
                    f"**Etki Seviyesi:** {entry.impact_level.title()}")
                lines.append(
                    f"**Değişiklik Tipi:** {entry.change_type.title()}")

                # Line change information
                if entry.lines_added > 0 or entry.lines_removed > 0:
                    line_summary = []
                    if entry.lines_added > 0:
                        line_summary.append(f"+{entry.lines_added}")
                    if entry.lines_removed > 0:
                        line_summary.append(f"-{entry.lines_removed}")
                    lines.append(
                        f"**Satır Değişiklikleri:** {' '.join(line_summary)}")

                if entry.tags:
                    lines.append(f"**Etiketler:** {', '.join(entry.tags)}")

                if entry.commit_hash:
                    lines.append(f"**Commit:** `{entry.commit_hash}`")

                lines.append("")
                lines.append("---")
                lines.append("")

            # Write to file
            with open(self.markdown_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

            self.logger.info(
                f"Generated markdown changelog: {self.markdown_file}")

        except Exception as e:
            self.logger.error(f"Error generating markdown: {e}")

    def get_entries(
        self,
        limit: Optional[int] = None,
        change_type: Optional[ChangeType] = None,
        impact_level: Optional[ImpactLevel] = None,
        tags: Optional[List[str]] = None,
        since: Optional[str] = None,
    ) -> List[ChangelogEntry]:
        """Query changelog entries with filters"""
        entries = self.changelog.entries.copy()

        # Apply filters
        if change_type:
            entries = [
                e for e in entries if e.change_type == change_type.value]

        if impact_level:
            entries = [
                e for e in entries if e.impact_level == impact_level.value]

        if tags:
            entries = [
                e for e in entries if any(
                    tag in e.tags for tag in tags)]

        if since:
            since_dt = datetime.fromisoformat(since)
            entries = [
                e for e in entries if datetime.fromisoformat(
                    e.timestamp) >= since_dt]

        # Apply limit
        if limit:
            entries = entries[:limit]

        return entries

    def get_stats(self) -> Dict[str, Any]:
        """Get changelog statistics"""
        entries = self.changelog.entries

        if not entries:
            return {"total": 0}

        # Count by type
        type_counts = {}
        impact_counts = {}

        for entry in entries:
            type_counts[entry.change_type] = type_counts.get(
                entry.change_type, 0) + 1
            impact_counts[entry.impact_level] = (
                impact_counts.get(entry.impact_level, 0) + 1
            )

        # Get date range
        timestamps = [datetime.fromisoformat(e.timestamp) for e in entries]

        return {
            "total": len(entries),
            "first_entry": min(timestamps).isoformat(),
            "last_entry": max(timestamps).isoformat(),
            "by_type": type_counts,
            "by_impact": impact_counts,
            "total_files_changed": sum(len(e.changed_files) for e in entries),
        }

    def export_to_format(self, format_type: str = "json") -> str:
        """Export changelog in different formats"""
        if format_type == "json":
            return json.dumps(
                self.changelog.to_dict(),
                indent=2,
                ensure_ascii=False)
        elif format_type == "markdown":
            with open(self.markdown_file, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported format: {format_type}")
