#!/usr/bin/env python3
"""
Build Script for Audio Transcription App
----------------------------------------

This script detects the operating system and builds the appropriate executable using PyInstaller.
It will create either a Linux AppImage or a Windows executable depending on the platform.

Requirements:
    - PyInstaller: pip install pyinstaller
    - All dependencies for the application must be installed
    - For Linux: appimagetool must be installed for AppImage creation
    - For Windows: On a Linux system, you need wine and Windows Python installed for cross-compilation

Usage:
    python build.py [--skip-deps-check] [--cross-compile]

Options:
    --skip-deps-check    Skip checking for dependencies (use if you're sure everything is installed)
    --cross-compile      Attempt to cross-compile (e.g. build Windows exe on Linux using Wine)

Example:
    python build.py              # Build for the current platform
    python build.py --cross-compile  # Try to build for the other platform as well
"""

import os
import sys
import platform
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """
    Check if necessary dependencies are installed.
    Returns True if all dependencies are met, False otherwise.
    """
    try:
        # Check if PyInstaller is installed
        import PyInstaller
        print("✓ PyInstaller is installed")
        
        # Check for poetry environment
        try:
            import poetry
            print("✓ Poetry is installed")
        except ImportError:
            print("! Poetry not found. It's recommended to use Poetry for dependency management")
            print("  Install with: pip install poetry")
            
        # Check for python-dotenv (used in the application)
        try:
            import dotenv
            print("✓ python-dotenv is installed")
        except ImportError:
            print("✗ python-dotenv not found, which is required for environment variable loading")
            print("  Install with: pip install python-dotenv")
            return False

        # Check platform-specific dependencies
        if platform.system() == "Linux":
            # Check for appimagetool on Linux
            appimagetool = subprocess.run(
                ["which", "appimagetool"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            if appimagetool.returncode != 0:
                print("✗ appimagetool not found, which is required for AppImage creation")
                print("  Install instructions: https://appimage.org/")
                return False
            print("✓ appimagetool is installed")
            
        elif platform.system() == "Windows":
            # Windows-specific checks could go here
            pass
        
        return True
    
    except ImportError:
        print("✗ PyInstaller not found, which is required for building executables")
        print("  Install with: pip install pyinstaller")
        return False

def build_linux():
    """Build Linux AppImage using PyInstaller."""
    print("\n=== Building Linux AppImage ===\n")
    
    # Ensure the spec file exists
    if not os.path.exists("linux_app.spec"):
        print("✗ linux_app.spec not found!")
        return False
    
    # Clean up any existing AppDir and AppImage files
    print("Cleaning up existing build artifacts...")
    app_dir = Path("AppDir")
    app_image = Path("Audio_Transcription_App-x86_64.AppImage")
    
    if app_dir.exists():
        print(f"- Removing {app_dir}")
        subprocess.run(["rm", "-rf", str(app_dir)], check=True)
    
    if app_image.exists():
        print(f"- Removing {app_image}")
        subprocess.run(["rm", "-f", str(app_image)], check=True)
    
    # Run PyInstaller
    try:
        print("Running PyInstaller with linux_app.spec file...")
        subprocess.run(
            ["pyinstaller", "linux_app.spec", "--clean", "--noconfirm"], 
            check=True
        )
        print("✓ PyInstaller build completed successfully")
        
        # Verify if the AppImage was created
        if app_image.exists():
            # Make the AppImage executable
            subprocess.run(["chmod", "+x", str(app_image)], check=True)
            size_mb = app_image.stat().st_size / (1024 * 1024)
            print(f"\n✓ AppImage created successfully: {app_image} ({size_mb:.1f} MB)")
            
            # Verify the AppImage is valid
            try:
                # Run a simple test to see if the AppImage executable works
                print("Verifying AppImage integrity...")
                result = subprocess.run(
                    [f"./{app_image}", "--help"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5  # Timeout after 5 seconds
                )
                if result.returncode == 0:
                    print("✓ AppImage verification passed - executable runs correctly")
                else:
                    print(f"! AppImage verification warning: The AppImage returned non-zero exit code {result.returncode}")
                    print(f"! Error output: {result.stderr}")
            except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
                print(f"! AppImage verification warning: {e}")
                print("! The AppImage was created but may not be functioning correctly")
            
            print("\n✓ Linux build completed successfully")
            return True
        else:
            print("\n✗ AppImage creation failed: AppImage file not found")
            print("  PyInstaller completed, but the AppImage wasn't generated.")
            print("  Check if appimagetool is installed and working correctly.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"✗ PyInstaller build failed: {e}")
        return False

def build_windows():
    """Build Windows executable using PyInstaller."""
    print("\n=== Building Windows Executable ===\n")
    
    # Ensure the spec file exists
    if not os.path.exists("windows_app.spec"):
        print("✗ windows_app.spec not found!")
        return False
    
    # Run PyInstaller
    try:
        print("Running PyInstaller with windows_app.spec file...")
        subprocess.run(
            ["pyinstaller", "windows_app.spec", "--clean", "--noconfirm"], 
            check=True
        )
        print("✓ PyInstaller build completed successfully")
        print("\n✓ Windows build completed: dist/audio_transcription_app.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ PyInstaller build failed: {e}")
        return False

def cross_compile_windows():
    """
    Attempt to cross-compile a Windows executable from Linux.
    This is an advanced feature and requires Wine and Windows Python.
    """
    print("\n=== Cross-compiling Windows Executable from Linux ===\n")
    print("! Cross-compilation is an advanced feature and may not work in all environments")
    
    # Check if Wine is installed
    wine_check = subprocess.run(
        ["which", "wine"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    if wine_check.returncode != 0:
        print("✗ Wine not found, which is required for Windows cross-compilation")
        print("  Install Wine: sudo apt install wine")
        return False
    
    # Here you would add the specific commands to use Wine with PyInstaller
    # This is a complex setup and would need customization for your environment
    print("! Automated cross-compilation setup not implemented")
    print("  Manual steps:")
    print("  1. Install Windows Python in Wine")
    print("  2. Install PyInstaller in the Windows Python environment")
    print("  3. Run: wine python.exe -m PyInstaller windows_app.spec")
    
    return False

def main():
    """Main function to run the build process."""
    parser = argparse.ArgumentParser(description="Build audio transcription app executables")
    parser.add_argument("--skip-deps-check", action="store_true", help="Skip dependency checking")
    parser.add_argument("--cross-compile", action="store_true", help="Try cross-compilation")
    args = parser.parse_args()
    
    # Check dependencies unless explicitly skipped
    if not args.skip_deps_check:
        if not check_dependencies():
            print("\n✗ Dependency check failed. Fix the issues or use --skip-deps-check to bypass.")
            return 1
    
    # Detect system and build appropriate package
    system = platform.system()
    
    if system == "Linux":
        build_linux()
        if args.cross_compile:
            cross_compile_windows()
    elif system == "Windows":
        build_windows()
    else:
        print(f"✗ Unsupported platform: {system}")
        print("  This build script only supports Linux and Windows.")
        return 1
    
    print("\n=== Build Process Complete ===")
    print("\nIf you encounter any issues:")
    print("1. Check that all dependencies are correctly installed")
    print("2. Ensure PyInstaller has access to all required modules")
    print("3. For advanced troubleshooting, run PyInstaller manually with the --debug flag")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

