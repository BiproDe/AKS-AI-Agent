"""
Utility functions for the Kubernetes Discovery Agent
"""
import os

def write_to_file_md(file_path: str, content: str) -> None:
    """
    Write content to a markdown file.
    
    Args:
        file_path (str): Path to the file to write
        content (str): Content to write to the file
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully wrote content to {file_path}")
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")
        raise
