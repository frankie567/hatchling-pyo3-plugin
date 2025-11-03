from hatchling_pyo3_plugin.hooks import PyO3BuildHook


def test_plugin_name():
    assert PyO3BuildHook.PLUGIN_NAME == "pyo3"
