#!/bin/bash

# FastAPI Generator Installation Script
# This script sets up the generator for easy global access

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATOR_SCRIPT="$SCRIPT_DIR/generate_project.py"

echo "╔═══════════════════════════════════════════════════╗"
echo "║     FastAPI Generator - Installation Script      ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Make generator executable
echo ""
echo "Making generator executable..."
chmod +x "$GENERATOR_SCRIPT"
echo "✓ Generator is now executable"

# Detect shell
echo ""
echo "Detecting your shell..."
SHELL_CONFIG=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
    echo "✓ Detected Zsh shell"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
    echo "✓ Detected Bash shell"
else
    echo "⚠ Unknown shell: $SHELL"
    echo "You can manually add the alias to your shell config file"
fi

# Create alias
echo ""
echo "Setting up global alias 'fastapi-gen'..."

ALIAS_LINE="alias fastapi-gen='python3 $GENERATOR_SCRIPT'"

if [ -n "$SHELL_CONFIG" ]; then
    # Check if alias already exists
    if grep -q "alias fastapi-gen=" "$SHELL_CONFIG" 2>/dev/null; then
        echo "⚠ Alias already exists in $SHELL_CONFIG"
        read -p "Do you want to update it? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Remove old alias
            sed -i.bak '/alias fastapi-gen=/d' "$SHELL_CONFIG"
            echo "$ALIAS_LINE" >> "$SHELL_CONFIG"
            echo "✓ Updated alias in $SHELL_CONFIG"
        else
            echo "Skipping alias update"
        fi
    else
        echo "$ALIAS_LINE" >> "$SHELL_CONFIG"
        echo "✓ Added alias to $SHELL_CONFIG"
    fi
fi

# Create fastapi-gen script in /usr/local/bin (optional)
echo ""
read -p "Do you want to install 'fastapi-gen' command globally? (requires sudo) (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    WRAPPER_SCRIPT="/usr/local/bin/fastapi-gen"

    # Create wrapper script
    cat > /tmp/fastapi-gen << EOF
#!/bin/bash
python3 "$GENERATOR_SCRIPT" "\$@"
EOF

    # Install with sudo
    sudo mv /tmp/fastapi-gen "$WRAPPER_SCRIPT"
    sudo chmod +x "$WRAPPER_SCRIPT"
    echo "✓ Installed global 'fastapi-gen' command"
fi

echo ""
echo "╔═══════════════════════════════════════════════════╗"
echo "║              Installation Complete!               ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. Reload your shell configuration:"
if [ -n "$SHELL_CONFIG" ]; then
    echo "   source $SHELL_CONFIG"
fi
echo ""
echo "2. Test the generator:"
echo "   fastapi-gen --help"
echo "   OR"
echo "   fastapi-gen \"My First API\""
echo ""
echo "3. Read the documentation:"
echo "   cat QUICKSTART.md"
echo ""
echo "Happy coding! 🚀"
