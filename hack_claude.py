#!/usr/bin/env python3
"""
Claude 3.7 Hack Script with automated backups

This script enhances Claude 3.7 in Cursor by:
1. Increasing token limit to 200,000
2. Setting thinking level to "high"
3. Customizing Claude 3.7 UI styling

The script uses precise string matching to find the target functions:
- Token limit: Uses multiple search patterns for 'getEffectiveTokenLimit' with fallback to regex
- Thinking level: Searches for 'getModeThinkingLevel(e)'
- UI styling: Searches for '_serializableTitle:()=>"claude-3.7-sonnet"}'
"""

import os
import re
import sys
import shutil
import argparse
from datetime import datetime

def create_backup(file_path):
    """Create a backup of the target file."""
    backup_file = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(file_path, backup_file)
    print(f"Backup created at: {backup_file}")
    return backup_file

def modify_token_limit(content, mode="claude37_only"):
    """
    Modify the getEffectiveTokenLimit function to increase the token limit.
    
    Args:
        content: The file content
        mode: "claude37_only" or "all_models"
    
    Returns:
        Modified content
    """
    # Try multiple search patterns to find the function
    patterns = [
        'async getEffectiveTokenLimit(e)',  # Original exact match
        'async getEffectiveTokenLimit',     # More relaxed function name match
        'getEffectiveTokenLimit',           # Even more relaxed match
        'function getEffectiveTokenLimit'   # Alternative declaration style
    ]
    
    match_pos = -1
    for pattern in patterns:
        match_pos = content.find(pattern)
        if match_pos != -1:
            print(f"Found token limit function using pattern: {pattern}")
            break
    
    if match_pos == -1:
        # Try regex as a fallback for maximum flexibility
        import re
        rx_pattern = r'(?:async\s+)?(?:function\s+)?getEffectiveTokenLimit\s*\(\s*\w+\s*\)'
        match = re.search(rx_pattern, content)
        if match:
            match_pos = match.start()
            print(f"Found token limit function using regex fallback")
        else:
            print("WARNING: Could not find getEffectiveTokenLimit function.")
            return content
    
    # Find the opening brace after the pattern
    opening_brace_pos = content.find('{', match_pos)
    if opening_brace_pos == -1:
        print("WARNING: Could not find opening brace for getEffectiveTokenLimit function.")
        return content
    
    # Find the matching closing brace (considering nested braces)
    brace_count = 1
    pos = opening_brace_pos + 1
    while brace_count > 0 and pos < len(content):
        if content[pos] == '{':
            brace_count += 1
        elif content[pos] == '}':
            brace_count -= 1
        pos += 1
    
    if brace_count != 0:
        print("WARNING: Could not find matching closing brace for getEffectiveTokenLimit function.")
        return content
    
    # Extract the original function
    original_function = content[match_pos:pos]
    
    # Create the replacement based on mode
    if mode == "claude37_only":
        # Only apply to Claude 3.7 models
        replacement = '''async getEffectiveTokenLimit(e) {
  if(e.modelName && e.modelName.includes('claude-3.7')) return 200000;
  
  // Original function code below
  ''' + original_function[original_function.find('{')+1:]
    else:
        # Apply to all models
        replacement = '''async getEffectiveTokenLimit(e) {
  return 200000; // Always use 200K limit for all models
  
  // Original function code will never run
  ''' + original_function[original_function.find('{')+1:]
    
    # Replace the function in the content
    modified_content = content[:match_pos] + replacement + content[pos:]
    
    if modified_content == content:
        print("WARNING: Failed to modify token limit function.")
    else:
        print("Token limit function modified successfully.")
    
    return modified_content

def modify_thinking_level(content):
    """Modify the getModeThinkingLevel function to always return 'high'."""
    # Find the function using the exact pattern requested
    pattern = 'getModeThinkingLevel(e)'
    
    # Find the function in the content
    match_pos = content.find(pattern)
    if match_pos == -1:
        print("WARNING: Could not find getModeThinkingLevel function.")
        return content
    
    # Find the opening brace after the pattern
    opening_brace_pos = content.find('{', match_pos)
    if opening_brace_pos == -1:
        print("WARNING: Could not find opening brace for getModeThinkingLevel function.")
        return content
    
    # Find the matching closing brace (considering nested braces)
    brace_count = 1
    pos = opening_brace_pos + 1
    while brace_count > 0 and pos < len(content):
        if content[pos] == '{':
            brace_count += 1
        elif content[pos] == '}':
            brace_count -= 1
        pos += 1
    
    if brace_count != 0:
        print("WARNING: Could not find matching closing brace for getModeThinkingLevel function.")
        return content
    
    # Extract the original function
    original_function = content[match_pos:pos]
    
    # Simple replacement
    replacement = '''getModeThinkingLevel(e) {
  return "high";
}'''
    
    # Replace the function in the content
    modified_content = content[:match_pos] + replacement + content[pos:]
    
    if modified_content == content:
        print("WARNING: Failed to modify thinking level function.")
    else:
        print("Thinking level function modified successfully.")
    
    return modified_content

