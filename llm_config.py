from crewai import LLM
import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=GOOGLE_API_KEY,
    temperature=0.1
)
