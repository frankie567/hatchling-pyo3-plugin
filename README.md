# Hatchling PyO3 Plugin

<p align="center">
    <em>A Hatchling build hook plugin for building PyO3 Rust extensions</em>
</p>

[![build](https://github.com/frankie567/hatchling-pyo3-plugin/workflows/Build/badge.svg)](https://github.com/frankie567/hatchling-pyo3-plugin/actions)
[![codecov](https://codecov.io/gh/frankie567/hatchling-pyo3-plugin/branch/master/graph/badge.svg)](https://codecov.io/gh/frankie567/hatchling-pyo3-plugin)
[![PyPI version](https://badge.fury.io/py/hatchling-pyo3-plugin.svg)](https://badge.fury.io/py/hatchling-pyo3-plugin)

---

**Documentation**: <a href="https://frankie567.github.io/hatchling-pyo3-plugin/" target="_blank">https://frankie567.github.io/hatchling-pyo3-plugin/</a>

**Source Code**: <a href="https://github.com/frankie567/hatchling-pyo3-plugin" target="_blank">https://github.com/frankie567/hatchling-pyo3-plugin</a>

---

## Overview

PyO3 is a popular framework for creating Python bindings to Rust code. While [Maturin](https://github.com/PyO3/maturin) is the recommended build backend for PyO3 projects, this plugin enables PyO3 extensions to be built using Hatchling as an alternative build backend.

This is inspired by [setuptools-rust](https://github.com/PyO3/setuptools-rust), which provides similar functionality for setuptools.

## Features

- ✅ Build PyO3 Rust extensions as part of the Hatchling build process
- ✅ Automatic detection of Cargo.toml
- ✅ Cross-platform support (Linux, macOS, Windows)
- ✅ Configurable build profiles (release/debug)
- ✅ Custom Cargo arguments support
- ✅ Integration with standard Python packaging workflow

## Usage

### Installation

Add the plugin to your `pyproject.toml`:

```toml
[build-system]
requires = ["hatchling", "hatchling-pyo3-plugin"]
build-backend = "hatchling.build"

[tool.hatch.build.hooks.pyo3]
# Plugin will automatically detect and build Rust extensions
```

### Project Structure

```
my-project/
├── pyproject.toml
├── Cargo.toml          # Rust project configuration
├── src/
│   └── lib.rs          # Rust source code with PyO3 bindings
└── my_package/
    └── __init__.py     # Python package
```

### Example pyproject.toml

```toml
[build-system]
requires = ["hatchling", "hatchling-pyo3-plugin"]
build-backend = "hatchling.build"

[project]
name = "my-pyo3-project"
version = "0.1.0"
description = "A project with PyO3 extensions"
requires-python = ">=3.8"

[tool.hatch.build.hooks.pyo3]
# Optional: specify Rust extensions explicitly
# If not specified, plugin will look for Cargo.toml in project root

# Optional configuration:
# cargo-manifest = "Cargo.toml"  # Path to Cargo.toml (default: "Cargo.toml")
# profile = "release"            # Build profile (default: "release", can be "debug")
# target-dir = "target"          # Cargo target directory (default: "target")
# cargo-args = ["--features", "special"]  # Additional cargo arguments
```

## Development

### Setup environment

We use [uv](https://docs.astral.sh/uv/) to manage the development environment and production build, and [just](https://github.com/casey/just) to manage command shortcuts. Ensure they are installed on your system.

### Run unit tests

You can run all the tests with:

```bash
just test
```

### Format the code

Execute the following command to apply linting and check typing:

```bash
just lint
```

### Publish a new version

You can bump the version, create a commit and associated tag with one command:

```bash
just version patch
```

```bash
just version minor
```

```bash
just version major
```

Your default Git text editor will open so you can add information about the release.

When you push the tag on GitHub, the workflow will automatically publish it on PyPi and a GitHub release will be created as draft.

## Serve the documentation

You can serve the Mkdocs documentation with:

```bash
just docs-serve
```

It'll automatically watch for changes in your code.

## License

This project is licensed under the terms of the MIT license.
