"""
Quick Command Executor - Example Integration
Shows how to use the macOS command library in your agent.
"""

from macos_commands import MacOSCommands

def execute_quick_command(command_text):
    """
    Execute a quick command using the predefined library.
    
    Args:
        command_text: Natural language command (e.g., "take screenshot")
    
    Returns:
        dict: Execution result
    """
    # Normalize command
    command_lower = command_text.lower().strip()
    
    # Try to execute from library
    result = MacOSCommands.execute_shortcut(command_lower)
    
    if result:
        return result
    
    # Try searching for partial matches
    matches = MacOSCommands.search_command(command_lower)
    
    if matches:
        # Execute first match
        first_match = list(matches.keys())[0]
        print(f"Found similar command: {first_match}")
        return MacOSCommands.execute_shortcut(first_match)
    
    return {"success": False, "error": "Command not found in library"}


# Example usage:
if __name__ == "__main__":
    import sys
    
    # Test commands
    test_commands = [
        "take screenshot",
        "open calculator",
        "new tab",
        "lock screen",
        "show desktop",
        "turn off wifi",
    ]
    
    print("🧪 Testing macOS Command Library\n")
    print("=" * 50)
    
    for cmd in test_commands:
        print(f"\n📝 Command: '{cmd}'")
        result = execute_quick_command(cmd)
        
        if result and result.get("success"):
            print(f"✅ Success: {result.get('type')} - {result}")
        else:
            print(f"❌ Failed: {result}")
    
    print("\n" + "=" * 50)
    print("\n💡 To list all commands:")
    print("   from macos_commands import MacOSCommands")
    print("   all_cmds = MacOSCommands.get_all_commands()")
    print(f"   Total commands available: {len(MacOSCommands.get_all_commands())}")
