import json
import logging
import os
from pathlib import Path

STATE_FILE_NAME = ".file_states.json"
SUMMARIZER_DIR = ".summarizer"
logger = logging.getLogger(__name__)


def get_changed_files_since_last_run(
    project_root_path: Path, watch_dir: str = "src"
) -> list[str]:
    """
    Identifies .py files under watch_dir that have been modified since the last run.
    Updates a state file with current modification times.
    Returns a list of file paths relative to the project_root_path.
    """
    # Create .summarizer directory if it doesn't exist
    summarizer_dir = project_root_path / SUMMARIZER_DIR
    summarizer_dir.mkdir(exist_ok=True)
    
    state_file_path = summarizer_dir / STATE_FILE_NAME
    tracked_dir_path = project_root_path / watch_dir

    previous_states = {}
    if state_file_path.exists():
        try:
            with open(state_file_path, "r", encoding="utf-8") as f:
                previous_states = json.load(f)
            logger.debug(f"Loaded previous states from {state_file_path}")
        except json.JSONDecodeError:
            logger.warning(
                f"Corrupted state file {state_file_path}. Assuming all files changed.")
            previous_states = {}
        except Exception as e:
            logger.error(f"Error loading state file {state_file_path}: {e}")
            previous_states = {}
    else:
        logger.info(
            f"State file {state_file_path} not found. "
            f"Assuming first run or all files changed."
        )

    current_states = {}
    changed_files_relative_paths = []

    if not tracked_dir_path.is_dir():
        logger.warning(
            f"Watch directory {tracked_dir_path} does not exist. "
            f"No files will be tracked."
        )
        return []

    for file_path_obj in tracked_dir_path.rglob("*.py"):
        if "__pycache__" in str(
                file_path_obj.parts):  # Check parts for __pycache__
            continue
        
        # Skip .summarizer directory to avoid infinite recursion
        if SUMMARIZER_DIR in str(file_path_obj.parts):
            continue

        try:
            relative_path_str = str(
                file_path_obj.relative_to(project_root_path))
            current_mtime = os.path.getmtime(file_path_obj)
            current_states[relative_path_str] = current_mtime

            if previous_states.get(relative_path_str) != current_mtime:
                changed_files_relative_paths.append(relative_path_str)
                logger.debug(
                    f"Detected change in: {relative_path_str} "
                    f"(new_mtime: {current_mtime}, "
                    f"old_mtime: {previous_states.get(relative_path_str)})"
                )
            elif (
                relative_path_str not in previous_states
            ):  # New file not caught by mtime diff if mtime is same
                # (unlikely but good to have)
                changed_files_relative_paths.append(relative_path_str)
                logger.debug(
                    f"Detected new file: {relative_path_str} (mtime: {current_mtime})")

        except FileNotFoundError:
            logger.warning(
                f"File {file_path_obj} not found during scan, might have been deleted.")
            continue
        except Exception as e:
            logger.error(f"Error processing file {file_path_obj}: {e}")
            continue

    # Optionally, detect deleted files:
    # deleted_files = [path for path in previous_states if path not in current_states]
    # if deleted_files:
    #     logger.info(f"Detected deleted files: {deleted_files}")
    #     # You might want to add these to changed_files_relative_paths with a
    # special marker or handle separately

    try:
        with open(state_file_path, "w", encoding="utf-8") as f:
            json.dump(current_states, f, indent=4)
        logger.debug(f"Saved current states to {state_file_path}")
    except IOError as e:
        logger.error(f"Could not write to state file {state_file_path}: {e}")
    except Exception as e:
        logger.error(
            f"Unexpected error writing state file {state_file_path}: {e}")

    return changed_files_relative_paths


