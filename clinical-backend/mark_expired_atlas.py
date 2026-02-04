#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import asyncio

async def mark_expired_appointments():
    # Connect to MongoDB Atlas (from config)
    MONGODB_URL = "mongodb+srv://sorimdevs_db_user:USRvJ36YOlw59026@wellnessdev.shmitlo.mongodb.net/?appName=WellnessDev"
    DATABASE_NAME = "wellness_db"
    
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    now = datetime.now(timezone.utc)
    
    # Mark expired: pending appointments where date has passed
    query_expired = {
        "status": "pending",
        "appointment_date": {"$lt": now}
    }
    
    result_expired = await db.appointments.update_many(
        query_expired,
        {"$set": {"status": "expired", "auto_expired_at": now}}
    )
    
    # Mark missed: approved/scheduled appointments where date has passed
    query_missed = {
        "status": {"$in": ["approved", "scheduled"]},
        "appointment_date": {"$lt": now}
    }
    
    result_missed = await db.appointments.update_many(
        query_missed,
        {"$set": {"status": "missed", "auto_missed_at": now}}
    )
    
    print(f"✅ Updated appointments:")
    print(f"   - Expired: {result_expired.modified_count} (pending past appointments)")
    print(f"   - Missed: {result_missed.modified_count} (approved/scheduled past appointments)")
    
    # Show current status counts
    all_appointments = await db.appointments.find({}).to_list(length=1000)
    status_counts = {}
    for apt in all_appointments:
        status = apt.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print(f"\n📊 Appointment status counts after update:")
    for status, count in sorted(status_counts.items()):
        print(f"   {status}: {count}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(mark_expired_appointments())
