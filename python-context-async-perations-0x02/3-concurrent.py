#!/usr/bin/env python3

import asyncio
import aiosqlite

async def async_fetch_users():
    """Fetch all users from the database"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    """Fetch users older than 40 from the database"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    """Execute both queries concurrently using asyncio.gather"""
    # Execute both queries concurrently
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    # Print results
    print("All users:")
    for user in all_users:
        print(user)
    
    print("\nUsers older than 40:")
    for user in older_users:
        print(user)

if __name__ == "__main__":
    # Run the concurrent fetch
    asyncio.run(fetch_concurrently())