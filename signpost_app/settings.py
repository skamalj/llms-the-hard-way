"""Settings, read from environment variables with defaults. Also picks the AWS profile when none is set."""
import os
import re
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
SIGNPOST_PATH = Path(os.environ.get("SIGNPOST_PATH", APP_DIR.parent / "models" / "signpost"))
AGENT_MODEL = os.environ.get("AGENT_MODEL", "claude-opus-5-5")
AGENT_EFFORT = os.environ.get("AGENT_EFFORT", "low")              # short chat replies; raise for harder agents
TABLE_NAME = os.environ.get("CHECKPOINT_TABLE", "signpost-checkpoints")
TTL_SECONDS = int(os.environ.get("CHECKPOINT_TTL", "86400"))       # checkpoints expire after a day
MAX_MESSAGES = int(os.environ.get("REDUCER_MAX_MESSAGES", "12"))   # the reducer prunes when a thread holds more than this ...
MIN_MESSAGES = int(os.environ.get("REDUCER_MIN_MESSAGES", "6"))    # ... down to this many (whole messages, oldest first)


def use_aws_profile():
    """If AWS_PROFILE is not set, use the first profile in ~/.aws/config (here: the single SSO profile).
    -> the profile name (not printed by callers; it contains the account id)."""
    if os.environ.get("AWS_PROFILE"):
        return os.environ["AWS_PROFILE"]
    cfg = Path.home() / ".aws" / "config"
    if cfg.exists():
        m = re.search(r"^\[profile (.+?)\]", cfg.read_text(), re.M)
        if m:
            os.environ["AWS_PROFILE"] = m.group(1)
            return m.group(1)
    return None
