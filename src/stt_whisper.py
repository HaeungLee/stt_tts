import os
import wave
import time
import numpy as np
import sounddevice as sd
import whisper
from datetime import datetime
from typing import Optional, Tuple

class WhisperSTT:
    def __init__(self, model_size: str = "base", device_id: int = None):
        """
        Initialize the Whisper speech-to-text engine.
        
        Args:
            model_size: Size of the Whisper model (tiny, base, small, medium, large)
            device_id: Audio input device ID (None for auto-detection)
        """
        self.model = whisper.load_model(model_size)
        self.sample_rate = 16000  # Whisper's default sample rate
        self.channels = 1         # Mono audio
        self.chunk = 1024         # Number of frames per buffer
        self.device_id = device_id
        
        # Auto-detect working audio device if not specified
        if self.device_id is None:
            self.device_id = self._find_working_device()
    
    def _find_working_device(self) -> Optional[int]:
        """
        Find a working audio input device.
        
        Returns:
            int: Device ID of working device, or None if none found
        """
        try:
            devices = sd.query_devices()
            print("🔍 오디오 입력 장치를 자동 탐지 중...")
            
            # Test devices in order of preference
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    try:
                        # Quick test recording
                        test_audio = sd.rec(
                            int(0.1 * self.sample_rate),  # 0.1 second test
                            samplerate=self.sample_rate,
                            channels=self.channels,
                            dtype='float32',
                            device=i
                        )
                        sd.wait()
                        
                        print(f"✅ 작동하는 장치 발견: {device['name']} (ID: {i})")
                        return i
                        
                    except Exception as e:
                        continue
            
            print("❌ 작동하는 오디오 입력 장치를 찾을 수 없습니다.")
            print("💡 해결 방법:")
            print("   1. Windows 설정 > 개인정보 > 마이크에서 앱 액세스 허용")
            print("   2. 마이크가 연결되어 있는지 확인")
            print("   3. 다른 앱이 마이크를 사용 중인지 확인")
            return None
            
        except Exception as e:
            print(f"장치 탐지 중 오류: {e}")
            return None
        
    def record_audio(self, duration: float = 5.0) -> np.ndarray:
        """
        Record audio from the microphone.
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            numpy.ndarray: Recorded audio data
        """
        if self.device_id is None:
            raise RuntimeError("❌ 작동하는 오디오 입력 장치가 없습니다. Windows 마이크 권한을 확인하세요.")
        
        print(f"\n🎤 Recording for {duration} seconds... (Press Ctrl+C to stop early)")
        print(f"   사용 중인 장치 ID: {self.device_id}")
        
        try:
            audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype='float32',
                device=self.device_id
            )
            sd.wait()  # Wait until recording is finished
            
            print("✅ Recording completed")
            return audio_data.flatten()
            
        except Exception as e:
            print(f"Error during recording: {e}")
            return None
    
    def transcribe_audio(self, audio_data: np.ndarray = None, audio_path: str = None) -> str:
        """
        Transcribe audio data or audio file to text.
        
        Args:
            audio_data: Audio data as numpy array
            audio_path: Path to audio file (alternative to audio_data)
            
        Returns:
            str: Transcribed text
        """
        try:
            if audio_path and os.path.exists(audio_path):
                # Load audio from file
                result = self.model.transcribe(audio_path, language='ko')
            elif audio_data is not None:
                # Use provided audio data
                result = self.model.transcribe(audio_data.astype(np.float32), language='ko')
            else:
                raise ValueError("Either audio_data or audio_path must be provided")
                
            return result["text"].strip()
            
        except Exception as e:
            print(f"Error during transcription: {e}")
            return ""
    
    def save_audio(self, audio_data: np.ndarray, filename: str = None) -> str:
        """
        Save audio data to a WAV file.
        
        Args:
            audio_data: Audio data to save
            filename: Output filename (default: timestamp)
            
        Returns:
            str: Path to the saved audio file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
            
        # Ensure the directory exists
        os.makedirs("recordings", exist_ok=True)
        filepath = os.path.join("recordings", filename)
        
        try:
            with wave.open(filepath, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(self.sample_rate)
                wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())
                
            return filepath
            
        except Exception as e:
            print(f"Error saving audio: {e}")
            return ""

def test_whisper():
    """Test function for Whisper STT"""
    print("Testing Whisper STT...")
    stt = WhisperSTT(model_size="base")
    
    # Record 5 seconds of audio
    print("Speak now...")
    audio_data = stt.record_audio(duration=5.0)
    
    if audio_data is not None:
        # Save the recording
        filepath = stt.save_audio(audio_data)
        print(f"Audio saved to {filepath}")
        
        # Transcribe the recording
        text = stt.transcribe_audio(audio_data=audio_data)
        print(f"\nTranscription: {text}")

if __name__ == "__main__":
    test_whisper()
