"""
Simplified Professional Configuration GUI
Dynamic configuration interface with modern design
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import flet as ft

from ..core.configuration_manager import ConfigurationManager


class SimplifiedConfigGUI:
    """Simplified professional configuration GUI"""

    def __init__(self, project_root: Optional[Path] = None):
        # Use project_root if provided, otherwise default to cwd for config
        config_dir = (
            project_root / ".summarizer" if project_root else Path.cwd() / ".summarizer"
        )
        # Ensure the config directory exists
        config_dir.mkdir(parents=True, exist_ok=True)

        self.config_manager = ConfigurationManager(config_dir=config_dir)
        self.page: Optional[ft.Page] = None
        self.field_controls: Dict[str, ft.Control] = {}
        self.status_text: Optional[ft.Text] = None

    def create_field_control(self, field_config: Dict[str, Any]) -> ft.Control:
        """Create control for configuration field - Enterprise flat design"""
        field_type = field_config.get("type", "text")
        key = field_config["key"]
        current_value = self.config_manager.get_field_value(key) or field_config.get(
            "default", ""
        )

        # Enterprise flat boyutlar - minimal ve temiz
        control_width = 300

        # Enterprise flat renk şeması - daha minimal
        border_color = "#ddd"
        focus_color = "#0078d4"  # Microsoft mavi
        text_color = "#323130"
        label_color = "#605e5c"

        if field_type == "password":
            control = ft.TextField(
                label=field_config["label"],
                hint_text=field_config.get("placeholder", ""),
                password=True,
                can_reveal_password=True,
                value=current_value,
                width=control_width,
                border_radius=0,  # Tamamen flat
                border_color=border_color,
                focused_border_color=focus_color,
                color=text_color,
                label_style=ft.TextStyle(color=label_color, size=12),
                content_padding=ft.padding.symmetric(horizontal=8, vertical=12),
            )

        elif field_type == "select":
            options = []
            for option in field_config.get("options", []):
                options.append(
                    ft.dropdown.Option(key=option["value"], text=option["label"])
                )

            control = ft.Dropdown(
                label=field_config["label"],
                value=current_value,
                options=options,
                width=control_width,
                border_radius=0,  # Tamamen flat
                border_color=border_color,
                focused_border_color=focus_color,
                color=text_color,
                label_style=ft.TextStyle(color=label_color, size=12),
                content_padding=ft.padding.symmetric(horizontal=8, vertical=12),
            )

        elif field_type == "number":
            control = ft.TextField(
                label=field_config["label"],
                hint_text=field_config.get("placeholder", ""),
                value=current_value,
                width=control_width,
                border_radius=0,  # Tamamen flat
                border_color=border_color,
                focused_border_color=focus_color,
                color=text_color,
                label_style=ft.TextStyle(color=label_color, size=12),
                keyboard_type=ft.KeyboardType.NUMBER,
                content_padding=ft.padding.symmetric(horizontal=8, vertical=12),
            )

        elif field_type == "boolean":
            control = ft.Container(
                content=ft.Row(
                    [
                        ft.Switch(
                            value=(
                                current_value.lower() == "true"
                                if current_value
                                else False
                            ),
                            tooltip=field_config.get("description", ""),
                            scale=0.9,
                            active_color=focus_color,
                        ),
                        ft.Text(
                            field_config["label"],
                            size=13,
                            color=label_color,
                            weight=ft.FontWeight.W_400,
                        ),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START,
                ),
                width=control_width,
                padding=ft.padding.symmetric(horizontal=8, vertical=12),
                border=ft.border.all(1, border_color),
                border_radius=0,  # Tamamen flat
            )

        else:  # text
            control = ft.TextField(
                label=field_config["label"],
                hint_text=field_config.get("placeholder", ""),
                value=current_value,
                width=control_width,
                border_radius=0,  # Tamamen flat
                border_color=border_color,
                focused_border_color=focus_color,
                color=text_color,
                label_style=ft.TextStyle(color=label_color, size=12),
                content_padding=ft.padding.symmetric(horizontal=8, vertical=12),
            )

        self.field_controls[key] = control
        return control

    def on_profile_change(self, e):
        """Handle profile selection change"""
        profile_name = e.control.value
        if profile_name and self.config_manager.apply_profile(profile_name):
            self.refresh_field_values()
            self.show_status(f"✅ Applied profile: {profile_name}", "#27ae60")

    def refresh_field_values(self):
        """Refresh all field values from configuration manager"""
        for key, control in self.field_controls.items():
            value = self.config_manager.get_field_value(key)
            if value:
                if hasattr(control, "content") and isinstance(control.content, ft.Row):
                    # Boolean switch içinde
                    switch_control = control.content.controls[0]
                    if isinstance(switch_control, ft.Switch):
                        switch_control.value = value.lower() == "true"
                elif isinstance(control, ft.Switch):
                    control.value = value.lower() == "true"
                else:
                    control.value = value
        self.page.update()

    def create_group_section(self, group: Dict[str, Any]) -> ft.Container:
        """Create section for configuration group - Enterprise flat design"""
        fields = []

        # 3 sütunlu enterprise layout için fields'i üçlü gruplar halinde grupla
        group_fields = group.get("fields", [])

        # Alanları 3'er 3'er yerleştir (enterprise grid)
        for i in range(0, len(group_fields), 3):
            row_fields = []

            # İlk alan
            field_control = self.create_field_control(group_fields[i])
            row_fields.append(ft.Container(field_control, expand=1))

            # İkinci alan varsa ekle
            if i + 1 < len(group_fields):
                field_control_2 = self.create_field_control(group_fields[i + 1])
                row_fields.append(ft.Container(field_control_2, expand=1))
            else:
                row_fields.append(ft.Container(expand=1))  # Boş alan

            # Üçüncü alan varsa ekle
            if i + 2 < len(group_fields):
                field_control_3 = self.create_field_control(group_fields[i + 2])
                row_fields.append(ft.Container(field_control_3, expand=1))
            else:
                row_fields.append(ft.Container(expand=1))  # Boş alan

            # Enterprise row oluştur
            fields.append(
                ft.Row(
                    row_fields,
                    spacing=30,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=True,
                )
            )

        # Enterprise flat section header
        header_section = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.SETTINGS, size=20, color="#2c3e50"),
                    ft.Text(
                        group["title"],
                        size=18,
                        weight=ft.FontWeight.W_600,
                        color="#2c3e50",
                    ),
                    ft.Container(expand=1),  # Spacer
                    ft.Text(
                        group["description"], size=11, color="#7f8c8d", italic=True
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.symmetric(horizontal=0, vertical=8),
            bgcolor="#f8f9fa",
            border=ft.border.only(left=ft.BorderSide(4, "#3498db")),
        )

        return ft.Container(
            content=ft.Column(
                # Minimal spacing
                [header_section, ft.Container(height=8), *fields],
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=0, vertical=12),
            margin=ft.margin.only(bottom=8),
            bgcolor="transparent",
        )

    def save_configuration(self, e):
        """Save current configuration"""
        try:
            # Collect values from all controls
            for key, control in self.field_controls.items():
                if hasattr(control, "content") and isinstance(control.content, ft.Row):
                    # Boolean switch içinde
                    switch_control = control.content.controls[0]
                    if isinstance(switch_control, ft.Switch):
                        value = str(switch_control.value).lower()
                    else:
                        value = control.value or ""
                elif isinstance(control, ft.Switch):
                    value = str(control.value).lower()
                else:
                    value = control.value or ""

                if value:  # Only save non-empty values
                    self.config_manager.set_field_value(key, value)

            # Save configuration
            self.config_manager.save_configuration()
            self.show_status("✅ Configuration saved successfully!", "#27ae60")

        except Exception as ex:
            self.show_status(f"❌ Error saving configuration: {str(ex)}", "#e74c3c")

    def save_and_run(self, e):
        """Save configuration and run main application"""
        # First save
        self.save_configuration(None)

        # Check if save was successful
        if self.status_text and "✅" in self.status_text.value:
            try:
                self.show_status("🚀 Starting main application...", "#3498db")

                # Start main application
                subprocess.Popen([sys.executable, "-m", "src.main"], cwd=Path.cwd())

                # Close GUI after a short delay
                import time

                time.sleep(1)
                self.page.window.close()

            except Exception as ex:
                self.show_status(f"❌ Error starting application: {str(ex)}", "#e74c3c")

    def show_status(self, message: str, color: str):
        """Show status message"""
        if self.status_text:
            self.status_text.value = message
            self.status_text.color = color
            self.page.update()

    def main(self, page: ft.Page):
        """Main GUI entry point - Enterprise flat design"""
        self.page = page

        # Enterprise page setup - ultra flat minimal
        page.title = "⚙️ Enterprise Configuration Manager"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window.width = 1400  # Daha geniş enterprise layout
        page.window.height = 800
        page.window.resizable = True
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        page.scroll = ft.ScrollMode.AUTO
        page.bgcolor = "#fafbfc"  # Ultra minimal background

        # Import existing .env if available
        self.config_manager.import_from_env()

        # Enterprise flat header - minimal ve profesyonel
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.SETTINGS, size=28, color="#2c3e50"),
                    ft.Column(
                        [
                            ft.Text(
                                "Enterprise Configuration Manager",
                                size=22,
                                weight=ft.FontWeight.W_600,
                                color="#2c3e50",
                            ),
                            ft.Text(
                                "Professional configuration management system",
                                size=12,
                                color="#7f8c8d",
                            ),
                        ],
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                    ft.Container(expand=1),  # Spacer
                    ft.Container(
                        content=ft.Text(
                            "v2.0", size=10, color="#95a5a6", weight=ft.FontWeight.W_400
                        ),
                        padding=ft.padding.symmetric(horizontal=6, vertical=2),
                        bgcolor="#ecf0f1",
                        border_radius=0,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.symmetric(horizontal=24, vertical=16),
            bgcolor="#ffffff",
            border=ft.border.only(bottom=ft.BorderSide(1, "#e1e8ed")),
        )

        # Enterprise Quick Profile Selector - flat design
        profiles = self.config_manager.get_profiles()
        profile_section = ft.Container()

        if profiles:
            profile_options = []
            for profile_key, profile_data in profiles.items():
                profile_options.append(
                    ft.dropdown.Option(
                        key=profile_key,
                        text=f"{profile_data['name']} - {profile_data['description']}",
                    )
                )

            profile_dropdown = ft.Dropdown(
                label="⚡ Quick Setup Profile",
                options=profile_options,
                width=400,
                border_radius=0,
                border_color="#e1e8ed",
                focused_border_color="#3498db",
                on_change=self.on_profile_change,
                content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
            )

            profile_section = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.SPEED, size=20, color="#9b59b6"),
                        ft.Text(
                            "Quick Setup",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color="#2c3e50",
                        ),
                        ft.Container(width=30),  # Spacer
                        profile_dropdown,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.padding.symmetric(horizontal=32, vertical=16),
                bgcolor="#ffffff",
                border=ft.border.only(bottom=ft.BorderSide(1, "#e1e8ed")),
            )

        # Create configuration groups - enterprise layout
        group_sections = []
        for group in self.config_manager.get_configuration_groups():
            group_section = self.create_group_section(group)
            group_sections.append(group_section)

        # Main content area
        content_area = ft.Container(
            content=ft.Column(group_sections, spacing=20),
            padding=ft.padding.symmetric(horizontal=32, vertical=24),
            bgcolor="#ffffff",
            expand=True,
        )

        # Enterprise status bar
        self.status_text = ft.Text(
            "Ready for configuration...", size=12, color="#7f8c8d"
        )

        status_bar = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color="#7f8c8d"),
                    self.status_text,
                    ft.Container(expand=1),
                    ft.Text(
                        f"Last updated: {datetime.now().strftime('%H:%M')}",
                        size=11,
                        color="#95a5a6",
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.symmetric(horizontal=32, vertical=12),
            bgcolor="#f8f9fa",
            border=ft.border.only(top=ft.BorderSide(1, "#e1e8ed")),
        )

        # Enterprise action toolbar - flat design
        action_toolbar = ft.Container(
            content=ft.Row(
                [
                    ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.SAVE, size=16, color="white"),
                                ft.Text(
                                    "Save Configuration",
                                    size=13,
                                    color="white",
                                    weight=ft.FontWeight.W_500,
                                ),
                            ],
                            spacing=6,
                        ),
                        on_click=self.save_configuration,
                        bgcolor="#27ae60",
                        color="white",
                        width=180,
                        height=42,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=0),
                            elevation={"": 0, "hovered": 1},
                        ),
                    ),
                    ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.PLAY_ARROW, size=16, color="white"),
                                ft.Text(
                                    "Save & Run",
                                    size=13,
                                    color="white",
                                    weight=ft.FontWeight.W_500,
                                ),
                            ],
                            spacing=6,
                        ),
                        on_click=self.save_and_run,
                        bgcolor="#3498db",
                        color="white",
                        width=160,
                        height=42,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=0),
                            elevation={"": 0, "hovered": 1},
                        ),
                    ),
                    ft.Container(width=16),  # Spacer
                    ft.OutlinedButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.CLOSE, size=16, color="#e74c3c"),
                                ft.Text(
                                    "Cancel",
                                    size=13,
                                    color="#e74c3c",
                                    weight=ft.FontWeight.W_500,
                                ),
                            ],
                            spacing=6,
                        ),
                        on_click=lambda e: page.window.close(),
                        width=120,
                        height=42,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=0),
                            side=ft.BorderSide(1, "#e74c3c"),
                        ),
                    ),
                ],
                spacing=12,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=32, vertical=20),
            bgcolor="#ffffff",
            border=ft.border.only(top=ft.BorderSide(1, "#e1e8ed")),
        )

        # Enterprise main layout - tam ekran kullanımı ve minimal spacing
        main_layout = ft.Column(
            [header, profile_section, content_area, action_toolbar, status_bar],
            spacing=0,
            expand=True,
        )

        # Add to page - full screen
        page.add(main_layout)


def run_configuration_gui(project_root_str: Optional[str] = None):
    """Run the configuration GUI"""
    project_root = Path(project_root_str) if project_root_str else Path.cwd()
    gui = SimplifiedConfigGUI(project_root=project_root)
    ft.app(target=gui.main)


# For compatibility
def main_gui_entry():
    # This function will be called by the summarizer CLI
    # It needs to accept the project_root argument from the CLI
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project_root",
        type=str,
        help="The root directory of the project.",
        default=None,
    )
    args = parser.parse_args()

    # If project_root is not passed, it defaults to None, and SimplifiedConfigGUI will use Path.cwd()
    run_configuration_gui(args.project_root)


if __name__ == "__main__":
    # When run directly, try to get project_root from argv or default to cwd
    # This allows testing the GUI with a specific project context if needed
    # e.g. python -m src.gui.modern_config_gui --project_root /path/to/your/project
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project_root",
        type=str,
        help="The root directory of the project.",
        default=None,
    )
    args = parser.parse_args()

    run_configuration_gui(args.project_root)
