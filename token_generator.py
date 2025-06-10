# token_generator.py

import os
import jwt
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get LiveKit credentials and room
API_KEY = os.getenv("LIVEKIT_API_KEY")
API_SECRET = os.getenv("LIVEKIT_API_SECRET")
ROOM_NAME = os.getenv("LIVEKIT_ROOM", "default-room")

# Generate token function
def create_token(identity="user", ttl_seconds=3600):
    now = int(time.time())

    payload = {
    "jti": f"{identity}-{now}",
    "iss": API_KEY,
    "sub": identity,
    "nbf": now,
    "exp": now + ttl_seconds,
    "video": {
        "room_join": True,
        "room": ROOM_NAME,        
        "can_publish": True,
        "can_subscribe": True
    }
}


    token = jwt.encode(payload, API_SECRET, algorithm="HS256")
    return token

# Run and print the token
if __name__ == "__main__":
    identity = "testuser"
    token = create_token(identity)
    print("\n✅ LiveKit JWT Token Generated!\n")
    print(f"🔑 Identity: {identity}")
    print(f"🛋️ Room: {ROOM_NAME}")
    print(f"🧾 Token:\n\n{token}\n")
