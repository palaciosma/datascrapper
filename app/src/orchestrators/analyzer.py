# Internal imports
from .base import BaseProcessor
from app.src.services.openai import deepseek_analysis, compose_prompt
from app.src.services.file_operations import load_txt_file
from app.src.config import ANALYSIS_SYSTEM_PROMPT_PATH

class deepseek_analyzer(BaseProcessor):
    def run(self, file_name: str, file_content: str, extraction_schema: list[dict]):
        
        # Decode base64 content to temp file
        temp_file_path = self.load_file(file_name, file_content)
        
        # Extract text from the temp PDF file
        extracted_text = self.extract_text(temp_file_path)
        
        # Compose prompt and extract fields
        system_message = load_txt_file(ANALYSIS_SYSTEM_PROMPT_PATH)
        prompt = compose_prompt(extracted_text, system_message)

        extracted_fields = deepseek_analysis(prompt)

        return extracted_fields
    

