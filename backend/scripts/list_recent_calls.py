import httpx
import asyncio
import json
import sys
import os
from datetime import datetime

# Fix path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_settings

settings = get_settings()

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

async def list_recent_calls():
    headers = {
        "Authorization": f"Bearer {settings.vapi_api_key}",
        "Content-Type": "application/json"
    }

    print(f"Fetching recent calls from VAPI...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.vapi.ai/call?limit=10",
                headers=headers
            )
            
            if response.status_code == 200:
                calls = response.json()
                # Sort by startedAt descending
                calls.sort(key=lambda x: x.get('startedAt', ''), reverse=True)

                if calls:
                    print(f"LATEST_CALL_ID:{calls[0].get('id')}")
                else:
                    print("NO_CALLS_FOUND")
                    
            else:
                print(f"❌ Failed to fetch calls: {response.status_code}")
                print(response.text)
                    
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(list_recent_calls())
