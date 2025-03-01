#!/usr/bin/env python
import subprocess
import sys
import os

def main():
    """Wrapper function to run the Streamlit app."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "poetry_app.py")
    
    # Build the command to run streamlit
    cmd = ["streamlit", "run", app_path]
    
    # Add any additional arguments passed to this script
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])
    
    # Run the streamlit command
    subprocess.run(cmd)

if __name__ == "__main__":
    main()

