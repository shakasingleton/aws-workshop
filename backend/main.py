from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key
import os
import re

app = FastAPI(title="Event Management API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE', 'EventsTable')
table = dynamodb.Table(table_name)

# Pydantic models
class Event(BaseModel):
    eventId: str = Field(..., pattern=r'^[a-zA-Z0-9_-]+$')
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=2000)
    date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    location: str = Field(..., min_length=1, max_length=200)
    capacity: int = Field(..., gt=0)
    organizer: str = Field(..., min_length=1, max_length=100)
    status: str = Field(..., pattern=r'^(active|cancelled|completed)$')

    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Invalid date format. Use YYYY-MM-DD')
        return v

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=2000)
    date: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}-\d{2}$')
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    capacity: Optional[int] = Field(None, gt=0)
    organizer: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[str] = Field(None, pattern=r'^(active|cancelled|completed)$')

    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD')
        return v

@app.get("/")
def read_root():
    return {"message": "Event Management API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/events", status_code=201)
def create_event(event: Event):
    try:
        # Check if event already exists
        response = table.get_item(Key={'eventId': event.eventId})
        if 'Item' in response:
            raise HTTPException(status_code=409, detail="Event already exists")
        
        # Use ExpressionAttributeNames to handle reserved keywords
        table.put_item(
            Item={
                'eventId': event.eventId,
                'title': event.title,
                'description': event.description,
                'date': event.date,
                'location': event.location,
                'capacity': event.capacity,
                'organizer': event.organizer,
                'status': event.status
            }
        )
        return event.model_dump()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/events/{event_id}")
def get_event(event_id: str):
    try:
        response = table.get_item(Key={'eventId': event_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Event not found")
        return response['Item']
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/events")
def list_events(status: Optional[str] = None):
    try:
        if status:
            # Filter by status using scan with filter expression
            response = table.scan(
                FilterExpression='#s = :status',
                ExpressionAttributeNames={'#s': 'status'},
                ExpressionAttributeValues={':status': status}
            )
        else:
            response = table.scan()
        return {"events": response.get('Items', [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.put("/events/{event_id}")
def update_event(event_id: str, event_update: EventUpdate):
    try:
        # Check if event exists
        response = table.get_item(Key={'eventId': event_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Build update expression
        update_data = event_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_expression = "SET " + ", ".join([f"#{k} = :{k}" for k in update_data.keys()])
        expression_attribute_names = {f"#{k}": k for k in update_data.keys()}
        expression_attribute_values = {f":{k}": v for k, v in update_data.items()}
        
        response = table.update_item(
            Key={'eventId': event_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )
        return response['Attributes']
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.delete("/events/{event_id}")
def delete_event(event_id: str):
    try:
        # Check if event exists
        response = table.get_item(Key={'eventId': event_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Event not found")
        
        table.delete_item(Key={'eventId': event_id})
        return {"message": "Event deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
