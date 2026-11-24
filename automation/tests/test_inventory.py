from pathlib import Path
import sys
import tempfile
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))
from netops.common import load_inventory

def test_inventory_load():
    root = Path(__file__).resolve().parents[1]
    inventory = load_inventory(root / "data/devices.example.yml")
    assert len(inventory) >= 2

def test_duplicate_device_rejected():
    with tempfile.TemporaryDirectory() as directory:
        file = Path(directory) / "inventory.yml"
        file.write_text("""devices:
  - {name: x, platform: cisco_ios, host: 192.0.2.1, credential_env: A}
  - {name: x, platform: cisco_ios, host: 192.0.2.2, credential_env: B}
""")
        with pytest.raises(ValueError, match="Duplicate"):
            load_inventory(file)

