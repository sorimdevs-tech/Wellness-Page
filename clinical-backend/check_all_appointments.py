#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import asyncio

async def check_all_appointments():
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.wellnesscare
    
    # Get all appointments
    all_appointments = await db.appointments.find({}).to_list(length=100)
    
    print(f"\n📊 Total appointments in database: {len(all_appointments)}")
    
    # Group by status
    status_counts = {}
    for apt in all_appointments:
        status = apt.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("\n📋 Appointments by status:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    
    # Check appointments with dates in January 2026
    print("\n\n📅 Appointments from January 2026:")
    now = datetime.utcnow()
    for apt in all_appointments[:10]:  # Show first 10
        apt_date = apt.get('appointment_date')
        if apt_date:
            print(f"\nID: {str(apt.get('_id'))[:8]}...")
            print(f"  Status: {apt.get('status')}")
            print(f"  Date: {apt_date}")
            print(f"  Is past?: {apt_date < now if isinstance(apt_date, datetime) else 'N/A'}")
            print(f"  Patient: {apt.get('patient_id', 'N/A')}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_all_appointments())
