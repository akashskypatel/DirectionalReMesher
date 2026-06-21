from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_native_cli_cmake_target_is_optional():
    cmake = (ROOT / "CMakeLists.txt").read_text()

    assert 'option(DIRECTIONAL_BUILD_CLI "Build the optional native command line executable" OFF)' in cmake
    assert "if(DIRECTIONAL_BUILD_CLI)" in cmake
    assert "add_executable(directional_cli src/directional_cli.cpp)" in cmake
    assert "OUTPUT_NAME directional" in cmake


def test_native_cli_source_exposes_info_command():
    source = (ROOT / "src" / "directional_cli.cpp").read_text()

    assert "directional_build_info" in source
    assert 'command == "info"' in source
    assert "unknown command" in source
