import platform
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock

from hatchling_pyo3_plugin.hooks import PyO3BuildHook


def test_plugin_name():
    assert PyO3BuildHook.PLUGIN_NAME == "pyo3"


def test_add_rust_artifacts_glob_pattern():
    """Test that glob patterns work correctly without causing ValueError."""
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create target/release directory
        target_dir = Path(tmpdir) / "target" / "release"
        target_dir.mkdir(parents=True)

        # Create test library files
        (target_dir / "libtest.so").touch()
        (target_dir / "libfoo.dylib").touch()
        (target_dir / "libbar.dll").touch()

        # Create a mock build hook with all required parameters
        mock_metadata = Mock()
        mock_metadata.core.name = "test-package"

        hook = PyO3BuildHook(
            root=tmpdir,
            config={},
            build_config=Mock(),
            metadata=mock_metadata,
            directory=tmpdir,
            target_name="wheel",
            app=MagicMock(),
        )

        # Test that _add_rust_artifacts doesn't raise ValueError
        build_data = {}
        try:
            hook._add_rust_artifacts(build_data)
            # If we get here without exception, the glob patterns are working
            assert True
        except ValueError as e:
            if "Invalid pattern" in str(e):
                assert False, f"Glob pattern error: {e}"
            raise

        # Verify that artifacts were found and added
        # On Linux, it should find libtest.so
        # On macOS, it should find libfoo.dylib
        # On Windows, it should find libbar.dll
        if platform.system() == "Linux":
            assert "force_include" in build_data
            assert any(
                "test.so" in path for path in build_data["force_include"].values()
            )
        elif platform.system() == "Darwin":
            assert "force_include" in build_data
            assert any(
                "foo.so" in path for path in build_data["force_include"].values()
            )
        elif platform.system() == "Windows":
            assert "force_include" in build_data
            assert any(
                "bar.pyd" in path for path in build_data["force_include"].values()
            )
