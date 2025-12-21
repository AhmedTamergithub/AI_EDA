import fitz  # PyMuPDF
from langdetect import detect, DetectorFactory
from typing import Optional
import os
from dotenv import load_dotenv
import json
import time

# Load environment variables
load_dotenv()

# Set seed for consistent language detection results
DetectorFactory.seed = 0


def extract_pdf(pdf_path: str) -> tuple[str, int]:
    """
    Extract text content from a PDF file using PyMuPDF.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        tuple[str, int]: A tuple containing (extracted_text, num_pages)
        
    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        ValueError: If PDF is empty or corrupted
        Exception: For other PDF processing errors
    """
    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)
        num_pages = len(doc)
        
        # Check if PDF is empty (0 pages) [Requirement 4]
        if num_pages == 0:
            doc.close()
            raise ValueError("PDF file is empty (0 pages)")
        
        # Extract text from all pages
        text = ""
        for page_num in range(num_pages):
            page = doc[page_num]
            text += page.get_text()
        
        # Close the document
        doc.close()
        
        # Check if PDF has no extractable text (images, scanned without OCR, binary data) [Requirement 3]
        extracted_text = text.strip()
        if not extracted_text:
            raise ValueError(f"PDF has {num_pages} page(s) but no extractable text (might be scanned images, binary data, or images without OCR)")
        
        return extracted_text, num_pages #[Requirement 2]
    
    except FileNotFoundError:
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    except ValueError:
        raise
    except Exception as e:
        raise Exception(f"Error extracting PDF (possibly corrupted or unreadable): {str(e)}")


def detect_language(text: str) -> str:
    """
    Detect the language of the given text using langdetect.
    
    Args:
        text (str): Text to detect language for
        
    Returns:
        str: ISO 639-1 language code (e.g., 'en', 'fr', 'es')
        
    Raises:
        ValueError: If text is empty or language cannot be detected
    """
    try:
        if not text or not text.strip():
            raise ValueError("Text is empty or contains only whitespace")
        
        # Detect language
        language_code = detect(text)
        
        return language_code
    
    except Exception as e:
        raise ValueError(f"Error detecting language: {str(e)}")


def summarize_text(text: str, max_length: str = "medium") -> dict:
    """
    Summarize text using Gemini LLM.
    
    Args:
        text (str): Text to summarize
        max_length (str): Desired summary length - 'short', 'medium', or 'long'
        
    Returns:
        dict: Structured JSON containing:
            - summary (str): The generated summary
            - prompt (dict): Contains system_prompt and user_prompt sent to LLM
            - metadata (dict): Contains input_length, summary_length, model, timestamp
            
    Raises:
        ValueError: If text is empty or invalid
        Exception: For LLM API errors
    """
    try:
        # Validate input
        if not text or not text.strip():
            raise ValueError("Text is empty or contains only whitespace")
        
        # Define length guidelines
        length_guide = {
            "short": "in 2-3 sentences",
            "medium": "in 1-2 paragraphs",
            "long": "in 3-4 paragraphs with detailed key points"
        }
        
        # Create system and user prompts
        system_prompt = (
            "You are a professional text summarization assistant. "
            "Your task is to create clear, concise, and accurate summaries. "
            "Focus on the main ideas, key points, and essential information. "
            "Maintain objectivity and do not add information not present in the original text."
        )
        
        user_prompt = (
            f"Please summarize the following text {length_guide.get(max_length, length_guide['medium'])}:\n\n"
            f"{text}"
        )
        
        # Use Gemini API with retry logic
        from google import genai
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        client = genai.Client(api_key=api_key)
        
        # Retry logic for rate limiting
        max_retries = 3
        retry_delay = 30  # seconds
        
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_prompt,
                    config={
                        'system_instruction': system_prompt,
                        'temperature': 0.7,
                    }
                )
                
                summary = response.text.strip()
                model_name = "gemini-2.5-flash"
                break  # Success, exit retry loop
                
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                        print(f"Rate limit hit. Waiting {wait_time} seconds before retry {attempt + 2}/{max_retries}...")
                        time.sleep(wait_time)
                    else:
                        raise  # Max retries reached
                else:
                    raise  # Non-rate-limit error
        
        # Prepare structured response
        result = {
            "summary": summary,
            "prompt": {
                "system_prompt": system_prompt,
                "user_prompt": user_prompt
            },
            "metadata": {
                "input_length": len(text),
                "summary_length": len(summary),
                "model": model_name,
                "max_length": max_length,
                "timestamp": __import__('datetime').datetime.now().isoformat()
            }
        }
        
        return result
    
    except ValueError:
        raise
    except Exception as e:
        raise Exception(f"Error during text summarization: {str(e)}")


if __name__ == "__main__":
    # Set your PDF path here
    pdf_path = "/home/ahmedubuntu/AI_EDA/code/summarization_agent/resources/Ahmed_Tamer_Samir_CV.pdf"
    
    try:
        # Extract text using the extract_pdf function
        text, num_pages = extract_pdf(pdf_path)
        
        print(f"Number of pages: {num_pages}")
        print(f"\nExtracted text length: {len(text)} characters")
        
        # Detect language
        lang = detect_language(text)
        print(f"Detected language: {lang}")
        
        # Summarize text
        print("\n" + "="*80)
        print("SUMMARIZATION")
        print("="*80)
        summary_result = summarize_text(text, max_length="short")
        
        # Save to JSON file
        output_file = "summarize_text_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_result, f, indent=2, ensure_ascii=False)
        
        print(f"\nSummary saved to: {output_file}")
        print(f"Summary preview: {summary_result['summary'][:200]}...")
    except Exception as e:
        print(f"Error: {e}")
