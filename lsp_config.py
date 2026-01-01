"""
LSP Configuration Generator for claude-harness v3.2
===================================================

Auto-generates .lsp.json configurations for Claude Code's native LSP support.

Detects project languages and configures appropriate language servers:
- TypeScript/JavaScript: typescript-language-server
- Python: python-lsp-server (pylsp)
- Go: gopls
- Rust: rust-analyzer
- Java: jdtls
- C/C++: clangd
- C#: omnisharp
- PHP: intelephense
- Kotlin: kotlin-language-server
- Ruby: solargraph
- HTML/CSS: vscode-html-languageserver, vscode-css-languageserver
"""

import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


class LSPConfigGenerator:
    """
    Generates Claude Code LSP configurations based on project languages.

    Claude Code v2.0.74+ has native LSP support via .lsp.json files.
    This generator auto-detects languages and creates proper configurations.
    """

    # LSP server configurations for supported languages
    LSP_SERVERS = {
        "typescript": {
            "command": "typescript-language-server",
            "args": ["--stdio"],
            "extensionToLanguage": {
                ".ts": "typescript",
                ".tsx": "typescriptreact",
                ".js": "javascript",
                ".jsx": "javascriptreact",
                ".mts": "typescript",
                ".cts": "typescript",
                ".mjs": "javascript",
                ".cjs": "javascript"
            },
            "install_check": "typescript-language-server",
            "install_cmd": "npm install -g typescript-language-server typescript"
        },
        "python": {
            "command": "pylsp",
            "args": [],
            "extensionToLanguage": {
                ".py": "python",
                ".pyi": "python"
            },
            "initializationOptions": {
                "settings": {
                    "pylsp": {
                        "plugins": {
                            "jedi_definition": {"enabled": True},
                            "jedi_references": {"enabled": True},
                            "jedi_hover": {"enabled": True},
                            "jedi_completion": {"enabled": True}
                        }
                    }
                }
            },
            "install_check": "pylsp",
            "install_cmd": "pip install 'python-lsp-server[all]'"
        },
        "go": {
            "command": "gopls",
            "args": [],
            "extensionToLanguage": {
                ".go": "go"
            },
            "install_check": "gopls",
            "install_cmd": "go install golang.org/x/tools/gopls@latest"
        },
        "rust": {
            "command": "rust-analyzer",
            "args": [],
            "extensionToLanguage": {
                ".rs": "rust"
            },
            "install_check": "rust-analyzer",
            "install_cmd": "rustup component add rust-analyzer"
        },
        "java": {
            "command": "jdtls",
            "args": [],
            "extensionToLanguage": {
                ".java": "java"
            },
            "install_check": "jdtls",
            "install_cmd": "# See https://github.com/eclipse/eclipse.jdt.ls"
        },
        "c_cpp": {
            "command": "clangd",
            "args": [],
            "extensionToLanguage": {
                ".c": "c",
                ".cpp": "cpp",
                ".cc": "cpp",
                ".cxx": "cpp",
                ".h": "c",
                ".hpp": "cpp",
                ".hxx": "cpp"
            },
            "install_check": "clangd",
            "install_cmd": "# Install LLVM/Clang from your package manager"
        },
        "csharp": {
            "command": "omnisharp",
            "args": ["--languageserver"],
            "extensionToLanguage": {
                ".cs": "csharp"
            },
            "install_check": "omnisharp",
            "install_cmd": "# See https://github.com/OmniSharp/omnisharp-roslyn"
        },
        "php": {
            "command": "intelephense",
            "args": ["--stdio"],
            "extensionToLanguage": {
                ".php": "php"
            },
            "install_check": "intelephense",
            "install_cmd": "npm install -g intelephense"
        }
    }

    def __init__(self, project_dir: Path):
        """
        Initialize LSP config generator.

        Args:
            project_dir: Project root directory
        """
        self.project_dir = project_dir
        self.plugin_dir = project_dir / ".claude" / "plugins" / "lsp"

    def detect_languages(self) -> List[str]:
        """
        Auto-detect languages used in project.

        Returns:
            List of detected language identifiers
        """
        detected = []

        # Check for common project files/patterns
        if (self.project_dir / "package.json").exists():
            detected.append("typescript")

        if (self.project_dir / "requirements.txt").exists() or \
           (self.project_dir / "pyproject.toml").exists() or \
           (self.project_dir / "setup.py").exists():
            detected.append("python")

        if (self.project_dir / "go.mod").exists():
            detected.append("go")

        if (self.project_dir / "Cargo.toml").exists():
            detected.append("rust")

        if (self.project_dir / "pom.xml").exists() or \
           (self.project_dir / "build.gradle").exists():
            detected.append("java")

        if (self.project_dir / "CMakeLists.txt").exists():
            detected.append("c_cpp")

        if list(self.project_dir.glob("*.csproj")):
            detected.append("csharp")

        if (self.project_dir / "composer.json").exists():
            detected.append("php")

        return detected

    def check_lsp_server_installed(self, language: str) -> bool:
        """
        Check if LSP server binary is installed.

        Args:
            language: Language identifier

        Returns:
            True if installed, False otherwise
        """
        config = self.LSP_SERVERS.get(language)
        if not config:
            return False

        check_cmd = config.get("install_check")
        return shutil.which(check_cmd) is not None

    def generate_lsp_config(self, languages: Optional[List[str]] = None) -> Dict:
        """
        Generate .lsp.json configuration.

        Args:
            languages: List of languages to configure (auto-detected if None)

        Returns:
            LSP configuration dictionary
        """
        if languages is None:
            languages = self.detect_languages()

        if not languages:
            return {"lspServers": {}}

        lsp_servers = {}

        for lang in languages:
            if lang in self.LSP_SERVERS:
                config = self.LSP_SERVERS[lang].copy()
                # Remove our custom fields
                config.pop("install_check", None)
                config.pop("install_cmd", None)
                lsp_servers[lang] = config

        return {
            "name": "claude-harness-lsp",
            "version": "1.0.0",
            "description": "Auto-generated LSP configuration for claude-harness project",
            "lspServers": lsp_servers
        }

    def write_lsp_config(self, languages: Optional[List[str]] = None) -> Path:
        """
        Write .lsp.json file to project.

        Args:
            languages: Languages to configure (auto-detected if None)

        Returns:
            Path to created .lsp.json file
        """
        # Create plugin directory
        self.plugin_dir.mkdir(parents=True, exist_ok=True)

        # Generate config
        config = self.generate_lsp_config(languages)

        # Write plugin.json (contains LSP config)
        plugin_file = self.plugin_dir / "plugin.json"
        with open(plugin_file, "w") as f:
            json.dump(config, f, indent=2)

        return plugin_file

    def get_installation_instructions(self, languages: Optional[List[str]] = None) -> str:
        """
        Get installation instructions for missing LSP servers.

        Args:
            languages: Languages to check (auto-detected if None)

        Returns:
            Formatted installation instructions
        """
        if languages is None:
            languages = self.detect_languages()

        missing = []

        for lang in languages:
            if not self.check_lsp_server_installed(lang):
                config = self.LSP_SERVERS.get(lang, {})
                missing.append({
                    "language": lang,
                    "server": config.get("install_check", "unknown"),
                    "command": config.get("install_cmd", "# No installation command available")
                })

        if not missing:
            return "✓ All LSP servers installed!"

        lines = ["LSP Server Installation Instructions:", ""]

        for item in missing:
            lines.append(f"❌ {item['language']} ({item['server']}):")
            lines.append(f"   {item['command']}")
            lines.append("")

        return "\n".join(lines)

    def setup_lsp(self, languages: Optional[List[str]] = None) -> Dict:
        """
        Complete LSP setup for project.

        Args:
            languages: Languages to configure (auto-detected if None)

        Returns:
            Setup summary with paths and instructions
        """
        if languages is None:
            languages = self.detect_languages()

        # Write LSP config
        config_file = self.write_lsp_config(languages)

        # Check installations
        instructions = self.get_installation_instructions(languages)

        return {
            "config_file": str(config_file),
            "languages": languages,
            "installation_instructions": instructions,
            "enable_command": "Set environment variable: ENABLE_LSP_TOOL=1"
        }
