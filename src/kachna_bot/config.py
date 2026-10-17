"""Load the local, untracked configuration from the project root."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

_config_path = Path.cwd() / "config.py"
_spec = spec_from_file_location("kachna_bot_local_config", _config_path)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"Could not load application configuration from {_config_path}")

_module = module_from_spec(_spec)
_spec.loader.exec_module(_module)
Config = _module.Config
