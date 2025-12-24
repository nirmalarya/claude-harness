"""
Prompt Loading Utilities
========================

Functions for loading prompt templates from the prompts directory.
"""

import shutil
from pathlib import Path


PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(name: str) -> str:
    """Load a prompt template from the prompts directory."""
    prompt_path = PROMPTS_DIR / f"{name}.md"
    return prompt_path.read_text()


def get_initializer_prompt(mode: str = "greenfield") -> str:
    """Load the initializer prompt based on mode."""
    if mode == "enhancement":
        return load_prompt("enhancement_initializer_prompt")
    elif mode == "bugfix":
        return load_prompt("enhancement_initializer_prompt")  # Same as enhancement
    else:
        return load_prompt("initializer_prompt")


def get_coding_prompt(mode: str = "greenfield") -> str:
    """Load the coding agent prompt based on mode."""
    if mode == "enhancement":
        return load_prompt("enhancement_coding_prompt")
    elif mode == "bugfix":
        return load_prompt("bugfix_mode_prompt")
    else:
        return load_prompt("coding_prompt")


def copy_spec_to_project(project_dir: Path, spec_file: str = None, mode: str = "greenfield") -> None:
    """Copy the spec file into the project directory for the agent to read."""
    if spec_file:
        # Custom spec file provided
        spec_source = Path(spec_file)
        spec_name = "enhancement_spec.txt" if mode in ["enhancement", "bugfix"] else "app_spec.txt"
    else:
        # Use default spec from prompts
        spec_source = PROMPTS_DIR / "app_spec.txt"
        spec_name = "app_spec.txt"
    
    spec_dest = project_dir / spec_name
    
    if not spec_dest.exists() or mode in ["enhancement", "bugfix"]:
        shutil.copy(spec_source, spec_dest)
        print(f"Copied {spec_source.name} to project directory as {spec_name}")
