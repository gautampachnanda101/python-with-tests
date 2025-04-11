#!/bin/bash

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit..."
    pip install pre-commit
fi

# Install the pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

echo "Pre-commit hooks installed successfully!"
echo "These hooks will now run automatically on every commit."
echo ""
echo "You can also run them manually with:"
echo "  pre-commit run --all-files"
echo ""
echo "To temporarily bypass hooks, use:"
echo "  git commit -m 'Your message' --no-verify"