def get_file_line_changes(
    project_root_path: Path, changed_files: list[str]
) -> dict[str, dict[str, int]]:
    """
    Analyzes line changes for each changed file by comparing current state with backup.
    Returns a dictionary with file paths as keys and line change stats as values.

    Returns:
        {
            "file_path": {
                "lines_added": int,
                "lines_removed": int,
                "lines_total": int,
                "change_ratio": float
            }
        }
    """
    line_changes = {}
    summarizer_dir = project_root_path / SUMMARIZER_DIR
    backup_dir = summarizer_dir / "file_backups"

    for file_path in changed_files:
        full_path = project_root_path / file_path
        backup_path = backup_dir / file_path

        if not full_path.exists():
            logger.warning(f"File {file_path} no longer exists")
            continue

        try:
            # Read current file
            with open(full_path, "r", encoding="utf-8") as f:
                current_lines = f.readlines()

            current_count = len(current_lines)

            # Read backup if exists
            if backup_path.exists():
                try:
                    with open(backup_path, "r", encoding="utf-8") as f:
                        backup_lines = f.readlines()
                    backup_count = len(backup_lines)

                    # Simple line count difference (more sophisticated diff could be
                    # added)
                    line_diff = current_count - backup_count

                    if line_diff > 0:
                        lines_added = line_diff
                        lines_removed = 0
                    elif line_diff < 0:
                        lines_added = 0
                        lines_removed = abs(line_diff)
                    else:
                        # Same line count, but content might have changed
                        # Do a simple content comparison
                        changed_lines = sum(
                            1
                            for i, (curr, back) in enumerate(
                                zip(current_lines, backup_lines)
                            )
                            if curr != back
                        )
                        lines_added = changed_lines // 2  # Rough estimate
                        lines_removed = changed_lines // 2

                except Exception as e:
                    logger.warning(
                        f"Could not read backup for {file_path}: {e}")
                    # If no backup, treat as all lines added
                    lines_added = current_count
                    lines_removed = 0
            else:
                # No backup exists, treat as new file
                lines_added = current_count
                lines_removed = 0

            change_ratio = (lines_added + lines_removed) / \
                max(current_count, 1)

            line_changes[file_path] = {
                "lines_added": lines_added,
                "lines_removed": lines_removed,
                "lines_total": current_count,
                "change_ratio": round(change_ratio, 3),
            }

            logger.debug(
                f"Line analysis for {file_path}: +{lines_added} -{lines_removed} "
                f"(total: {current_count})"
            )

        except Exception as e:
            logger.error(f"Error analyzing lines for {file_path}: {e}")
            line_changes[file_path] = {
                "lines_added": 0,
                "lines_removed": 0,
                "lines_total": 0,
                "change_ratio": 0.0,
            }

    return line_changes


def create_file_backups(
        project_root_path: Path,
        watch_dir: str = "src") -> None:
    """
    Creates backup copies of current files for future line diff analysis.
    Should be called after processing changes.
    """
    # Create .summarizer directory if it doesn't exist
    summarizer_dir = project_root_path / SUMMARIZER_DIR
    summarizer_dir.mkdir(exist_ok=True)
    
    backup_dir = summarizer_dir / "file_backups"
    tracked_dir_path = project_root_path / watch_dir

    if not tracked_dir_path.is_dir():
        return

    backup_dir.mkdir(exist_ok=True)

    for file_path_obj in tracked_dir_path.rglob("*.py"):
        if "__pycache__" in str(file_path_obj.parts):
            continue
        
        # Skip .summarizer directory to avoid infinite recursion
        if SUMMARIZER_DIR in str(file_path_obj.parts):
            continue

        try:
            relative_path = file_path_obj.relative_to(project_root_path)
            backup_path = backup_dir / relative_path

            # Create backup directory structure
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy file content
            with open(file_path_obj, "r", encoding="utf-8") as src, open(
                backup_path, "w", encoding="utf-8"
            ) as dst:
                dst.write(src.read())

        except Exception as e:
            logger.error(f"Error creating backup for {file_path_obj}: {e}")


def get_aggregate_line_stats(line_changes: dict) -> dict:
    """
    Aggregates line change statistics across all files.
    """
    if not line_changes:
        return {
            "total_lines_added": 0,
            "total_lines_removed": 0,
            "total_files_changed": 0,
            "average_change_ratio": 0.0,
        }

    total_added = sum(stats["lines_added"] for stats in line_changes.values())
    total_removed = sum(stats["lines_removed"]
                        for stats in line_changes.values())
    total_files = len(line_changes)
    avg_ratio = (sum(stats["change_ratio"]
                     for stats in line_changes.values()) / total_files)

    return {
        "total_lines_added": total_added,
        "total_lines_removed": total_removed,
        "total_files_changed": total_files,
        "average_change_ratio": round(avg_ratio, 3),
    }
