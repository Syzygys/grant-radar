"""Grant Radar 基础测试（离线可跑）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import main  # noqa: E402


def test_collect_returns_list():
    rows = main.collect()
    assert isinstance(rows, list)


def test_row_shape_when_present():
    for r in main.collect():
        assert {"platform", "name", "reward", "url"} <= set(r)


def test_print_table_no_crash(capsys):
    main.print_table([])
    main.print_table([{"platform": "X", "name": "demo", "reward": "100 USDC", "url": "http://x"}])
    out = capsys.readouterr().out
    assert "demo" in out


if __name__ == "__main__":
    test_collect_returns_list()
    test_row_shape_when_present()
    print("OK")
