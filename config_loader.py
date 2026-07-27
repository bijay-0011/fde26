import os
import re
import yaml
import logging
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Load .env
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)

# Matches:
# ${VAR}
# ${VAR:default}
ENV_PATTERN = re.compile(r"\$\{([^}:]+)(?::([^}]*))?\}")

def _replace_env(value):
    """Replace ${VAR} or ${VAR:default} inside a string."""

    if not isinstance(value, str):
        return value

    def repl(match):
        var = match.group(1)
        default = match.group(2) or ""
        return os.getenv(var, default)

    return ENV_PATTERN.sub(repl, value)


def _walk(obj):
    """Recursively replace env vars in dict/list/string."""

    if isinstance(obj, dict):
        return {k: _walk(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [_walk(v) for v in obj]

    if isinstance(obj, str):
        return _replace_env(obj)

    return obj


def load_config(config_file="config.yaml"):
    search_paths = [
        Path("/app") / config_file,
        BASE_DIR / config_file,
        Path(config_file),
    ]

    for path in search_paths:
        if path.exists():
            logger.info(f"Loaded configuration from: {path}")

            with open(path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

            return _walk(config)

    raise FileNotFoundError(f"Could not find {config_file}")


CONFIG = load_config()