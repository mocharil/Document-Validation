# project/config.py
from google.oauth2 import service_account
import vertexai
from dotenv import load_dotenv
import os
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
)


# Load environment variables from .env file
load_dotenv()

project_id = os.getenv('PROJECT_ID')
credentials_file_path = os.getenv('CREDENTIALS_FILE_PATH')

credentials = service_account.Credentials.from_service_account_file(credentials_file_path)
vertexai.init(project=project_id, credentials=credentials)
model = os.getenv("GEMINI_MODEL")
multimodal_model = GenerativeModel(model)

safety_config = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}

generation_config = GenerationConfig(temperature=0.0, top_p=1, top_k=32)
