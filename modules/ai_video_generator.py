"""
AI Text Generation and Video Creation Module
Handles OpenAI API integration for text generation and Pixabay API for video creation
"""
import os
import requests
import json
from typing import Optional, Tuple
import tempfile
import subprocess


def generate_text_with_openai(api_key: str, prompt: str) -> Tuple[bool, str]:
    """
    Generate text using OpenAI API.
    
    Args:
        api_key: OpenAI API key
        prompt: The prompt to generate text from
        
    Returns:
        Tuple of (success: bool, result: str)
    """
    try:
        if not api_key or not api_key.startswith('sk-'):
            return False, "Invalid OpenAI API key. Please provide a valid key starting with 'sk-'"
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant that generates motivational and inspirational content.'},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 150,
            'temperature': 0.7
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result['choices'][0]['message']['content'].strip()
            return True, generated_text
        else:
            error_msg = f"OpenAI API error: {response.status_code} - {response.text}"
            return False, error_msg
            
    except Exception as e:
        return False, f"Error generating text: {str(e)}"


def search_pixabay_videos(api_key: str, query: str, per_page: int = 10) -> Tuple[bool, list]:
    """
    Search for videos on Pixabay.
    
    Args:
        api_key: Pixabay API key
        query: Search query
        per_page: Number of results to return
        
    Returns:
        Tuple of (success: bool, videos: list)
    """
    try:
        if not api_key:
            return False, []
        
        url = "https://pixabay.com/api/videos/"
        params = {
            'key': api_key,
            'q': query,
            'per_page': per_page,
            'video_type': 'all'
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            videos = data.get('hits', [])
            return True, videos
        else:
            return False, []
            
    except Exception as e:
        print(f"Error searching Pixabay: {str(e)}")
        return False, []


def download_video(video_url: str, output_path: str) -> bool:
    """
    Download a video from URL.
    
    Args:
        video_url: URL of the video to download
        output_path: Path to save the video
        
    Returns:
        bool: Success status
    """
    try:
        response = requests.get(video_url, stream=True, timeout=60)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        return False
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return False


def create_video_with_audio(video_path: str, audio_path: str, output_path: str, target_duration: int = 30) -> Tuple[bool, str]:
    """
    Create a video by combining video footage with audio narration.
    Uses ffmpeg to merge video and audio.
    
    Args:
        video_path: Path to the video file
        audio_path: Path to the audio file
        output_path: Path to save the output video
        target_duration: Target duration in seconds
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Check if ffmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False, "FFmpeg is not installed. Please install FFmpeg to create videos."
        
        # Get audio duration
        probe_cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            audio_path
        ]
        
        try:
            result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
            audio_duration = float(result.stdout.strip())
        except:
            audio_duration = target_duration
        
        # Create video with audio
        # Loop video if needed, trim to audio duration, add audio
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-stream_loop', '-1',  # Loop video
            '-i', video_path,
            '-i', audio_path,
            '-t', str(audio_duration),  # Duration = audio length
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-shortest',
            '-pix_fmt', 'yuv420p',
            output_path
        ]
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_path):
            return True, f"Video created successfully: {output_path}"
        else:
            error_msg = result.stderr if result.stderr else "Unknown error"
            return False, f"FFmpeg error: {error_msg}"
            
    except Exception as e:
        return False, f"Error creating video: {str(e)}"


def create_motivational_video(
    text: str,
    audio_path: str,
    pixabay_api_key: str,
    search_query: str = "motivation success",
    target_duration: int = 30,
    output_dir: str = "output"
) -> Tuple[bool, str, str]:
    """
    Create a complete motivational video with narration.
    
    Args:
        text: The text being narrated
        audio_path: Path to the generated audio file
        pixabay_api_key: Pixabay API key
        search_query: Search query for videos
        target_duration: Target video duration
        output_dir: Directory to save output files
        
    Returns:
        Tuple of (success: bool, video_path: str, message: str)
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Search for videos on Pixabay
        success, videos = search_pixabay_videos(pixabay_api_key, search_query, per_page=5)
        
        if not success or not videos:
            return False, "", "No videos found on Pixabay. Please check your API key and search query."
        
        # Get the first video (you can randomize this)
        video = videos[0]
        
        # Get the best quality video URL
        video_files = video.get('videos', {})
        video_url = None
        
        # Try to get medium or large quality
        for quality in ['medium', 'large', 'small']:
            if quality in video_files:
                video_url = video_files[quality]['url']
                break
        
        if not video_url:
            return False, "", "Could not find suitable video quality"
        
        # Download the video
        temp_video_path = os.path.join(tempfile.gettempdir(), f"pixabay_video_{os.getpid()}.mp4")
        
        print(f"Downloading video from Pixabay...")
        if not download_video(video_url, temp_video_path):
            return False, "", "Failed to download video from Pixabay"
        
        # Create output video path
        output_video_path = os.path.join(output_dir, f"video_{os.path.basename(audio_path).replace('.wav', '.mp4')}")
        
        # Combine video and audio
        print(f"Creating video with audio narration...")
        success, message = create_video_with_audio(
            temp_video_path,
            audio_path,
            output_video_path,
            target_duration
        )
        
        # Clean up temp video
        try:
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
        except:
            pass
        
        if success:
            return True, output_video_path, "Video created successfully!"
        else:
            return False, "", message
            
    except Exception as e:
        return False, "", f"Error creating motivational video: {str(e)}"
