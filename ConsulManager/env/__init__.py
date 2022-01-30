from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent

for file_env in env_path.glob("*.env"):
    print(f"loading: {file_env}")
    load_dotenv(file_env)