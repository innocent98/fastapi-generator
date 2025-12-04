#!/bin/bash

# FastAPI Project Generator - Uninstall Script
# This script removes the fastapi-gen global command

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Determine the install directory based on where fastapi-gen is located
if [ -f "/usr/local/bin/fastapi-gen" ]; then
    INSTALL_DIR="/usr/local/bin"
    NEEDS_SUDO=true
elif [ -f "$HOME/.local/bin/fastapi-gen" ]; then
    INSTALL_DIR="$HOME/.local/bin"
    NEEDS_SUDO=false
else
    INSTALL_DIR=""
    NEEDS_SUDO=false
fi

WRAPPER_SCRIPT="$INSTALL_DIR/fastapi-gen"

echo "============================================================"
echo "FastAPI Project Generator - Uninstaller"
echo "============================================================"
echo ""

# Check if fastapi-gen is installed
if [ -z "$INSTALL_DIR" ] || [ ! -f "$WRAPPER_SCRIPT" ]; then
    echo "❌ fastapi-gen is not installed"
    echo "   Checked locations:"
    echo "   - /usr/local/bin/fastapi-gen"
    echo "   - $HOME/.local/bin/fastapi-gen"
    exit 1
fi

# Remove the wrapper script
echo "Found fastapi-gen in $INSTALL_DIR"
echo "Removing fastapi-gen..."

if [ "$NEEDS_SUDO" = true ]; then
    echo "This will require sudo permissions..."
    sudo rm -f "$WRAPPER_SCRIPT"
else
    rm -f "$WRAPPER_SCRIPT"
fi

if [ $? -eq 0 ]; then
    echo "✓ fastapi-gen removed successfully from $INSTALL_DIR"
    echo ""
    echo "============================================================"
    echo "✓ Uninstallation complete!"
    echo "============================================================"
    echo ""
    echo "The generator script (generate_project.py) is still available"
    echo "in this directory if you want to use it directly or reinstall."
    echo ""
    echo "To reinstall: ./install.sh"
    echo ""
else
    echo "❌ Failed to remove fastapi-gen"
    exit 1
fi