def modify_ui_styling(content, style="gradient"):
    """
    Modify the Claude 3.7 UI styling.
    
    Args:
        content: The file content
        style: "gradient", "red", or "animated"
    
    Returns:
        Modified content
    """
    # Use the exact search pattern as requested
    search_pattern = '_serializableTitle:()=>"claude-3.7-sonnet"}'
    
    # Find the pattern in the content
    match_pos = content.find(search_pattern)
    if match_pos == -1:
        print("WARNING: Could not find UI styling pattern.")
        return content
    
    # Find the start of the object (looking for 'a=' or 'a =' before the pattern)
    line_start = content.rfind('a=', 0, match_pos)
    if line_start == -1:
        line_start = content.rfind('a =', 0, match_pos)
        if line_start == -1:
            print("WARNING: Could not find the start of the UI styling object.")
            return content
    
    # Find the end of the object (the closing brace is already in our search pattern)
    line_end = match_pos + len(search_pattern)
    
    # Extract the original line
    original_line = content[line_start:line_end]
    
    # Define the replacements based on style
    if style == "gradient":
        replacement = 'a={...e,title:"claude-3.7-sonnet",id:r,subTitle:"HACKED",subTitleClass:"!opacity-100 gradient-text-high font-bold",_serializableTitle:()=>"3.7 Hacked"}'
    elif style == "red":
        replacement = 'a={...e,title:"claude-3.7-sonnet",id:r,subTitle:"HACKED",subTitleClass:"!opacity-100 text-red-600 font-bold",_serializableTitle:()=>"3.7 Hacked"}'
    elif style == "animated":
        replacement = 'a={...e,title:"claude-3.7-sonnet",id:r,subTitle:"HACKED",subTitleClass:"!opacity-100 text-red-500 animate-pulse font-bold",_serializableTitle:()=>"3.7 Hacked"}'
    
    # Replace the original line in the content
    modified_content = content[:line_start] + replacement + content[line_end:]
    
    if modified_content == content:
        print("WARNING: Failed to modify UI styling.")
    else:
        print("UI styling modified successfully.")
    
    return modified_content

def modify_file(file_path, token_mode="claude37_only", ui_style="gradient", skip_backup=False):
    """Apply all modifications to the specified file."""
    try:
        # Check if file exists
        if not os.path.isfile(file_path):
            print(f"Error: File not found: {file_path}")
            return False
        
        # Create backup unless skipped
        if not skip_backup:
            create_backup(file_path)
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply modifications
        print("Applying modifications...")
        content = modify_token_limit(content, token_mode)
        content = modify_thinking_level(content)
        content = modify_ui_styling(content, ui_style)
        
        # Write modified content back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Successfully modified: {file_path}")
        return True
    
    except Exception as e:
        print(f"Error modifying file: {e}")
        return False

def find_cursor_workbench_file():
    """Try to find the Cursor workbench.desktop.main.js file in common locations."""
    potential_paths = [
        # macOS paths
        "/Applications/Cursor.app/Contents/Resources/app/out/vs/workbench/workbench.desktop.main.js",
        os.path.expanduser("~/Applications/Cursor.app/Contents/Resources/app/out/vs/workbench/workbench.desktop.main.js"),
        
        # Windows paths
        "C:\\Program Files\\Cursor\\resources\\app\\out\\vs\\workbench\\workbench.desktop.main.js",
        "C:\\Program Files (x86)\\Cursor\\resources\\app\\out\\vs\\workbench\\workbench.desktop.main.js",
        os.path.expanduser("~\\AppData\\Local\\Programs\\Cursor\\resources\\app\\out\\vs\\workbench\\workbench.desktop.main.js"),
        
        # Linux paths
        "/usr/share/cursor/resources/app/out/vs/workbench/workbench.desktop.main.js",
        os.path.expanduser("~/.local/share/cursor/resources/app/out/vs/workbench/workbench.desktop.main.js")
    ]
    
    for path in potential_paths:
        if os.path.isfile(path):
            return path
    
    return None

def main():
    """Main function to parse arguments and run the script."""
    parser = argparse.ArgumentParser(description="Hack Claude 3.7 in Cursor")
    
    parser.add_argument("--file", "-f", help="Path to workbench.desktop.main.js file")
    parser.add_argument("--token-mode", "-t", choices=["claude37_only", "all_models"], 
                        default="claude37_only", help="Token limit mode")
    parser.add_argument("--ui-style", "-u", choices=["gradient", "red", "animated"], 
                        default="gradient", help="UI styling mode")
    parser.add_argument("--skip-backup", "-s", action="store_true", 
                        help="Skip creating a backup file")
    
    args = parser.parse_args()
    
    # If file path not provided, try to find it
    if not args.file:
        detected_file = find_cursor_workbench_file()
        if detected_file:
            print(f"Found Cursor workbench file at: {detected_file}")
            args.file = detected_file
        else:
            print("Could not automatically detect Cursor workbench.desktop.main.js file.")
            print("Please provide the file path using the --file option.")
            return 1
    
    # Perform the modifications
    success = modify_file(args.file, args.token_mode, args.ui_style, args.skip_backup)
    
    if success:
        print("\nHack complete! You may need to restart Cursor for changes to take effect.")
        print("\nModifications applied:")
        if args.token_mode == "claude37_only":
            print("- Token limit set to 200,000 for Claude 3.7 models only")
        else:
            print("- Token limit set to 200,000 for ALL models")
        print("- Thinking level set to HIGH for all conversations")
        print(f"- UI styling set to {args.ui_style.upper()} mode")
        return 0
    else:
        print("\nHack failed. Please check the error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
