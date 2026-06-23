from __future__ import annotations

import contextlib
import os
from collections.abc import Iterator

from setuptools import build_meta as _build_meta


_BUILD_SETTING_MAPPINGS = {
    "DIRECTIONAL_ENABLE_GMP": ("use-gmp", "directional.use-gmp"),
    "DIRECTIONAL_ENABLE_SUITESPARSE": (
        "enable-suitesparse",
        "directional.enable-suitesparse",
    ),
    "DIRECTIONAL_ENABLE_PARDISO": (
        "enable-pardiso",
        "directional.enable-pardiso",
    ),
    "DIRECTIONAL_ENABLE_CUDSS": (
        "enable-cudss",
        "directional.enable-cudss",
    ),
    "DIRECTIONAL_BUILD_CLI": ("build-cli", "directional.build-cli"),
}


def _get_setting(
    config_settings: dict[str, object] | None, *keys: str
) -> object | None:
    if not config_settings:
        return None
    return next((config_settings[key] for key in keys if key in config_settings), None)


def _normalize_bool(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        if not value:
            return None
        value = value[-1]
    text = str(value).strip().lower()
    if text in {"1", "on", "true", "yes"}:
        return "1"
    if text in {"0", "off", "false", "no"}:
        return "0"
    raise ValueError(f"Invalid boolean build setting: {value!r}")


@contextlib.contextmanager
def _apply_directional_settings(
    config_settings: dict[str, object] | None,
) -> Iterator[None]:
    mappings = {
        environment_name: _normalize_bool(
            _get_setting(config_settings, *setting_names)
        )
        for environment_name, setting_names in _BUILD_SETTING_MAPPINGS.items()
    }
    previous = {key: os.environ.get(key) for key in mappings}
    try:
        for key, value in mappings.items():
            if value is not None:
                os.environ[key] = value
        yield
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _with_settings(function, *args, config_settings=None, **kwargs):
    with _apply_directional_settings(config_settings):
        return function(*args, config_settings=config_settings, **kwargs)


def get_requires_for_build_wheel(config_settings=None):
    return _with_settings(
        _build_meta.get_requires_for_build_wheel,
        config_settings=config_settings,
    )


def get_requires_for_build_sdist(config_settings=None):
    return _with_settings(
        _build_meta.get_requires_for_build_sdist,
        config_settings=config_settings,
    )


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    return _with_settings(
        _build_meta.prepare_metadata_for_build_wheel,
        metadata_directory,
        config_settings=config_settings,
    )


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    return _with_settings(
        _build_meta.build_wheel,
        wheel_directory,
        metadata_directory=metadata_directory,
        config_settings=config_settings,
    )


def build_sdist(sdist_directory, config_settings=None):
    return _with_settings(
        _build_meta.build_sdist,
        sdist_directory,
        config_settings=config_settings,
    )
