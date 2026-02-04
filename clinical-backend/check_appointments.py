#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import asyncio

async def check_appointments():
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.wellnesscare
    
    # Get a few appointments to see their structure
    appointments = await db.appointments.find({"status": "pending"}).limit(5).to_list(length=5)
    
    print(f"Found {len(appointments)} pending appointments")
    print("\nSample appointment data:")
    for apt in appointments:
        print(f"\nAppointment ID: {apt.get('_id')}")
        print(f"  Status: {apt.get('status')}")
        print(f"  Date field: {apt.get('appointment_date')}")
        print(f"  Date type: {type(apt.get('appointment_date'))}")
        print(f"  Patient ID: {apt.get('patient_id')}")
        print(f"  Doctor ID: {apt.get('doctor_id')}")
    
    # Check current time
    now = datetime.utcnow()
    print(f"\n\nCurrent UTC time: {now}")
    print(f"Current UTC time type: {type(now)}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_appointments())
