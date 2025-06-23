import os
import sys
import time
import argparse
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.stt_whisper import WhisperSTT
from src.gemma_client import GemmaClient
from src.tts_elevenlabs import ElevenLabsTTS

class VoiceAssistant:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the voice assistant with STT, LLM, and TTS components.
        
        Args:
            config: Optional configuration dictionary
        """
        # Load environment variables
        load_dotenv()
        
        # Default configuration
        self.config = {
            "stt_model": "base",  # Whisper model size (tiny, base, small, medium, large)
            "tts_voice_id": 'JBFqnCBsd6RMkjVDRZzb',  # George voice (valid voice ID)
            "tts_model": 'eleven_flash_v2_5',  # Updated TTS model
            "llm_model": "gemma-3-27b-it",  # LLM model
            "recording_duration": 5.0,  # Default recording duration in seconds
            "save_recordings": True,  # Whether to save audio recordings
            "verbose": True  # Print debug information
        }
        
        # Update with any provided config
        if config:
            self.config.update(config)
        
        # Initialize components
        self.stt = None
        self.llm = None
        self.tts = None
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize STT, LLM, and TTS components."""
        print("Initializing components...")
        
        try:
            # Initialize STT (Whisper)
            print("  - Initializing Whisper STT...")
            self.stt = WhisperSTT(model_size=self.config["stt_model"])
            
            # Initialize LLM (Gemma 3)
            print("  - Initializing Gemma LLM...")
            self.llm = GemmaClient(model=self.config["llm_model"])
            
            # Initialize TTS (ElevenLabs)
            print("  - Initializing ElevenLabs TTS...")
            self.tts = ElevenLabsTTS(
                voice_id=self.config["tts_voice_id"],
                model=self.config["tts_model"]
            )
            
            print("All components initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing components: {e}")
            raise
    
    def process_voice_input(self, audio_data=None, audio_path=None) -> Optional[str]:
        """
        Process voice input and return the assistant's response.
        
        Args:
            audio_data: Raw audio data (numpy array)
            audio_path: Path to audio file (alternative to audio_data)
            
        Returns:
            str: Assistant's response text, or None if there was an error
        """
        try:
            # Transcribe speech to text
            print("\n🔍 Transcribing speech...")
            text = self.stt.transcribe_audio(audio_data=audio_data, audio_path=audio_path)
            
            if not text:
                print("No speech detected or error in transcription.")
                return None
                
            print(f"🎤 You said: {text}")
            
            # Generate response using LLM
            print("\n🤖 Generating response...")
            response = self.llm.generate_response(
                prompt=text,
                temperature=0.7,
                max_output_tokens=200
            )
            
            if not response:
                print("No response generated.")
                return None
                
            print(f"\n💬 Assistant: {response}")
            
            # Convert response to speech
            print("\n🔊 Speaking...")
            self.tts.speak(response)
            
            return response
            
        except Exception as e:
            print(f"Error in voice processing: {e}")
            return None
    
    def start_interactive_mode(self):
        """Start an interactive voice conversation with the assistant."""
        print("\n" + "="*50)
        print("🎙️  Voice Assistant - Interactive Mode")
        print("  - Press Ctrl+C to exit")
        print("  - Speak when you see the 'Recording...' prompt")
        print("="*50 + "\n")
        
        try:
            while True:
                try:
                    # Record audio
                    print(f"\n🎤 Recording for {self.config['recording_duration']} seconds...")
                    audio_data = self.stt.record_audio(duration=self.config["recording_duration"])
                    
                    if audio_data is not None:
                        # Save recording if enabled
                        if self.config["save_recordings"]:
                            os.makedirs("recordings", exist_ok=True)
                            timestamp = time.strftime("%Y%m%d_%H%M%S")
                            filename = f"recording_{timestamp}.wav"
                            self.stt.save_audio(audio_data, filename)
                        
                        # Process the audio
                        self.process_voice_input(audio_data=audio_data)
                        
                except KeyboardInterrupt:
                    print("\nStopping recording...")
                    break
                except Exception as e:
                    print(f"Error in interactive mode: {e}")
                    continue
                    
        except KeyboardInterrupt:
            print("\nExiting interactive mode...")
        except Exception as e:
            print(f"Fatal error: {e}")
        finally:
            print("\nGoodbye! 👋")

def main():
    """Main entry point for the voice assistant."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Voice Assistant with STT, LLM, and TTS")
    parser.add_argument("--mode", type=str, default="interactive",
                       choices=["interactive", "file"],
                       help="Run mode: interactive (default) or process an audio file")
    parser.add_argument("--audio", type=str, help="Path to audio file to process (for file mode)")
    parser.add_argument("--stt-model", type=str, default="base",
                       help="Whisper model size (tiny, base, small, medium, large)")
    parser.add_argument("--duration", type=float, default=5.0,
                       help="Recording duration in seconds (for interactive mode)")
    parser.add_argument("--voice", type=str, help="Voice ID for TTS (default: Rachel)")
    parser.add_argument("--model", type=str, help="TTS model to use (default: eleven_multilingual_v2)")
    
    args = parser.parse_args()
    
    # Prepare config
    config = {
        "stt_model": args.stt_model,
        "recording_duration": args.duration,
    }
    
    if args.voice:
        config["tts_voice_id"] = args.voice
    if args.model:
        config["tts_model"] = args.model
    
    try:
        # Initialize the voice assistant
        assistant = VoiceAssistant(config=config)
        
        # Run in the selected mode
        if args.mode == "interactive":
            assistant.start_interactive_mode()
        elif args.mode == "file" and args.audio:
            if not os.path.exists(args.audio):
                print(f"Error: Audio file not found: {args.audio}")
                return
            print(f"Processing audio file: {args.audio}")
            assistant.process_voice_input(audio_path=args.audio)
        else:
            print("Please specify a valid mode and audio file path.")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
