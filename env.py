from dotenv import load_dotenv 
import os 

load_dotenv(dotenv_path=".env")

GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
POSTGRES_URL= os.getenv("POSTGRES_URL")
JWT_SECRET= os.getenv("JWT_SECRET")
ORIGIN_URL= os.getenv("ORIGIN_URL")