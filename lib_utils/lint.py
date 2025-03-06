#!/usr/bin/env python3
"""Script to run pylint on the entire repository and auto-fix common issues."""

import os
import sys
import subprocess

def auto_fix_code(src_dir):
    """Auto-fix common code style issues."""
    print("\nAuto-fixing code style issues...")
    
    # Run isort to fix import order
    print("\nFixing import order with isort...")
    subprocess.run(
        [sys.executable, "-m", "isort", src_dir, "--profile", "black"],
        check=False
    )
    
    # Run autopep8 to fix PEP 8 issues
    print("\nFixing PEP 8 issues with autopep8...")
    subprocess.run(
        [
            sys.executable, "-m", "autopep8",
            "--in-place",
            "--recursive",
            "--aggressive",
            "--aggressive",
            "--max-line-length", "100",
            src_dir
        ],
        check=False
    )

def run_pylint():
    """Run pylint on the src directory and auto-fix common issues."""
    try:
        # Get the root directory of the project (one level up from lib_utils)
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        src_dir = os.path.join(root_dir, "src")
        
        # Add project root to PYTHONPATH
        env = os.environ.copy()
        if 'PYTHONPATH' in env:
            env['PYTHONPATH'] = f"{root_dir}{os.pathsep}{env['PYTHONPATH']}"
        else:
            env['PYTHONPATH'] = root_dir
        
        # First, auto-fix what we can
        auto_fix_code(src_dir)
        
        # Then run pylint to check remaining issues
        print("\nRunning pylint to check remaining issues...")
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pylint",
                src_dir,
                "--recursive=y",
                "--disable=C0114,C0115,C0116",  # Disable all docstring warnings
            ],
            capture_output=True,
            text=True,
            check=False,
            env=env
        )
        
        # Print the output
        print(result.stdout)
        if result.stderr:
            print("Errors:", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            
        # Return the exit code
        return result.returncode
        
    except subprocess.CalledProcessError as e:
        print(f"Error running tools: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(run_pylint())