import os

# State Machine Configuration
MAX_ATTEMPTS = 3

# File Processing
SUPPORTED_EXTENSIONS = {
    ".txt": "text",
    ".pdf": "pdf",
    ".docx": "docx",
    ".doc": "docx"
}

# LLM Configuration
DEFAULT_MODEL = "gpt-4o-mini"
TEMPERATURE = 0.0

# Prompt Templates
SYSTEM_PROMPT = (
    "You are a literal data extraction assistant. "
    "Extract values EXACTLY as mentioned in the text. "
    "Do not perform your own calculations or fix math errors in the source on the first try. "
    "If validation fails, you will be given feedback to correct your extraction."
)
