"""
Output Formatter for Better Readability
========================================

Formats agent tool use output to be more human-readable.
"""

def format_tool_output(tool_name: str, tool_input: dict, result: str = None) -> str:
    """Format tool usage in a readable way."""
    
    separator = "━" * 70
    
    # Map tool names to readable labels
    tool_labels = {
        "TodoWrite": "📝 Task Update",
        "Edit": "✏️  File Edit",
        "Write": "📄 New File",
        "Read": "📖 Reading File",
        "Bash": "⚡ Running Command",
        "mcp__puppeteer__puppeteer_navigate": "🌐 Browser Navigation",
        "mcp__puppeteer__puppeteer_click": "🖱️  Browser Click",
        "mcp__puppeteer__puppeteer_screenshot": "📸 Screenshot",
        "Grep": "🔍 Searching Code",
        "Glob": "📂 Finding Files",
    }
    
    label = tool_labels.get(tool_name, f"🔧 {tool_name}")
    
    output = f"\n{separator}\n"
    output += f"{label}\n"
    output += f"{separator}\n\n"
    
    # Format based on tool type
    if tool_name == "TodoWrite":
        todos = tool_input.get('todos', [])
        for todo in todos:
            status = todo.get('status', 'pending')
            content = todo.get('content', 'Unknown')
            
            emoji = {
                'completed': '✅',
                'in_progress': '🔄',
                'pending': '⏳',
                'cancelled': '❌'
            }.get(status, '📌')
            
            output += f"{emoji} {status.upper()}: {content}\n"
    
    elif tool_name == "Edit":
        file_path = tool_input.get('file_path', 'Unknown file')
        output += f"📁 File: {file_path}\n\n"
        
        old = tool_input.get('old_string', '')[:100]
        new = tool_input.get('new_string', '')[:100]
        
        if old and new:
            output += f"🔧 Change:\n"
            output += f"   FROM: {old}...\n"
            output += f"   TO:   {new}...\n"
    
    elif tool_name == "Write":
        file_path = tool_input.get('file_path', 'Unknown file')
        content_len = len(tool_input.get('contents', ''))
        output += f"📁 File: {file_path}\n"
        output += f"📏 Size: {content_len} characters\n"
    
    elif tool_name == "Read":
        file_path = tool_input.get('target_file', 'Unknown file')
        output += f"📁 File: {file_path}\n"
    
    elif tool_name == "Bash":
        command = tool_input.get('command', '')
        desc = tool_input.get('description', '')
        
        if desc:
            output += f"📋 Purpose: {desc}\n\n"
        
        # Show first line of command
        first_line = command.split('\n')[0]
        if len(first_line) > 80:
            first_line = first_line[:77] + "..."
        output += f"💻 Command: {first_line}\n"
        
        if '\n' in command:
            output += f"   (multiline command)\n"
    
    elif "puppeteer" in tool_name:
        if "navigate" in tool_name:
            url = tool_input.get('url', '')
            output += f"🌐 URL: {url}\n"
        elif "click" in tool_name:
            selector = tool_input.get('selector', tool_input.get('element', ''))
            output += f"🎯 Target: {selector}\n"
        elif "screenshot" in tool_name:
            name = tool_input.get('name', 'screenshot')
            output += f"📸 Name: {name}\n"
    
    # Show result if available
    if result:
        if result == "Done":
            output += f"\n✅ SUCCESS\n"
        elif "Error" in result:
            output += f"\n❌ ERROR: {result}\n"
    
    output += f"\n{separator}\n"
    
    return output


# Example usage in progress display
def print_session_progress(session_num: int, total_features: int, passing_features: int):
    """Print formatted session progress."""
    
    percentage = (passing_features / total_features * 100) if total_features > 0 else 0
    
    separator = "━" * 70
    
    print(f"\n{separator}")
    print(f"📊 Session {session_num} Progress")
    print(f"{separator}\n")
    print(f"Features: {passing_features}/{total_features} passing ({percentage:.1f}%)")
    print(f"Remaining: {total_features - passing_features} features\n")
    print(f"{separator}\n")

