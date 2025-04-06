import os
from dotenv import load_dotenv

load_dotenv()

# LLM
BASE_MODEL_NAME = os.getenv('BASE_MODEL_NAME')
BASIC_LLM_URL = os.getenv('BASIC_LLM_URL')
BASIC_LLM_API_KEY = os.getenv('BASIC_LLM_API_KEY')
# Tavily API 
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
