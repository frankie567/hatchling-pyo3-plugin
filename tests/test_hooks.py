import os
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
        # This should not raise ValueError with the fixed glob patterns
        hook._add_rust_artifacts(build_data)

        # Verify that artifacts were found and added
        assert "force_include" in build_data
        # On Linux, it should find libtest.so
        # On macOS, it should find libfoo.dylib
        # On Windows, it should find libbar.dll
        if platform.system() == "Linux":
            assert any(
                "test.so" in path for path in build_data["force_include"].values()
            )
        elif platform.system() == "Darwin":
            assert any(
                "foo.so" in path for path in build_data["force_include"].values()
            )
        elif platform.system() == "Windows":
            assert any(
                "bar.pyd" in path for path in build_data["force_include"].values()
            )


def test_get_profile_from_environment():
    """Test that profile can be set via environment variable."""
    with tempfile.TemporaryDirectory() as tmpdir:
        mock_metadata = Mock()
        mock_metadata.core.name = "test-package"

        # Test with environment variable
        os.environ["HATCH_BUILD_HOOK_PYO3_PROFILE"] = "debug"
        try:
            hook = PyO3BuildHook(
                root=tmpdir,
                config={},
                build_config=Mock(),
                metadata=mock_metadata,
                directory=tmpdir,
                target_name="wheel",
                app=MagicMock(),
            )
            assert hook._get_profile() == "debug"
        finally:
            del os.environ["HATCH_BUILD_HOOK_PYO3_PROFILE"]

        # Test with config
        hook = PyO3BuildHook(
            root=tmpdir,
            config={"profile": "release"},
            build_config=Mock(),
            metadata=mock_metadata,
            directory=tmpdir,
            target_name="wheel",
            app=MagicMock(),
        )
        assert hook._get_profile() == "release"

        # Test default
        hook = PyO3BuildHook(
            root=tmpdir,
            config={},
            build_config=Mock(),
            metadata=mock_metadata,
            directory=tmpdir,
            target_name="wheel",
            app=MagicMock(),
        )
        assert hook._get_profile() == "release"


def test_copy_to_source():
    """Test that artifacts are copied to source directory when enabled."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create target/release directory
        target_dir = Path(tmpdir) / "target" / "release"
        target_dir.mkdir(parents=True)

        # Create package directory
        package_dir = Path(tmpdir) / "test_package"
        package_dir.mkdir(parents=True)

        # Create test library file
        lib_ext = ".so"
        if platform.system() == "Windows":
            lib_suffix = ".dll"
        elif platform.system() == "Darwin":
            lib_suffix = ".dylib"
        else:
            lib_suffix = ".so"

        lib_file = target_dir / f"libtest{lib_suffix}"
        lib_file.touch()

        # Create a mock build hook
        mock_metadata = Mock()
        mock_metadata.core.name = "test-package"

        hook = PyO3BuildHook(
            root=tmpdir,
            config={"copy-to-source": True},
            build_config=Mock(),
            metadata=mock_metadata,
            directory=tmpdir,
            target_name="wheel",
            app=MagicMock(),
        )

        # Call _add_rust_artifacts
        build_data = {}
        hook._add_rust_artifacts(build_data)

        # Verify that file was copied to source
        expected_file = package_dir / f"test{lib_ext}"
        assert expected_file.exists(), f"Expected file {expected_file} to exist"


def test_copy_to_source_disabled():
    """Test that artifacts are not copied when copy-to-source is disabled."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create target/release directory
        target_dir = Path(tmpdir) / "target" / "release"
        target_dir.mkdir(parents=True)

        # Create package directory
        package_dir = Path(tmpdir) / "test_package"
        package_dir.mkdir(parents=True)

        # Create test library file
        lib_ext = ".so"
        if platform.system() == "Windows":
            lib_suffix = ".dll"
        elif platform.system() == "Darwin":
            lib_suffix = ".dylib"
        else:
            lib_suffix = ".so"

        lib_file = target_dir / f"libtest{lib_suffix}"
        lib_file.touch()

        # Create a mock build hook
        mock_metadata = Mock()
        mock_metadata.core.name = "test-package"

        hook = PyO3BuildHook(
            root=tmpdir,
            config={"copy-to-source": False},
            build_config=Mock(),
            metadata=mock_metadata,
            directory=tmpdir,
            target_name="wheel",
            app=MagicMock(),
        )

        # Call _add_rust_artifacts
        build_data = {}
        hook._add_rust_artifacts(build_data)

        # Verify that file was NOT copied to source
        expected_file = package_dir / f"test{lib_ext}"
        assert not expected_file.exists(), f"Expected file {expected_file} to not exist"
