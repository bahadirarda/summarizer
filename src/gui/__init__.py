# Modern GUI Module
from .modern_config_gui import SimplifiedConfigGUI, run_configuration_gui

__all__ = ["SimplifiedConfigGUI", "run_configuration_gui"]

# Alias for backward compatibility
main = run_configuration_gui
