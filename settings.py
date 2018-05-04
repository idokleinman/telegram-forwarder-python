from dotenv import load_dotenv
import os
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

phone = os.getenv("PHONE")
username = os.getenv("USERNAME")

from_channel_link = os.getenv("FROM_CHANNEL_LINK")
to_user = os.getenv("TO_USER")
poll_interval = int(os.getenv("POLL_INTERVAL"))
