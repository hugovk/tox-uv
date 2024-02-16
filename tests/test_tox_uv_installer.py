from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest
    from tox.pytest import ToxProjectCreator


def test_uv_install_in_ci_list(tox_project: ToxProjectCreator, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CI", "1")
    project = tox_project({"tox.ini": "[testenv]\ndeps = tomli\npackage=skip"})
    result = project.run()
    result.assert_success()
    assert "tomli==" in result.out


def test_uv_install_with_pre(tox_project: ToxProjectCreator) -> None:
    project = tox_project({"tox.ini": "[testenv]\ndeps = tomli\npip_pre = true\npackage=skip"})
    result = project.run("-vv")
    result.assert_success()


def test_uv_install_with_pre_custom_install_cmd(tox_project: ToxProjectCreator) -> None:
    project = tox_project({
        "tox.ini": """
    [testenv]
    deps = tomli
    pip_pre = true
    package = skip
    install_command = uv pip install {packages}
    """
    })
    result = project.run("-vv")
    result.assert_success()


def test_uv_install_without_pre_custom_install_cmd(tox_project: ToxProjectCreator) -> None:
    project = tox_project({
        "tox.ini": """
    [testenv]
    deps = tomli
    package = skip
    install_command = uv pip install {packages}
    """
    })
    result = project.run("-vv")
    result.assert_success()