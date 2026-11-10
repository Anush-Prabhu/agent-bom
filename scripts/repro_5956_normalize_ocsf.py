"""Reproduce agent-bom#5956: _normalize_ocsf_event drops actor/session/cloud/device.

Pinned to main at 43be104 (parent of this branch tip when the script was added).
Run from the repo root after `uv sync --extra dev`:

    .venv/Scripts/python.exe scripts/repro_5956_normalize_ocsf.py
"""

from __future__ import annotations

import json

from agent_bom.api.observability_events import _normalize_ocsf_event

# Exact payload used for the Unit 6 reproduction report.
EVENT = {
    "class_name": "API Activity",
    "class_uid": 6003,
    "severity_id": 1,
    "time": "2026-10-25T12:00:00.000Z",
    "metadata": {
        "uid": "meta-1",
        "product": {"name": "test-product"},
    },
    "actor": {
        "user": {"name": "alice"},
        "session": {"uid": "sess-123"},
    },
    "cloud": {
        "account": {"uid": "acct-9"},
        "region": "us-east-1",
    },
    "device": {
        "hostname": "dev-host-1",
    },
    "observables": [
        {"trace_id": "trace-abc"},
    ],
}

if __name__ == "__main__":
    out = _normalize_ocsf_event(EVENT, tenant_id="tenant-demo")
    print("agent_name=", repr(out.get("agent_name")))
    print("session_id=", repr(out.get("session_id")))
    print("trace_id=", repr(out.get("trace_id")))
    print("keys=", sorted(out.keys()))
    print("--- full normalized event ---")
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
