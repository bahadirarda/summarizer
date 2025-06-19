import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Any
import re
import sys
import subprocess
import urllib.parse

from .file_tracker import (  # Import for getting changed files
    get_changed_files_since_last_run,
    get_file_line_changes,
    get_aggregate_line_stats,
    create_file_backups,
)
from .json_changelog_manager import JsonChangelogManager, ImpactLevel, ChangeType
from .readme_generator import update_readme
from .version_manager import VersionManager
from .git_manager import GitManager

logger_changelog = logging.getLogger(__name__)


def _detect_impact_level(summary: str, changed_files: list) -> ImpactLevel:
    """Auto-detect impact level based on summary and files"""
    summary_lower = summary.lower()

    # Critical indicators
    critical_keywords = [
        "critical",
        "hotfix",
        "security"]
    if any(keyword in summary_lower for keyword in critical_keywords):
        return ImpactLevel.CRITICAL

    # High impact indicators
    high_keywords = ["major", "breaking", "api"]
    if any(keyword in summary_lower for keyword in high_keywords):
        return ImpactLevel.HIGH

    # Low impact indicators
    low_keywords = ["typo", "docs", "readme"]
    if any(keyword in summary_lower for keyword in low_keywords):
        return ImpactLevel.LOW

    # Based on file count
    if len(changed_files) > 10:
        return ImpactLevel.HIGH
    elif len(changed_files) <= 2:
        return ImpactLevel.LOW

    return ImpactLevel.MEDIUM


def _ask_user(prompt: str) -> bool:
    try:
        return input(f"{prompt} (y/n): ").lower() == 'y'
    except (EOFError, KeyboardInterrupt):
        return False


def _run_ci_checks(project_root: Path) -> bool:
    ci_script_path = project_root / "scripts" / "run_ci_checks.py"
    if not ci_script_path.exists():
        print(f"   ❌ CI script not found at {ci_script_path}")
        return False
    # Pass '-s' to pytest to disable output capture, allowing interactive prompts if necessary for testing
    ci_process = subprocess.run([sys.executable, str(ci_script_path), '-s'], cwd=project_root)
    if ci_process.returncode == 0:
        print("   ✅ All CI checks passed.")
        return True
    else:
        print("   ❌ CI checks failed.")
        return False


def _write_next_command(project_root: Path, command: str):
    command_file_path = project_root / ".summarizer" / "next_command.sh"
    try:
        with open(command_file_path, "w") as f: f.write(f"{command}\n")
        print(f"   ✨ Next step command generated: {command}")
    except Exception as e:
        logger_changelog.error(f"Could not create next_command.sh file: {e}")


def _handle_pull_request_flow(project_root: Path, git_manager: GitManager, current_branch: str, target_branch: str, pr_body: str, gemini_client: Any = None):
    """
    Handles the pull request creation process intelligently.
    It first pushes the changes and then creates the PR.
    """
    prompt_message = f"   ❔ Push changes on '{current_branch}' and create a Pull Request to '{target_branch}'?"
    if not _ask_user(prompt_message):
        print("   ⚪️ Operation skipped by user.")
        return

    # Step 1: Run pre-push CI checks
    if not _run_ci_checks(project_root):
        if not _ask_user("   ⚠️  CI checks failed. Proceed with push and PR anyway?"):
            print("   ⚪️ Operation aborted due to CI failure.")
            return

    # Step 2: Push the branch to the remote
    print(f"   🚀 Pushing changes on '{current_branch}' to remote...")
    push_success, push_output = git_manager.push(current_branch)

    if not push_success:
        print(f"   ❌ Push failed. Git Error:\n{push_output}")
        # Even if push fails, it might be because the branch is already up-to-date.
        # Let's check for that specific case.
        if "already up-to-date" not in push_output and "up to date" not in push_output:
            return # A real error occurred, so we stop.
    
    # If the branch was already up-to-date, there are no new commits to create a PR with.
    if "already up-to-date" in push_output or "up to date" in push_output:
         print(f"   ⚪️ Branch '{current_branch}' is already up-to-date with the remote. No new commits to create a PR for.")
         return
         
    print("   ✅ Branch pushed successfully.")
    
    # Step 3: Create the Pull Request
    print("   🤖 Generating AI-powered pull request details...")
    pr_title, new_pr_body = git_manager.generate_pull_request_details(pr_body, gemini_client)
    print(f"   📝 PR Title: {pr_title}")
    
    pr_url = git_manager.create_pull_request(
        title=pr_title, body=new_pr_body, base_branch=target_branch, head_branch=current_branch
    )

    if pr_url:
        print(f"   ✅ Successfully created Pull Request: {pr_url}")
    else:
        print("   ❌ Failed to create Pull Request.")
        print("   You may need to create it manually on GitHub.")


