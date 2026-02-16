import os
import instructor
from openai import OpenAI
from typing import Type, TypeVar, List, Optional, Any
from pydantic import BaseModel
from dotenv import load_dotenv
from src.config import DEFAULT_MODEL, SYSTEM_PROMPT

# Load environment variables
load_dotenv()

T = TypeVar("T", bound=BaseModel)

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = instructor.patch(
            OpenAI(api_key=self.api_key),
            mode=instructor.Mode.JSON
        )

    def _build_prompt(self, raw_text: str, previous_errors: Optional[List[str]] = None) -> str:
        prompt = f"Extract structured information from the following text:\n\n{raw_text}\n"
        
        if previous_errors:
            prompt += "\n### Previous Validation Errors found in your last output:\n"
            for error in previous_errors:
                prompt += f"- {error}\n"
            prompt += "\nPlease correct these errors in your new response using mathematical logic."
            
        return prompt

    def extract_structured_data(
        self, 
        text: str, 
        response_model: Type[T], 
        errors: Optional[List[str]] = None,
        max_retries: int = 3
    ) -> T:
        prompt = self._build_prompt(text, errors)
        
        try:
            return self.client.chat.completions.create(
                model=DEFAULT_MODEL,
                response_model=response_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_retries=max_retries
            )
        except Exception as e:
            # Graceful error handling for API issues
            print(f"Error during extraction: {e}")
            raise

def extract_structured_data(text: str, schema: Type[T], errors: Optional[List[str]] = None) -> T:
    """Helper function to perform extraction."""
    client = LLMClient()
    return client.extract_structured_data(text, schema, errors)
