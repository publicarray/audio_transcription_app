#!/usr/bin/env python
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    """Wrapper function to run the Streamlit app."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "app.py")
    
    # Import streamlit and run the app directly
    import streamlit.web.cli as stcli
    
    # Prepare the args - similar to ["streamlit", "run", app_path]
    sys.argv = [sys.argv[0], "run", app_path] + sys.argv[1:]
    
    # Run the streamlit app
    stcli.main()

if __name__ == "__main__":
    main()