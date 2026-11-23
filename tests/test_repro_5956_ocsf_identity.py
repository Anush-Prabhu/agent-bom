"""Regression check for agent-bom#5956: OCSF ingest drops actor, session, cloud and device.

Fails at 43be104 (fields dropped); passes at a96d79a (#6001).
"""

from agent_bom.api.observability_events import _normalize_ocsf_event

EVENT = {
    "class_name": "API Activity",
    "class_uid": 6003,
    "severity_id": 1,
    "time": "2026-10-25T12:00:00.000Z",
    "metadata": {"uid": "meta-1", "product": {"name": "test-product"}},
    "actor": {"user": {"name": "alice"}, "session": {"uid": "sess-123"}},
    "cloud": {"account": {"uid": "acct-9"}, "region": "us-east-1"},
    "device": {"hostname": "dev-host-1"},
    "observables": [{"trace_id": "trace-abc"}],
}


def test_ocsf_identity_context_is_retained():
    out = _normalize_ocsf_event(EVENT, tenant_id="tenant-demo")
    assert out.get("actor", {}).get("session") == {"uid": "sess-123"}
    assert out.get("cloud") == {"account": {"uid": "acct-9"}, "region": "us-east-1"}
    assert out.get("device") == {"hostname": "dev-host-1"}
    assert out["session_id"]
    assert out["trace_id"] == "trace-abc"


def test_session_id_is_stable_across_retries():
    first = _normalize_ocsf_event(EVENT, tenant_id="tenant-demo")["session_id"]
    assert first and first == _normalize_ocsf_event(EVENT, tenant_id="tenant-demo")["session_id"]
