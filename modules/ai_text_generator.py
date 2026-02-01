"""
AI Text Generation for Batch TTS
Uses OpenAI API to generate content for batch text-to-speech
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_openai_client():
    """Get OpenAI client with API key from environment variable."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Please set it in the .env file or as an environment variable.")
    return OpenAI(api_key=api_key)


def calculate_words_for_duration(duration_value, duration_unit):
    """
    Calculate approximate number of words needed for desired audio duration.
    
    Args:
        duration_value: Numeric value (e.g., 8)
        duration_unit: "minutes" or "seconds"
    
    Returns:
        Approximate word count needed
    """
    # Standard speech rate: ~150 words per minute
    WORDS_PER_MINUTE = 150
    
    if duration_unit == "minutes":
        total_minutes = duration_value
    else:  # seconds
        total_minutes = duration_value / 60
    
    words_needed = int(total_minutes * WORDS_PER_MINUTE)
    return max(words_needed, 10)  # Minimum 10 words


def generate_single_text(topic, duration_value, duration_unit, variation_number=1):
    """
    Generate a single text based on topic and duration.
    
    Args:
        topic: The topic/theme for the content
        duration_value: Numeric duration value
        duration_unit: "minutes" or "seconds"
        variation_number: Number to ensure unique variations
    
    Returns:
        Generated text string
    """
    try:
        client = get_openai_client()
        words_needed = calculate_words_for_duration(duration_value, duration_unit)
        
        # Create a unique prompt for each variation
        system_prompt = f"""You are a professional content creator. Your task is to CREATE content in the style/genre specified by the user.

IMPORTANT: 
- If the user says "motivational speeches", you should WRITE an actual motivational speech, not talk ABOUT motivational speeches
- If the user says "bedtime stories", you should WRITE an actual bedtime story, not talk ABOUT bedtime stories
- If the user says "product descriptions", you should WRITE actual product descriptions, not talk ABOUT product descriptions

Generate natural, conversational text suitable for text-to-speech.
The content should be approximately {words_needed} words long.
Make it sound natural when spoken aloud - use conversational language, avoid complex formatting."""

        user_prompt = f"""CREATE content in this style/genre: {topic}

Requirements:
- Approximately {words_needed} words
- Write ACTUAL content in that style/genre (don't talk about it, BE it)
- Natural, conversational tone suitable for voice narration
- Variation #{variation_number} (make it completely unique and different from other variations)
- No special formatting, just plain text
- Engaging and well-structured
- Start directly with the content (no meta-commentary)

Generate the content now:"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.9,  # Higher temperature for more variation
            max_tokens=words_needed * 2  # Allow some buffer
        )
        
        generated_text = response.choices[0].message.content.strip()
        return generated_text
        
    except Exception as e:
        return f"Error generating text: {str(e)}"


def generate_all_texts(topic, duration_value, duration_unit, num_texts=100, progress_callback=None):
    """
    Generate multiple unique texts based on topic and duration.
    
    Args:
        topic: The topic/theme for all content
        duration_value: Numeric duration value
        duration_unit: "minutes" or "seconds"
        num_texts: Number of texts to generate (default 100)
        progress_callback: Optional callback function(current, total, text) for progress updates
    
    Yields:
        (index, generated_text, status_message)
    """
    try:
        client = get_openai_client()
        words_needed = calculate_words_for_duration(duration_value, duration_unit)
        
        for i in range(num_texts):
            try:
                # Generate unique text for this field
                text = generate_single_text(topic, duration_value, duration_unit, variation_number=i+1)
                
                status = f"Generated text {i+1}/{num_texts}"
                yield i, text, status
                
            except Exception as e:
                error_text = f"Error: {str(e)}"
                yield i, error_text, f"Failed to generate text {i+1}/{num_texts}"
                
    except Exception as e:
        yield 0, f"Error: {str(e)}", "Failed to initialize AI text generation"
