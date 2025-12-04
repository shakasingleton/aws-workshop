#!/bin/bash

echo "Initializing git repository..."
git init

echo "Adding all files..."
git add .

echo "Creating initial commit..."
git commit -m "Initial commit: FastAPI backend and CDK infrastructure setup"

echo ""
echo "Git repository initialized successfully!"
echo ""
echo "Next steps:"
echo "1. Create a new repository on GitHub/GitLab/etc"
echo "2. Run these commands (replace with your repo URL):"
echo ""
echo "   git remote add origin <your-repo-url>"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
