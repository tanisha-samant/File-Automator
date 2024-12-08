import time
import logging
from groq import Groq

# Configure logging
logging.basicConfig(level=logging.INFO)

MODEL_NAME = "llama-3.2-3b-preview"
MIXTRAL_API_KEY = "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"  # Replace with your actual API key

client = Groq(api_key=MIXTRAL_API_KEY)

def rate_limited_request():
    """Simulate rate-limiting handling with reduced wait time."""
    time.sleep(1)  # Reduced from 5 to 1 second

def send_mixtral_request(messages, max_attempts=3, max_tokens=4096):
    """
    Send a request to the Mixtral API with improved error handling and retry logic.
    
    :param messages: List of messages for the Mixtral API.
    :param max_attempts: Max number of retries in case of errors.
    :param max_tokens: Maximum tokens for the response.
    :return: The content of the completion response or None if an error occurs.
    """
    # Truncate input to prevent overwhelming the model
    if len(messages[1]['content']) > 50000:
        messages[1]['content'] = messages[1]['content'][:50000]
        logging.warning("Input text truncated to 50,000 characters")

    for attempt in range(max_attempts):
        try:
            rate_limited_request()
            
            # Make the request using the Groq client
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.5,  # Balanced creativity
                max_tokens=max_tokens,  # Configurable max tokens
                top_p=0.9,
                stream=False,
                stop=None
            )
            
            # Extract and validate content from the response
            response_content = completion.choices[0].message.content
            
            if response_content and len(response_content.strip()) > 0:
                return response_content
            
            logging.warning(f"Empty response on attempt {attempt + 1}")
        
        except Exception as e:
            logging.error(f"Mixtral Request Error (Attempt {attempt + 1}): {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
    
    return None

def classify_document(text):
    """Classify document with improved error handling."""
    # Truncate extremely large texts
    if len(text) > 50000:
        text = text[:50000]
        logging.warning("Text truncated for classification")

    messages = [
        {"role": "system", "content": "You are an AI assistant that classifies documents based on their content."},
        {"role": "user", "content": f"Classify the following document in one or two words:\n\n{text}"}
    ]
    return send_mixtral_request(messages)

def summarize_and_extract_details(text, language="English"):
    """Advanced document summarization with chunking for large documents.
    
    :param text: Full document text
    :param language: Language of summarization
    :return: Comprehensive summary
    """
    # Logging and initial checks
    logging.info(f"Starting document summarization. Total text length: {len(text)} characters")

    # If text is very large, implement chunking strategy
    def chunk_text(text, chunk_size=20000, overlap=2000):
        """
        Split text into manageable chunks with overlap to maintain context.
        
        :param text: Full text to be chunked
        :param chunk_size: Maximum size of each chunk
        :param overlap: Number of characters to overlap between chunks
        :return: List of text chunks
        """
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        return chunks

    # Chunk the text if it's too large
    if len(text) > 30000:
        logging.info("Large document detected. Implementing chunk-based summarization.")
        text_chunks = chunk_text(text)
        
        # Summarize each chunk
        chunk_summaries = []
        for i, chunk in enumerate(text_chunks, 1):
            logging.info(f"Processing chunk {i}/{len(text_chunks)}")
            
            chunk_summary_messages = [
                {"role": "system", "content": f"You are an AI assistant summarizing part of a larger document in {language}. Provide a concise summary focusing on key points."},
                {"role": "user", "content": f"Summarize this document chunk within 300 words:\n\n{chunk}"}
            ]
            
            chunk_summary = send_mixtral_request(chunk_summary_messages)
            if chunk_summary:
                chunk_summaries.append(chunk_summary)
            
            # Prevent overwhelming the API
            time.sleep(1)
        
        # Combine chunk summaries into a comprehensive summary
        combined_summary_messages = [
            {"role": "system", "content": f"You are an AI assistant creating a comprehensive summary in {language}. Merge the following chunk summaries into a coherent, concise overview."},
            {"role": "user", "content": "Chunk Summaries:\n" + "\n\n".join(chunk_summaries)}
        ]
        
        final_summary = send_mixtral_request(combined_summary_messages)
        
        return final_summary or "Could not generate a complete summary."
    
    # For smaller documents, use standard summarization
    else:
        logging.info("Standard summarization for smaller document")
        messages = [
            {"role": "system", "content": f"Summarize this document in {language} within 300 words, capturing the most important information."},
            {"role": "user", "content": text}
        ]
        
        summary = send_mixtral_request(messages)
        return summary or "Could not generate a summary."

def translate_text(text, target_language):
    """Translate text to the specified target language."""
    if len(text) > 20000:
        text = text[:20000]
        logging.warning("Text truncated for translation")

    messages = [
        {"role": "system", "content": "You are an AI translator that translates text accurately."},
        {"role": "user", "content": f"Translate the following text to {target_language}:\n\n{text}"}
    ]
    
    try:
        translated_text = send_mixtral_request(messages)
        if not translated_text:
            logging.error("Translation request returned empty response.")
            return None
        return translated_text
    except Exception as e:
        logging.error(f"Translation error: {e}")
        return None

def enhance_ocr_with_context(text):
    """
    Enhance OCR text by cleaning up errors and improving readability.

    :param text: OCR-extracted text to be enhanced
    :return: Enhanced text with improved readability
    """
    # Check if input text is empty
    if not text:
        logging.warning("Empty text provided for OCR enhancement")
        return ""

    # Truncate extremely large texts
    if len(text) > 50000:
        text = text[:50000]
        logging.warning("Text truncated for OCR enhancement")

    messages = [
        {"role": "system", "content": "You are an AI assistant that improves OCR-extracted text by correcting errors, fixing formatting, and enhancing readability."},
        {"role": "user", "content": f"Enhance the readability of this OCR-extracted text:\n\n{text}"}
    ]
    
    enhanced_text = send_mixtral_request(messages)
    
    # Additional fallback if no enhancement is returned
    if not enhanced_text:
        logging.warning("OCR enhancement failed. Returning original text.")
        return text
    
    return enhanced_text