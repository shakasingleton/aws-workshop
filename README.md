# AWS Builder Lab Project

This project contains a FastAPI backend and AWS CDK infrastructure.

## Project Structure

```
.
├── backend/              # FastAPI application
│   ├── main.py          # Main FastAPI app
│   └── requirements.txt # Python dependencies
├── infrastructure/       # AWS CDK project
│   ├── app.py           # CDK app entry point
│   ├── stack.py         # CDK stack definition
│   ├── cdk.json         # CDK configuration
│   └── requirements.txt # CDK dependencies
└── .kiro/               # Kiro configuration (version controlled)
    └── settings/
        └── mcp.json     # MCP server configuration
```

## Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Infrastructure Setup

```bash
cd infrastructure
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cdk synth
```

## MCP Servers Configured

- AWS Knowledge Base Retrieval
- AWS Frontend
- AWS CDK
- Brave Search
- Fetch
