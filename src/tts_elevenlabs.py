import os
import io
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from elevenlabs import play, stream
from elevenlabs.client import ElevenLabs
import sounddevice as sd
import soundfile as sf
import numpy as np

class ElevenLabsTTS:
    def __init__(self, api_key: str = None, voice_id: str = None, model: str = None):
        """
        Initialize the ElevenLabs Text-to-Speech engine.
        
        Args:
            api_key: ElevenLabs API key (if None, will try to load from .env)
            voice_id: Voice ID to use (if None, will use default)
            model: Model to use (if None, will use default)
        """
        # Load environment variables
        load_dotenv()
        
        # Set API key (parameter takes precedence over .env)
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        if not self.api_key:
            raise ValueError("ElevenLabs API key not provided. Set ELEVENLABS_API_KEY in .env file or pass as parameter.")
        
        # Initialize the client
        self.client = ElevenLabs(api_key=self.api_key)
        
        # Set voice and model - Use valid voice ID from the list
        self.voice_id = voice_id or 'uyVNoMrnUku1dZyVEXwD'  # George voice (from available list)
        self.model = model or 'eleven_flash_v2_5'  # Updated default model
        
        # Initialize audio settings
        self.sample_rate = 44100  # Default sample rate for ElevenLabs
    
    def list_voices(self) -> List[Dict[str, str]]:
        """
        List all available voices.
        
        Returns:
            List[Dict[str, str]]: List of available voices with id and name
        """
        try:
            all_voices = self.client.voices.get_all()
            return [{"id": v.voice_id, "name": v.name} for v in all_voices.voices]
        except Exception as e:
            print(f"Error listing voices: {e}")
            return []
            
    def list_models(self) -> List[Dict[str, Any]]:
        """
        List all available TTS models.
        
        Returns:
            List[Dict[str, Any]]: List of available models with their details
        """
        try:
            # ElevenLabs의 일반적으로 사용 가능한 모델들을 반환
            return [
                {
                    "model_id": "eleven_turbo_v2_5",
                    "name": "Eleven Turbo v2.5",
                    "description": "Fast, high-quality speech synthesis",
                    "languages": ["en", "ko", "ja", "zh"]
                },
                {
                    "model_id": "eleven_flash_v2_5",
                    "name": "Eleven Flash v2.5",
                    "description": "Ultra-fast speech synthesis",
                    "languages": ["en", "ko", "ja", "zh"]
                },
                {
                    "model_id": "eleven_multilingual_v2",
                    "name": "Eleven Multilingual v2",
                    "description": "Multilingual speech synthesis",
                    "languages": ["en", "ko", "ja", "zh", "es", "fr", "de"]
                }
            ]
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
    
    def text_to_speech(self, text: str, voice_id: str = None, model: str = None, 
                     save_path: str = None, stream_audio: bool = False) -> Optional[bytes]:
        """
        Convert text to speech and optionally save to file.
        
        Args:
            text: Text to convert to speech
            voice_id: Voice ID to use (if None, uses instance default)
            model: Model to use (if None, uses instance default)
            save_path: If provided, save audio to this file
            stream_audio: If True, stream the audio instead of generating it all at once
            
        Returns:
            Optional[bytes]: Audio data as bytes if successful, None otherwise
        """
        if not text.strip():
            print("No text provided for TTS")
            return None
            
        try:
            # Use provided voice_id/model or fall back to instance defaults
            current_voice = voice_id or self.voice_id
            current_model = model or self.model
            
            print(f"🔊 Generating speech with voice {current_voice} and model {current_model}...")
            
            if stream_audio:
                # Stream the audio using the new API
                audio_stream = self.client.text_to_speech.stream(
                    text=text,
                    voice_id=current_voice,
                    model_id=current_model
                )
                
                # If save path is provided, save the streamed audio
                if save_path:
                    os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True)
                    with open(save_path, 'wb') as f:
                        for chunk in audio_stream:
                            f.write(chunk)
                    print(f"Audio saved to {save_path}")
                    return None
                    
                # Convert stream to bytes for return
                audio_bytes = b''.join(audio_stream)
                return audio_bytes
            else:
                # Generate all at once using the new API
                audio = self.client.text_to_speech.convert(
                    text=text,
                    voice_id=current_voice,
                    model_id=current_model,
                    output_format="mp3_44100_128"
                )
                
                # Save to file if path is provided
                if save_path:
                    os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True)
                    with open(save_path, 'wb') as f:
                        for chunk in audio:
                            f.write(chunk)
                    print(f"Audio saved to {save_path}")
                    
                return audio
            
        except Exception as e:
            print(f"Error in text-to-speech conversion: {e}")
            return None
    
    def play_audio(self, audio_data: bytes):
        """
        Play audio data using ElevenLabs play function.
        
        Args:
            audio_data: Audio data to play (bytes from ElevenLabs)
        """
        if not audio_data:
            print("No audio data to play")
            return
            
        try:
            # Use ElevenLabs play function directly
            play(audio_data)
                
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def speak(self, text: str, voice_id: str = None, model: str = None, stream_audio: bool = False):
        """
        Convert text to speech and play it immediately.
        
        Args:
            text: Text to speak
            voice_id: Voice ID to use (if None, uses instance default)
            model: Model to use (if None, uses instance default)
            stream_audio: If True, stream the audio for playback
        """
        if stream_audio:
            # Stream the audio directly using the new API
            audio_stream = self.client.text_to_speech.stream(
                text=text,
                voice_id=voice_id or self.voice_id,
                model_id=model or self.model
            )
            stream(audio_stream)
        else:
            # Generate and play normally
            audio = self.text_to_speech(text, voice_id, model)
            if audio:
                self.play_audio(audio)

def test_elevenlabs():
    """Test function for ElevenLabs TTS"""
    print("Testing ElevenLabs TTS...")
    
    try:
        tts = ElevenLabsTTS()
        
        # List available voices
        print("\nAvailable voices (first 5):")
        voices = tts.list_voices()
        for i, voice in enumerate(voices[:5]):
            print(f"{i+1}. {voice['name']} (ID: {voice['id']})")
            
        # List available models
        print("\nAvailable models:")
        models = tts.list_models()
        for model in models:
            print(f"- {model['name']} ({model['model_id']})")
            if model['description']:
                print(f"  {model['description']}")
        
        # Test TTS
        test_text = "안녕하세요! 지선님. 저는 주인님이 만든 EevenLabs TTS 시스템 입니다."
        
        print(f"\nTest: {test_text}")
        
        # Generate and play with streaming
        print("Playing with streaming...")
        tts.speak(test_text, stream_audio=True)
        
        # Generate and save to file
        os.makedirs("output", exist_ok=True)
        output_path = os.path.join("output", "test_tts_output.mp3")
        audio_data = tts.text_to_speech(test_text, save_path=output_path)
        
        if os.path.exists(output_path):
            print(f"Audio saved to {os.path.abspath(output_path)}")
        
        print("\nAll tests completed!")
        
    except Exception as e:
        print(f"Error in test: {e}")

if __name__ == "__main__":
    test_elevenlabs()
