#!/usr/bin/env python3
"""
Claude 3.7 Hack Script with automated backups

This script enhances Claude 3.7 in Cursor by:
1. Increasing token limit to 200,000
2. Setting thinking level to "high"
3. Customizing Claude 3.7 UI styling
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
    # Find the function using a simple pattern
    pattern = r'async\s+getEffectiveTokenLimit\s*\(\s*e\s*\)\s*\{[^}]+\}'
    
    # Get the original function
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print("WARNING: Could not find getEffectiveTokenLimit function.")
        return content
    
    original_function = match.group(0)
    
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
    modified_content = content.replace(original_function, replacement)
    
    if modified_content == content:
        print("WARNING: Failed to modify token limit function.")
    else:
        print("Token limit function modified successfully.")
    
    return modified_content

def modify_thinking_level(content):
    """Modify the getModeThinkingLevel function to always return 'high'."""
    # Find the function using a simple pattern
    pattern = r'getModeThinkingLevel\s*\(\s*e\s*\)\s*\{[^}]+\}'
    
    # Get the original function
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print("WARNING: Could not find getModeThinkingLevel function.")
        return content
    
    original_function = match.group(0)
    
    # Simple replacement as per README
    replacement = '''getModeThinkingLevel(e) {
  return "high";
}'''
    
    # Replace the function in the content
    modified_content = content.replace(original_function, replacement)
    
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
    # Define the patterns exactly as shown in the README
    original_pattern = r'a\s*=\s*\{\s*\.\.\.e\s*,\s*title\s*:\s*"claude-3\.7-sonnet"\s*,\s*id\s*:\s*r\s*,\s*_serializableTitle\s*:\s*\(\s*\)\s*=>\s*"claude-3\.7-sonnet"\s*\}'
    
    # For minified version
    minified_pattern = r'a=\{\.\.\.e,title:"claude-3\.7-sonnet",id:r,_serializableTitle:\(\)=>"claude-3\.7-sonnet"\}'
    
    # Define the replacements based on style
    if style == "gradient":
        replacement = 'a = { ...e, title: "claude-3.7-sonnet", id: r, subTitle: "HACKED", subTitleClass: "!opacity-100 gradient-text-high font-bold", _serializableTitle: () => "3.7 Hacked" }'
        minified_replacement = 'a={...e,title:"claude-3.7-sonnet",id:r,subTitle:"HACKED",subTitleClass:"!opacity-100 gradient-text-high font-bold",_serializableTitle:()=>"3.7 Hacked"}'
    elif style == "red":
        replacement = 'a = { ...e, title: "claude-3.7-sonnet", id: r, subTitle: "HACKED", subTitleClass: "!opacity-100 text-red-600 font-bold", _serializableTitle: () => "3.7 Hacked" }'
        minified_replacement = 'a={...e,title:"claude-3.7-sonnet",id:r,subTitle:"HACKED",subTitleClass:"!opacity-100 text-red-600 font-bold",_serializableTitle:()=>"3.7 Hacked"}'
    elif style == "animated":
        replacement = 'a = { ...e, title: "claude-3.7-sonnet", id: r, subTitle: "HACKED", subTitleClass: "!opacity-100 text-red-500 animate-pulse font-bold", _serializableTitle: () => "3.7 Hacked" }'
        minified_replacement = 'a={...e,title:"claude-3.7-sonnet",id:r,subTitle:"HACKED",subTitleClass:"!opacity-100 text-red-500 animate-pulse font-bold",_serializableTitle:()=>"3.7 Hacked"}'
    
    # Try to replace with the standard pattern
    modified_content = re.sub(original_pattern, replacement, content)
    
    # If no changes were made, try with the minified pattern
    if modified_content == content:
        modified_content = re.sub(minified_pattern, minified_replacement, content)
    
    # Check if either replacement worked
    if modified_content == content:
        # Search for strings with claude-3.7-sonnet to help debugging
        print("WARNING: Could not modify UI styling. Pattern might have changed.")
        
        # Try a simple string search for each line
        search_string = '"claude-3.7-sonnet"'
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if search_string in line and '_serializableTitle' in line and 'id:r' in line:
                print(f"Found potential match on line {i+1}: {line[:100]}...")
        
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