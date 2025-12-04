# Setup Instructions for Task 2

## What's Been Done

✅ **MCP Servers Configured** in `.kiro/settings/mcp.json`:
- AWS Knowledge Base Retrieval (aws-kb-retrieval)
- AWS Frontend (aws-frontend)
- AWS CDK (aws-cdk)
- Brave Search (brave-search) - needs API key
- Fetch (fetch)

✅ **Project Structure Created**:
```
backend/
  ├── main.py              # FastAPI app with basic endpoints
  ├── requirements.txt     # FastAPI dependencies
  └── __init__.py

infrastructure/
  ├── app.py              # CDK app entry point
  ├── stack.py            # CDK stack (empty for now)
  ├── cdk.json            # CDK configuration
  ├── requirements.txt    # CDK dependencies
  └── __init__.py

.kiro/
  └── settings/
      └── mcp.json        # MCP server configuration

.gitignore                # Excludes Python cache, CDK output, etc.
                         # NOTE: .kiro folder is NOT ignored
README.md                 # Project documentation
```

## Next Steps

### 1. Initialize Git and Push to Remote

In a **new terminal window**, run:

```bash
cd "/Users/shakasingleton/Desktop/AWS Workshop"

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: FastAPI backend and CDK infrastructure setup"

# Create a new repo on GitHub, then:
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

### 2. Optional: Add Brave Search API Key

If you want to use Brave Search, edit `.kiro/settings/mcp.json` and add your API key:
```json
"brave-search": {
  "command": "uvx",
  "args": ["mcp-server-brave-search"],
  "env": {
    "BRAVE_API_KEY": "your-api-key-here"
  }
}
```

### 3. Verify MCP Servers

After saving mcp.json, Kiro should automatically connect to the MCP servers. You can verify by checking the MCP panel in Kiro.

## Quick Start Commands

**Run Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Test CDK:**
```bash
cd infrastructure
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cdk synth
```
