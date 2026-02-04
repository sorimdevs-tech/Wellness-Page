#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import asyncio

async def mark_expired_appointments():
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.wellnesscare
    
    now = datetime.utcnow()
    
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
    
    client.close()

if __name__ == "__main__":
    asyncio.run(mark_expired_appointments())