def _handle_release_creation(project_root: Path, git_manager: GitManager, new_version: str):
    release_branch_name = f"release/v{new_version}"
    if _ask_user(f"   ❔ Run CI checks and create release branch '{release_branch_name}'?"):
        if not _run_ci_checks(project_root):
            if not _ask_user("   ⚠️  CI checks failed. Create branch anyway?"):
                return
        if git_manager.create_branch(release_branch_name):
            _write_next_command(project_root, f"git checkout {release_branch_name}")
        else:
            print(f"   ⚠️  Could not create release branch '{release_branch_name}'.")


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
        print("   🔍 Scanning for changed files...")
        # Use dynamic directory discovery (no manual directory specification needed)
        changed_files = get_changed_files_since_last_run(project_root)
        print(f"   📂 Dynamically scanning all Python directories")

        if changed_files:
            print(f"   ✅ Found {len(changed_files)} changed files:")
            for file in changed_files:
                print(f"      • {file}")
            logger_changelog.info(
                f"Detected changed files since last run: {changed_files}"
            )
        else:
            print("   📝 No file changes detected")
            logger_changelog.info("No file changes detected since last run.")
            # Check if this is a new project that needs initialization
            changelog_file = project_root / "CHANGELOG.md"
            json_file = project_root / "changelog.json"
            
            if not changelog_file.exists() or not json_file.exists():
                print("   🎉 Initializing new project...")
                logger_changelog.info("Initializing new project with welcome entry.")
                _create_initial_project_entry(json_manager, project_root)
                return
            else:
                print("   ✅ Project up to date - no changes to track")
                # No changes in existing project
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
        print("   📊 Analyzing line changes...")
        line_changes = get_file_line_changes(project_root, changed_files)
        aggregate_stats = get_aggregate_line_stats(line_changes)
        total_lines_added = aggregate_stats["total_lines_added"]
        total_lines_removed = aggregate_stats["total_lines_removed"]

        print(f"   📈 Line changes: +{total_lines_added} added, -{total_lines_removed} removed")

        logger_changelog.info(
            f"Line changes analysis: +{total_lines_added} -{total_lines_removed} "
            f"across {len(changed_files)} files"
        )

    except Exception as e:
        print("   ⚠️  Could not analyze line changes")
        logger_changelog.error(
            f"Error analyzing line changes: {e}",
            exc_info=True)

    # Get AI summary using RequestManager
    try:
        print("   🤖 Generating AI analysis...")
        from ..services.request_manager import RequestManager

        request_manager = RequestManager()
        gemini_client = request_manager.get_client("GeminiClient")
    except ValueError:
        print("   ⚠️  AI client not available")
        logger_changelog.warning("GeminiClient not found in RequestManager.")
        gemini_client = None

    summary = "Genel güncelleme."
    impact_level = ImpactLevel.MEDIUM
    change_type = ChangeType.OTHER

    if gemini_client and gemini_client.is_ready():
        try:
            prompt = f"Değişen dosyalar: {', '.join(changed_files)}"
            ai_summary = gemini_client.generate_summary(
                text_prompt=prompt, changed_files=changed_files
            )
            summary = ai_summary
            print("   ✨ AI analysis completed successfully")
            print(f"   📝 Summary: {summary[:100]}{'...' if len(summary) > 100 else ''}")
            logger_changelog.info(f"AI tarafından oluşturulan özet: {summary}")

            # Auto-detect impact level based on summary and files
            impact_level = _detect_impact_level(ai_summary, changed_files)
            print(f"   🎯 Impact level: {impact_level.value}")

        except Exception as e:
            print("   ⚠️  AI analysis failed, using fallback")
            logger_changelog.error(
                f"GeminiClient'tan özet alınırken hata oluştu: {e}",
                exc_info=True)
            summary = "AI özeti alınamadı. Değişiklikler uygulandı."
    else:
        print("   ⚠️  AI client unavailable, using default summary")
        logger_changelog.warning(
            "GeminiClient kullanılamıyor. Varsayılan özet kullanılıyor."
        )

    # Add entry to JSON changelog
    print("   💾 Saving changelog entry...")
    entry_id = json_manager.add_entry(
        ai_summary=summary,
        changed_files=changed_files,
        impact_level=impact_level,
        change_type=change_type,
        lines_added=total_lines_added,
        lines_removed=total_lines_removed,
    )

    print(f"   ✅ Changelog entry created (ID: {entry_id[:8]}...)")
    logger_changelog.info(f"Changelog entry added with ID: {entry_id}")

    # Create backups for next run comparison
    try:
        print("   🔄 Creating backup files for future comparison...")
        create_file_backups(project_root, "src" if (project_root / "src").exists() else ".")
        print("   ✅ Backup files created")
        logger_changelog.debug("File backups created for future line analysis")
    except Exception as e:
        print("   ⚠️  Could not create backup files")
        logger_changelog.error(
            f"Error creating file backups: {e}",
            exc_info=True)

    # Update README.md automatically with AI enhancement
    try:
        print("   📝 Updating README.md with current project state...")
        
        # Get AI client for README enhancement
        ai_client = None
        try:
            from ..services.request_manager import RequestManager
            request_manager = RequestManager()
            ai_client = request_manager.get_client("GeminiClient")
        except:
            pass  # Continue without AI enhancement
            
        readme_updated = update_readme(project_root, ai_client)
        if readme_updated:
            print("   ✅ README.md automatically updated")
        else:
            print("   ⚠️  README.md update skipped")
            
    except Exception as e:
        print(f"   ⚠️  Could not update README.md: {e}")
        logger_changelog.error(f"Error updating README.md: {e}", exc_info=True)

    # Professional Version Management
    try:
        print("   🏷️  Analyzing changes for version management...")
        version_manager = VersionManager(project_root)
        
        # Auto-increment version based on change impact
        current_version = version_manager.get_current_version()
        
        # Determine increment type based on impact level and change analysis
        increment_type = "patch"  # Default
        if impact_level == ImpactLevel.CRITICAL:
            increment_type = "major"
        elif impact_level == ImpactLevel.HIGH:
            increment_type = "minor" 
        elif impact_level == ImpactLevel.MEDIUM:
            increment_type = "minor"
        else:
            increment_type = "patch"
            
        # Auto-increment based on changes for better version management
        new_version, old_version, _ = version_manager.auto_increment_based_on_branch()
        
        if new_version != old_version and version_manager.update_version_in_files(new_version):
            print(f"   📈 Version updated: {current_version} → {new_version}")
            print(f"   🎯 Change Impact: {impact_level.value} ({increment_type} increment)")
            
            # Get version codename
            major, minor, _ = version_manager.parse_version(new_version)
            codename = version_manager._get_version_codename(major, minor, new_version, gemini_client)
            if codename:
                print(f"   💫 Codename: {codename}")
                
            # Create git tag for new version
            try:
                version_manager.create_git_tag(new_version, codename=codename)
                print(f"   🏷️  Git tag created: v{new_version}")
            except Exception as tag_error:
                print(f"   ⚠️  Could not create git tag: {tag_error}")
                
            # Commit changes to git
            git_manager = GitManager(project_root)
            if not git_manager.is_working_directory_clean():
                if _ask_user("   ❔ Summarizer updated project files. Commit these maintenance changes?"):
                    commit_message = f"chore(summarizer): Update project to v{new_version}"
                    if not (git_manager.stage_all() and git_manager.commit(commit_message)):
                        print("   ❌ Failed to commit maintenance changes. Aborting next git actions.")
                        return

            # Handle GitFlow and CI checks
            branch_name = git_manager.get_current_branch()
            target_branch = None
            if branch_name.startswith(('feature/', 'bugfix/')): target_branch = 'develop'
            elif branch_name == 'develop': target_branch = 'staging'
            elif branch_name.startswith('release/'): target_branch = 'main'
            elif branch_name.startswith('hotfix/'): target_branch = 'main'
            
            if branch_name == 'staging':
                _handle_release_creation(project_root, git_manager, new_version)
            elif target_branch:
                _handle_pull_request_flow(project_root, git_manager, branch_name, target_branch, summary, gemini_client)
            elif branch_name.startswith(('release/', 'hotfix/')):
                match = re.match(r"^(release|hotfix)\/v(\d+\.\d+\.\d+)", branch_name)
                if match and match.group(2) != new_version:
                    new_branch_name = f"{match.group(1)}/v{new_version}"
                    if _ask_user(f"   ❔ On old branch. Create and switch to '{new_branch_name}'?"):
                        if git_manager.create_branch(new_branch_name):
                            _write_next_command(project_root, f"git checkout {new_branch_name}")

    except Exception as e:
        print(f"   ⚠️  Version management failed: {e}")
        logger_changelog.error(f"Error in version management: {e}", exc_info=True)


