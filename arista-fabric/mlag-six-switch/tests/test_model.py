import sys
from pathlib import Path
import copy
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"python"))
from model import load, validate, peer_info
from render import render,render_node
from drift import compare

def test_valid_topology():
    data=load()
    assert validate(data)
    assert len(data["devices"])==6
    assert len(data["pairs"])==3

def test_peer_addresses():
    data=load()
    assert peer_info(data,"MGT-05")==("10.255.255.4/31","10.255.255.5")
    assert peer_info(data,"MGT-06")==("10.255.255.5/31","10.255.255.4")

def test_prevent_port_collision():
    data=copy.deepcopy(load())
    data["devices"]["MGT-05"]["bundles"][0]["ports"].append("Ethernet49")
    try:
        validate(data)
        assert False, "must reject duplicate peer-link member"
    except ValueError as ex:
        assert "duplicate physical port" in str(ex)

def test_render_all_nodes(tmp_path):
    data=load()
    output=render(data,tmp_path)
    assert len(list(tmp_path.rglob("*.cfg")))==24
    assert "mlag configuration" in (tmp_path/"mlag/MGT-05.cfg").read_text()
    assert "ip virtual-router address 10.4.26.1" in (tmp_path/"gateway/MGT-05.cfg").read_text()
    assert "ip virtual-router address" not in (tmp_path/"gateway/MGT-01.cfg").read_text()
    assert "mlag 52" in (tmp_path/"bundles/MGT-06.cfg").read_text()

def test_render_deterministic(tmp_path):
    data=load()
    a=render_node(data,"MGT-01")
    b=render_node(data,"MGT-01")
    assert a==b

def test_drift_detection():
    assert not compare("hostname X\n","hostname X\n")
    assert compare("hostname X\n","hostname Y\n")
