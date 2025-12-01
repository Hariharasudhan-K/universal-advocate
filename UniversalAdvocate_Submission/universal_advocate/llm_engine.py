import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in .env or pass it to the constructor.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp') # Using Flash for speed as requested

    def query(self, prompt: str) -> str:
        """
        Sends a prompt to the Gemini model and returns the text response.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error querying Gemini: {str(e)}"

# Singleton instance for easy import if needed, but classes can instantiate their own
def get_llm_engine(api_key=None):
    return LLMEngine(api_key)
