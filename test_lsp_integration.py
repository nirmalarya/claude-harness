#!/usr/bin/env python3
"""
Test LSP Integration

Verifies that LSP configurations are generated correctly.
"""

import json
import shutil
import tempfile
from pathlib import Path
from lsp_config import LSPConfigGenerator


def test_language_detection():
    """Test that languages are detected from project files."""
    print("Testing Language Detection")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        lsp_gen = LSPConfigGenerator(project_dir)

        # Create TypeScript project
        (project_dir / "package.json").write_text("{}")
        (project_dir / "tsconfig.json").write_text("{}")

        detected = lsp_gen.detect_languages()
        print(f"\n✓ TypeScript project detected: {detected}")
        assert "typescript" in detected

        # Add Python files
        (project_dir / "requirements.txt").write_text("requests")

        detected = lsp_gen.detect_languages()
        print(f"✓ TypeScript + Python detected: {detected}")
        assert "typescript" in detected and "python" in detected

        # Add Go files
        (project_dir / "go.mod").write_text("module test")

        detected = lsp_gen.detect_languages()
        print(f"✓ TypeScript + Python + Go detected: {detected}")
        assert all(lang in detected for lang in ["typescript", "python", "go"])


def test_lsp_config_generation():
    """Test that LSP configurations are generated correctly."""
    print("\n\nTesting LSP Config Generation")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        lsp_gen = LSPConfigGenerator(project_dir)

        # Generate config for TypeScript and Python
        config = lsp_gen.generate_lsp_config(["typescript", "python"])

        print(f"\n✓ Generated config:")
        print(json.dumps(config, indent=2))

        # Verify structure
        assert "lspServers" in config
        assert "typescript" in config["lspServers"]
        assert "python" in config["lspServers"]

        # Verify TypeScript config
        ts_config = config["lspServers"]["typescript"]
        assert ts_config["command"] == "typescript-language-server"
        assert ".ts" in ts_config["extensionToLanguage"]
        assert ".tsx" in ts_config["extensionToLanguage"]

        # Verify Python config
        py_config = config["lspServers"]["python"]
        assert py_config["command"] == "pylsp"
        assert ".py" in py_config["extensionToLanguage"]

        print("\n✓ Config structure validated")


def test_lsp_config_file_creation():
    """Test that plugin.json file is created correctly."""
    print("\n\nTesting LSP Config File Creation")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        lsp_gen = LSPConfigGenerator(project_dir)

        # Write config file
        config_file = lsp_gen.write_lsp_config(["typescript"])

        print(f"\n✓ Config file created: {config_file}")

        # Verify file exists
        assert config_file.exists()
        assert config_file.name == "plugin.json"

        # Verify directory structure
        assert config_file.parent == project_dir / ".claude" / "plugins" / "lsp"

        # Verify file contents
        with open(config_file) as f:
            config = json.load(f)

        assert "lspServers" in config
        assert "typescript" in config["lspServers"]

        print("✓ File structure validated")
        print(f"✓ Content valid: {json.dumps(config, indent=2)}")


def test_installation_check():
    """Test that installation status is checked correctly."""
    print("\n\nTesting Installation Check")
    print("=" * 60)

    lsp_gen = LSPConfigGenerator(Path("/tmp"))

    # Check for node (likely installed)
    node_installed = shutil.which("node") is not None
    print(f"\n✓ Node installed: {node_installed}")

    # Check for TypeScript language server
    ts_installed = lsp_gen.check_lsp_server_installed("typescript")
    print(f"✓ typescript-language-server installed: {ts_installed}")

    # Check for Python language server
    py_installed = lsp_gen.check_lsp_server_installed("python")
    print(f"✓ pylsp installed: {py_installed}")

    # Get installation instructions
    instructions = lsp_gen.get_installation_instructions(["typescript", "python"])
    print(f"\n✓ Installation instructions:")
    print(instructions)


def test_full_setup():
    """Test complete LSP setup workflow."""
    print("\n\nTesting Complete LSP Setup")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)

        # Create a TypeScript project
        (project_dir / "package.json").write_text('{"name": "test-project"}')
        (project_dir / "tsconfig.json").write_text("{}")

        lsp_gen = LSPConfigGenerator(project_dir)
        setup_result = lsp_gen.setup_lsp()

        print(f"\n✓ Setup complete:")
        print(f"  Config file: {setup_result['config_file']}")
        print(f"  Languages: {setup_result['languages']}")
        print(f"  Enable command: {setup_result['enable_command']}")
        print(f"\n{setup_result['installation_instructions']}")

        # Verify config file was created
        config_file = Path(setup_result['config_file'])
        assert config_file.exists()

        # Verify TypeScript was detected
        assert "typescript" in setup_result['languages']


if __name__ == "__main__":
    print("Claude-Harness LSP Integration Test")
    print("=" * 60)

    try:
        test_language_detection()
        test_lsp_config_generation()
        test_lsp_config_file_creation()
        test_installation_check()
        test_full_setup()

        print("\n\n" + "=" * 60)
        print("✓ All LSP integration tests passed!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
