"""Loader for agent manifests and execution bootstrap.
Reads YAML in ../manifests/*.yaml and constructs in-memory agent specs.
"""
import os
import glob
import yaml
import json
from pathlib import Path
from typing import Dict, Any
from jsonschema import validate

MANIFEST_DIR = Path(__file__).resolve().parents[1] / "manifests"
SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"
SESSION_LOG = Path(__file__).resolve().parents[1] / "SESSION_LOG.md"

SUMMARY_SCHEMA_PATH = SCHEMA_DIR / "summary.schema.json"

class AgentSpec(Dict[str, Any]):
    pass

def load_env():
    # simplistic env loader; expects pre-exported variables or .env
    env_file = Path(__file__).resolve().parents[2] / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

def load_manifests() -> Dict[str, AgentSpec]:
    specs: Dict[str, AgentSpec] = {}
    for path in glob.glob(str(MANIFEST_DIR / "*.yaml")):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            agent_id = data.get("id") or Path(path).stem
            specs[agent_id] = AgentSpec(data)
    return specs

def ensure_session_log():
    if SESSION_LOG.exists():
        return
    SESSION_LOG.write_text("## Session: INIT\n", encoding="utf-8")

def append_session_line(line: str):
    with SESSION_LOG.open("a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")

def load_summary_schema() -> Dict[str, Any]:
    if SUMMARY_SCHEMA_PATH.exists():
        return json.loads(SUMMARY_SCHEMA_PATH.read_text())
    return {}

def validate_instance(instance: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    try:
        validate(instance, schema)
        return True
    except Exception:
        return False

def bootstrap():
    load_env()
    specs = load_manifests()
    ensure_session_log()
    append_session_line(f"[INIT] loaded_manifests={list(specs.keys())}")
    summary_schema = load_summary_schema()
    # dummy validation example
    test_instance = {"summary": "ok", "items": [{"id": "1", "text": "x"}], "sources": []}
    valid = validate_instance(test_instance, summary_schema)
    append_session_line(f"[SCHEMA_CHECK] summary_schema_valid={valid}")
    return {"specs": specs, "schema_valid": valid}

if __name__ == "__main__":
    state = bootstrap()
    print("Bootstrap complete", state)
