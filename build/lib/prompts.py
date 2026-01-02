"""
Prompt Loading Utilities
========================

Functions for loading prompt templates from the prompts directory.
"""

import os
import shutil
from pathlib import Path
from setup_mcp import MCPServerSetup


PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(name: str, mode: str = "greenfield") -> str:
    """
    Load a prompt template from the prompts directory.

    Args:
        name: Prompt filename (without .md extension)
        mode: Execution mode (for MCP tool injection)

    Returns:
        Prompt text with MCP tool documentation injected
    """
    prompt_path = PROMPTS_DIR / f"{name}.md"
    prompt = prompt_path.read_text()

    # Inject MCP tool documentation
    return inject_mcp_tools(prompt, mode)


def inject_mcp_tools(prompt: str, mode: str) -> str:
    """
    Inject MCP tool documentation into prompt templates.

    Replaces placeholders like {{DOCUMENTATION_MCP_TOOLS}} with actual tool names.
    """
    mcp_setup = MCPServerSetup()

    # Documentation tools
    doc_server = mcp_setup.get_documentation_server_name()
    if doc_server == "context7":
        doc_tools = """- context7_resolve_library_id(library_name: str) - Get library ID for documentation lookup
- context7_get_library_docs(library_id: str, topic: str) - Query latest framework documentation"""
    elif doc_server == "ref":
        doc_tools = """- ref_search(query: str) - Search documentation across frameworks
- ref_get_docs(path: str) - Get specific documentation page"""
    else:
        doc_tools = "⚠️ No documentation MCP configured"

    prompt = prompt.replace("{{DOCUMENTATION_MCP_TOOLS}}", doc_tools)

    # Browser automation tools
    browser_tools = """- puppeteer_navigate(url: str) - Navigate to a URL
- puppeteer_screenshot(path: str) - Take a screenshot (save to .claude/verification/)
- puppeteer_click(selector: str) - Click an element
- puppeteer_fill(selector: str, value: str) - Fill an input field
- puppeteer_select(selector: str, value: str) - Select from dropdown
- puppeteer_hover(selector: str) - Hover over an element
- puppeteer_evaluate(expression: str) - Execute JavaScript in browser"""

    prompt = prompt.replace("{{BROWSER_MCP_TOOLS}}", browser_tools)

    # Azure DevOps tools (backlog mode only)
    if mode == "backlog":
        ado_tools = """- azure_devops_get_work_items(project: str) - Fetch PBIs from backlog
- azure_devops_update_work_item(id: int, state: str) - Update PBI state
- azure_devops_add_work_item_comment(id: int, comment: str) - Add comment to PBI"""
        prompt = prompt.replace("{{AZURE_DEVOPS_MCP_TOOLS}}", ado_tools)

    return prompt


def get_initializer_prompt(mode: str = "greenfield") -> str:
    """Load the initializer prompt based on mode."""
    if mode == "enhancement":
        return load_prompt("enhancement_initializer_prompt", mode)
    elif mode == "bugfix":
        return load_prompt("enhancement_initializer_prompt", mode)  # Same as enhancement
    else:
        return load_prompt("initializer_prompt", mode)


def get_coding_prompt(mode: str = "greenfield") -> str:
    """Load the coding agent prompt based on mode."""
    if mode == "enhancement":
        return load_prompt("enhancement_coding_prompt", mode)
    elif mode == "bugfix":
        return load_prompt("bugfix_mode_prompt", mode)
    else:
        return load_prompt("coding_prompt", mode)


def copy_spec_to_project(project_dir: Path, spec_file: str = None, mode: str = "greenfield") -> None:
    """Copy the spec file and helper tools into the project directory."""
    # Create spec/ directory in project
    spec_dir = project_dir / "spec"
    spec_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy spec file to project/spec/
    if spec_file:
        spec_source = Path(spec_file)
        # Determine target name based on mode
        if mode in ["enhancement", "bugfix"]:
            spec_name = "enhancement_spec.txt"
        else:
            spec_name = "app_spec.txt"
    else:
        # Use default example spec
        spec_source = Path(__file__).parent / "specs" / "simple_example_spec.txt"
        spec_name = "app_spec.txt"
    
    spec_dest = spec_dir / spec_name
    
    if not spec_dest.exists() or mode in ["enhancement", "bugfix"]:
        shutil.copy(spec_source, spec_dest)
        print(f"Copied {spec_source.name} to project directory as {spec_name}")
    
    # Copy helper tools to project from harness root
    harness_root = Path(__file__).parent
    tools_to_copy = ["regression_tester.py"]
    
    for tool in tools_to_copy:
        tool_source = harness_root / tool
        tool_dest = project_dir / tool
        if tool_source.exists() and not tool_dest.exists():
            shutil.copy(tool_source, tool_dest)
            print(f"Copied {tool} to project directory")
