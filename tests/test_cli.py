from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from directional import cli


def test_info_reports_unavailable_native_extension(capsys):
    assert cli.main(["info"]) == 0

    captured = capsys.readouterr()
    assert "directional" in captured.out
    assert "native extension: unavailable" in captured.out


def test_load_input_rejects_non_npz(tmp_path):
    input_path = tmp_path / "mesh.txt"
    input_path.write_text("not an npz")

    try:
        cli._load_input(input_path)
    except ValueError as exc:
        assert "Input must be a .npz file" in str(exc)
    else:
        raise AssertionError("_load_input should reject non-.npz files")


def test_require_array_reports_missing_key():
    try:
        cli._require_array({}, "vertices")
    except ValueError as exc:
        assert "vertices" in str(exc)
    else:
        raise AssertionError("_require_array should reject missing keys")


def test_remesh_raw_cross_field_writes_npz(monkeypatch, tmp_path):
    class FakeOptions:
        lengthRatio = None
        integralSeamless = None
        roundSeams = None
        # featureAlign = None
        verbose = None
        normalizeDirections = None

    class FakeResult:
        success = True
        vertices = np.array([[0.0, 0.0, 0.0]])
        faces = np.array([[0, 0, 0]])
        degrees = np.array([4])

    calls = []

    def fake_raw(vertices, faces, raw_cross_field, options):
        calls.append((vertices, faces, raw_cross_field, options))
        return FakeResult()

    def fake_cross(*_args):
        raise AssertionError("raw_cross_field input should use remesh_from_raw_cross_field")

    monkeypatch.setattr(
        cli,
        "_load_native_api",
        lambda: (FakeOptions, fake_cross, fake_raw),
    )

    input_path = tmp_path / "input.npz"
    output_path = tmp_path / "output.npz"
    np.savez_compressed(
        input_path,
        vertices=np.zeros((1, 3)),
        faces=np.zeros((1, 3), dtype=np.int32),
        raw_cross_field=np.zeros((1, 12)),
    )

    assert cli.main(["remesh", str(input_path), str(output_path), "--length-ratio", "0.1"]) == 0
    assert len(calls) == 1
    assert calls[0][3].lengthRatio == 0.1

    with np.load(output_path) as output:
        assert bool(output["success"])
        np.testing.assert_array_equal(output["vertices"], FakeResult.vertices)
        np.testing.assert_array_equal(output["faces"], FakeResult.faces)
        np.testing.assert_array_equal(output["degrees"], FakeResult.degrees)
