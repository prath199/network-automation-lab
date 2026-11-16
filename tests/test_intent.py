from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def test_five_ansible_operations():
    assert len(list((ROOT / "ansible/playbooks").glob("*.yml"))) >= 5

def test_containerlab_topology():
    assert (ROOT / "containerlab/topology.clab.yml").is_file()

def test_mcp_allowlist():
    source = (ROOT / "observability-mcp/server.py").read_text()
    assert "if check not in SHOW" in source
    assert "SHOW[check]" in source
