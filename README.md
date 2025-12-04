# Event Management API

A serverless event management system built with FastAPI, AWS Lambda, API Gateway, and DynamoDB. This project provides a RESTful API for creating, reading, updating, and deleting events.

## Features

- **RESTful API** for event management (CRUD operations)
- **Serverless Architecture** using AWS Lambda and API Gateway
- **DynamoDB** for scalable data storage
- **FastAPI** for high-performance API development
- **Pydantic** for data validation
- **AWS CDK** for infrastructure as code
- **CORS enabled** for web access

## Project Structure

```
.
├── backend/              # FastAPI application
│   ├── main.py          # Main FastAPI app with API endpoints
│   ├── lambda_handler.py # Lambda handler using Mangum
│   ├── lambda_layer/    # Lambda dependencies layer
│   ├── requirements.txt # Python dependencies
│   └── docs/            # Generated API documentation
├── infrastructure/       # AWS CDK project
│   ├── app.py           # CDK app entry point
│   ├── stack.py         # CDK stack definition (Lambda, API Gateway, DynamoDB)
│   ├── cdk.json         # CDK configuration
│   └── requirements.txt # CDK dependencies
└── README.md            # This file
```

## API Endpoints

### Base URL
```
https://a0xfmuum0f.execute-api.us-west-2.amazonaws.com/prod/
```

### Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| GET | `/` | API welcome message | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/events` | List all events | 200 |
| GET | `/events?status=active` | Filter events by status | 200 |
| GET | `/events/{eventId}` | Get specific event | 200 |
| POST | `/events` | Create new event | 201 |
| PUT | `/events/{eventId}` | Update event | 200 |
| DELETE | `/events/{eventId}` | Delete event | 200 |

## Event Schema

```json
{
  "eventId": "string (required, alphanumeric with - and _)",
  "title": "string (required, 1-200 chars)",
  "description": "string (required, 1-2000 chars)",
  "date": "string (required, YYYY-MM-DD format)",
  "location": "string (required, 1-200 chars)",
  "capacity": "integer (required, > 0)",
  "organizer": "string (required, 1-100 chars)",
  "status": "string (required, one of: active, cancelled, completed)"
}
```

## Usage Examples

### Create an Event
```bash
curl -X POST https://a0xfmuum0f.execute-api.us-west-2.amazonaws.com/prod/events \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": "tech-conf-2025",
    "title": "Tech Conference 2025",
    "description": "Annual technology conference",
    "date": "2025-06-15",
    "location": "San Francisco, CA",
    "capacity": 500,
    "organizer": "Tech Events Inc",
    "status": "active"
  }'
```

### Get All Events
```bash
curl https://a0xfmuum0f.execute-api.us-west-2.amazonaws.com/prod/events
```

### Get Events by Status
```bash
curl "https://a0xfmuum0f.execute-api.us-west-2.amazonaws.com/prod/events?status=active"
```

### Get Specific Event
```bash
curl https://a0xfmuum0f.execute-api.us-west-2.amazonaws.com/prod/events/tech-conf-2025
```

### Update an Event
```bash
curl -X PUT https://a0xfmuum0f.execute-api.us-west-2.amazonaws.com/prod/events/tech-conf-2025 \
  -H "Content-Type: application/json" \
  -d '{
    "capacity": 600,
    "status": "completed"
  }'
```

### Delete an Event
```bash
curl -X DELETE https://a0xfmuum0f.execute-api.us-west-2.amazonaws.com/prod/events/tech-conf-2025
```

## Local Development

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Infrastructure Setup

1. Navigate to the infrastructure directory:
```bash
cd infrastructure
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install CDK dependencies:
```bash
pip install -r requirements.txt
```

4. Configure AWS credentials:
```bash
aws configure
```

5. Bootstrap CDK (first time only):
```bash
cdk bootstrap
```

6. Deploy the stack:
```bash
cdk deploy
```

## AWS Architecture

- **API Gateway**: REST API endpoint with CORS enabled
- **Lambda Function**: Python 3.11 runtime running FastAPI via Mangum
- **Lambda Layer**: Contains FastAPI, Pydantic, Boto3, and other dependencies
- **DynamoDB Table**: NoSQL database with on-demand billing
- **IAM Roles**: Least-privilege permissions for Lambda to access DynamoDB

## Technologies Used

- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Mangum** - AWS Lambda adapter for ASGI applications
- **Boto3** - AWS SDK for Python
- **AWS CDK** - Infrastructure as Code framework
- **AWS Lambda** - Serverless compute service
- **Amazon API Gateway** - API management service
- **Amazon DynamoDB** - NoSQL database service

## API Documentation

Detailed API documentation is available in the `backend/docs/` directory. Open `backend/docs/main.html` in a browser to view the full API documentation.

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `404` - Not Found
- `409` - Conflict (duplicate event)
- `500` - Internal Server Error

## License

This project is for educational purposes as part of the AWS Builder Lab.
