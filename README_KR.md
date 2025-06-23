# 음성 어시스턴트 (STT, LLM, TTS 통합)

Whisper를 사용한 음성 인식, Google의 Gemma 3를 활용한 자연어 처리, ElevenLabs의 고품질 음성 합성 기능을 갖춘 음성 어시스턴트입니다.

## 주요 기능

- 🎙️ Whisper 기반 실시간 음성 인식
- 🧠 Google Gemma 3를 활용한 자연어 처리
- 🔊 ElevenLabs의 고품질 음성 합성
- 💬 대화형 음성 모드 지원
- 🎧 오디오 파일 처리 기능
- 🎚️ 모델 및 음성 설정 커스터마이징 가능

## 필수 조건

- Python 3.8 이상
- FFmpeg (Whisper 사용을 위해 필요)
- Google AI API 키 (Gemma 3 사용을 위해 필요)
- ElevenLabs API 키 (TTS 사용을 위해 필요)

## 설치 방법

1. 저장소를 클론합니다:
   ```bash
   git clone <repository-url>
   cd stt_tts
   ```

python 3.10
2. 필요한 패키지들을 설치합니다:
   ```bash
   pip install -r requirements.txt
   ```

3. FFmpeg을 설치합니다:
   - Windows: [FFmpeg 공식 웹사이트](https://ffmpeg.org/download.html)에서 다운로드 후 PATH에 추가
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg`

4. 프로젝트 루트에 `.env` 파일을 생성하고 API 키를 추가합니다:
   ```
   # Google AI API 키 (Gemma 3 사용을 위해 필요)
   GOOGLE_API_KEY=your_google_api_key_here
   
   # ElevenLabs API 키 (TTS 사용을 위해 필요)
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   
   # 선택사항: 음성 및 모델 커스터마이징
   # VOICE_ID=21m00Tcm4TlvDq8ikWAM  # 기본값: Rachel 음성
   # MODEL=eleven_multilingual_v2   # TTS 모델
   ```

## 사용 방법

### 대화형 모드
대화형 음성 모드로 실행:
```bash
python src/main.py --mode interactive
```

### 오디오 파일 처리
미리 녹음된 오디오 파일 처리:
```bash
python src/main.py --mode file --audio path/to/your/audio.wav
```

### 명령줄 옵션
```
--mode MODE           실행 모드: interactive 또는 file (기본값: interactive)
--audio AUDIO         처리할 오디오 파일 경로 (file 모드에서 사용)
--stt-model MODEL     Whisper 모델 크기 (tiny, base, small, medium, large) (기본값: base)
--duration DURATION   녹음 시간(초) (대화형 모드에서 사용) (기본값: 5.0)
--voice VOICE_ID      TTS에 사용할 음성 ID (기본값: Rachel 음성)
--model TTS_MODEL     사용할 TTS 모델 (기본값: eleven_multilingual_v2)
```

## 프로젝트 구조

```
stt_tts/
│
├── src/
│   ├── __init__.py
│   ├── stt_whisper.py    # Whisper를 사용한 음성 인식
│   ├── gemma_client.py   # Gemma 3 API 클라이언트
│   ├── tts_elevenlabs.py # ElevenLabs를 사용한 음성 합성
│   └── main.py           # 메인 애플리케이션
│
├── config/             # 설정 파일 디렉토리
├── recordings/          # 녹음 파일 저장 디렉토리
├── output/              # 생성된 출력 파일 저장 디렉토리
│
├── .env.example        # 환경 변수 예시 파일
├── requirements.txt     # Python 의존성 목록
└── README_KR.md        # 이 파일 (한국어 버전)
```

## 커스터마이징

### 음성 변경
`.env` 파일의 `VOICE_ID`를 수정하여 TTS 음성을 변경할 수 있습니다. 사용 가능한 음성 목록을 보려면 다음 명령을 실행하세요:
```bash
python -c "from src.tts_elevenlabs import ElevenLabsTTS; tts = ElevenLabsTTS(); print('사용 가능한 음성:'); [print(f'{i+1}. {v[\"name\"]} (ID: {v[\"id\"]}') for i, v in enumerate(tts.list_voices()[:10])]"
```

### 다른 모델 사용하기
- **STT 모델**: `--stt-model` 매개변수 변경 (tiny, base, small, medium, large)
- **LLM 모델**: `gemma_client.py`의 `model` 매개변수 수정
- **TTS 모델**: `.env` 파일의 `MODEL` 값 변경

## 문제 해결

### 일반적인 문제
1. **Whisper가 작동하지 않음**: FFmpeg이 설치되어 있고 시스템 PATH에 추가되었는지 확인하세요
2. **API 오류**: API 키가 정확한지, 크레딧이 충분한지 확인하세요
3. **오디오 장치 문제**: 마이크와 스피커 설정을 확인하세요

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 참고 자료

- [OpenAI Whisper](https://github.com/openai/whisper) - 음성 인식을 위해 사용
- [Google AI](https://ai.google.dev/) - Gemma 3 모델 제공
- [ElevenLabs](https://elevenlabs.io/) - 고품질 음성 합성 제공