def _create_initial_project_entry(json_manager, project_root: Path):
    """Create professional initial project entry for new projects"""
    
    # Create hidden project structure
    summarizer_dir = project_root / ".summarizer"
    summarizer_dir.mkdir(exist_ok=True)
    
    # Detect project type
    project_type = _detect_project_type(project_root)
    project_name = project_root.name
    
    # Professional welcome message based on project type
    if project_type == "python":
        welcome_summary = f"""🚀 **{project_name} Projesi Başlatıldı**

**Proje Türü**: Python Projesi  
**Başlatılma Tarihi**: {datetime.now().strftime('%d %B %Y')}  
**Summarizer Framework**: v2.0.0

**📋 Proje Özeti:**
Bu proje, Summarizer Framework ile otomatik değişiklik takibi ve AI destekli analiz için yapılandırıldı. Artık kod değişiklikleriniz otomatik olarak tespit edilecek ve akıllı özetler oluşturulacak.

**🔧 Aktif Özellikler:**
- ✅ Otomatik dosya değişiklik takibi
- ✅ AI destekli kod analizi (Gemini AI)
- ✅ JSON ve Markdown changelog oluşturma
- ✅ Etki seviyesi ve değişiklik tipi otomatik tespiti
- ✅ Satır bazında değişiklik analizi

**📁 Oluşturulan Dosyalar:**
- `CHANGELOG.md` - İnsan okunabilir değişiklik günlüğü
- `changelog.json` - Yapılandırılmış değişiklik verisi
- `.summarizer/` - Gizli sistem dosyaları

**🎯 Sonraki Adımlar:**
1. Python dosyalarınızda değişiklik yapın
2. `summarizer` komutunu tekrar çalıştırın
3. Otomatik oluşturulan değişiklik analizini inceleyin

**💡 İpucu:** `summarizer --help` komutuyla tüm özellikleri keşfedin!"""

    elif project_type == "web":
        welcome_summary = f"""🌐 **{project_name} Web Projesi Başlatıldı**

**Proje Türü**: Web Geliştirme Projesi  
**Başlatılma Tarihi**: {datetime.now().strftime('%d %B %Y')}  
**Summarizer Framework**: v2.0.0

**📋 Proje Özeti:**
Web geliştirme projeniz Summarizer Framework ile entegre edildi. Frontend ve backend değişiklikleriniz otomatik olarak takip edilecek ve profesyonel değişiklik raporları oluşturulacak.

**🔧 Desteklenen Dosya Türleri:**
- ✅ JavaScript/TypeScript dosyaları (.js, .ts, .jsx, .tsx)
- ✅ HTML/CSS dosyaları (.html, .css, .scss)
- ✅ Python backend dosyaları (.py)
- ✅ Konfigürasyon dosyaları (package.json, requirements.txt)

**📁 Proje Yapısı Hazırlandı:**
- `CHANGELOG.md` - Geliştirme günlüğü
- `changelog.json` - API entegrasyonu için JSON verisi
- `.summarizer/` - Gizli sistem dosyaları

**🚀 Web Projesi Özellikleri:**
- Frontend/Backend değişiklik ayrımı
- Component bazında analiz
- Dependencies değişiklik takibi
- Performance impact analizi

Bu projede değişiklik yaptığınızda, otomatik olarak akıllı analizler oluşturulacak!"""

    else:
        welcome_summary = f"""📁 **{project_name} Projesi Başlatıldı**

**Proje Türü**: Genel Yazılım Projesi  
**Başlatılma Tarihi**: {datetime.now().strftime('%d %B %Y')}  
**Summarizer Framework**: v2.0.0

**📋 Hoş Geldiniz!**
Projeniz başarıyla Summarizer Framework ile entegre edildi. Artık tüm kod değişiklikleriniz otomatik olarak takip edilecek ve yapay zeka destekli analizler oluşturulacak.

**🔧 Sistem Özellikleri:**
- ✅ Dosya değişiklik takibi (.py, .js, .ts, .html, .css ve daha fazlası)
- ✅ Gemini AI ile kod analizi
- ✅ Otomatik impact level tespiti (Low/Medium/High/Critical)
- ✅ Değişiklik tipi kategorilendirmesi (Feature/Bug Fix/Refactor/Config)
- ✅ Markdown ve JSON format desteği

**📊 Tracking Bilgileri:**
- **Toplam Dosya**: 0 (henüz değişiklik yok)
- **Son Güncelleme**: {datetime.now().strftime('%H:%M:%S')}
- **Durum**: Aktif ve hazır ✅

**🎯 İlk Kullanım:**
1. Herhangi bir dosyada değişiklik yapın
2. `summarizer` komutunu tekrar çalıştırın  
3. Otomatik oluşturulan analizi görüntüleyin

**💡 Komutlar:**
- `summarizer --gui` - Görsel arayüz
- `summarizer --status` - Sistem durumu
- `summarizer screenshot` - Ekran analizi

Projenizde her değişiklik yaptığınızda, akıllı özetler otomatik oluşturulacak!"""

    # Add the initial entry
    print("   🎉 Creating welcome entry for new project...")
    entry_id = json_manager.add_entry(
        ai_summary=welcome_summary,
        changed_files=[],
        impact_level=ImpactLevel.LOW,
        change_type=ChangeType.CONFIG,
        lines_added=0,
        lines_removed=0,
    )
    
    print("   📁 Project structure initialized:")
    print("      • CHANGELOG.md - Human readable changelog")  
    print("      • changelog.json - Structured data format")
    print("      • .summarizer/ - Internal tracking files")
    
    # Create initial README.md for new project
    try:
        print("      • README.md - Auto-generated project documentation")
        
        # Get AI client for enhanced README
        ai_client = None
        try:
            from ..services.request_manager import RequestManager
            request_manager = RequestManager()
            ai_client = request_manager.get_client("GeminiClient")
        except:
            pass  # Continue without AI enhancement
            
        readme_created = update_readme(project_root, ai_client)
        if readme_created:
            print("   📝 Professional README.md created")
        else:
            print("   ⚠️  README.md creation skipped")
            
    except Exception as e:
        print(f"   ⚠️  Could not create README.md: {e}")
        logger_changelog.warning(f"Error creating initial README.md: {e}")
    
    logger_changelog.info(f"Initial project entry created: {entry_id}")
    print(f"   ✅ Project initialized successfully!")


def _detect_project_type(project_root: Path) -> str:
    """Detect project type based on files in directory"""
    
    # Check for web project indicators
    web_files = ["package.json", "index.html", "main.js", "app.js", "webpack.config.js"]
    if any((project_root / f).exists() for f in web_files):
        return "web"
    
    # Check for Python project indicators
    python_files = ["requirements.txt", "setup.py", "pyproject.toml", "main.py"]
    py_files = list(project_root.glob("*.py"))
    if any((project_root / f).exists() for f in python_files) or len(py_files) > 0:
        return "python"
    
    # Default to general project
    return "general"


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
