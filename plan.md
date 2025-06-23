# 음성 대화형 AI 어시스턴트 프로젝트 계획

## 1. 프로젝트 개요
- **목표**: 음성 입력(STT) → LLM 처리 → 음성 출력(TTS) 파이프라인 구축
- **주요 기술 스택**:
  - STT: Whisper (오프라인 음성 인식)
  - LLM: Google Gemma 3 27B (API 연동)
  - TTS: ElevenLabs (고품질 음성 합성)

## 2. 프로젝트 구조
```
stt_tts/
│
├── src/
│   ├── __init__.py
│   ├── stt_whisper.py    # 음성 인식 모듈
│   ├── gemma_client.py   # Gemma 3 API 연동
│   ├── tts_elevenlabs.py  # 음성 합성 모듈 (ElevenLabs)
│   └── main.py           # 메인 애플리케이션
│
├── config/
│   └── config.yaml      # API 키 및 설정 파일
│
├── requirements.txt     # 의존성 목록
└── README.md            # 프로젝트 설명
```

## 3. 상세 구현 계획

### 3.1 STT (Whisper)
- **기능**:
  - 실시간 마이크 입력 또는 오디오 파일 입력 처리
  - 한국어 음성을 텍스트로 변환
- **의존성**: `openai-whisper`, `sounddevice`, `numpy`, `elevenlabs`
- **주요 함수**:
  ```python
  def transcribe_audio(audio_path=None, use_mic=True):
      """음성 파일이나 마이크 입력을 텍스트로 변환"""
      pass
  ```

### 3.2 Gemma 3 27B API 클라이언트
- **기능**:
  - Google AI Studio API 연동
  - 프롬프트 엔지니어링을 통한 응답 최적화
- **의존성**: `google-genai` (Google의 새로운 Gen AI SDK)
- **주요 함수**:
  ```python
  def generate_response(prompt, max_tokens=150):
      """Gemma 3 모델에 프롬프트 전달 및 응답 생성
      
      Note: Google의 새로운 Gen AI SDK(google-genai) 사용
      import는 `from google import genai` 형태로 진행
      """
      pass
  ```

### 3.3 TTS (ElevenLabs)
- **기능**:
  - 생성된 텍스트를 고품질 음성으로 변환
  - 다양한 목소리 스타일 지원
  - 실시간 스트리밍 재생
- **의존성**: `elevenlabs`
- **주요 함수**:
  ```python
  def text_to_speech(text, voice_id='default', model='eleven_multilingual_v2'):
      """
      텍스트를 ElevenLabs를 사용해 음성으로 변환하여 재생
      
      Args:
          text (str): 변환할 텍스트
          voice_id (str): 사용할 음성 ID (기본값: 기본 음성)
          model (str): 사용할 TTS 모델 (기본값: 다국어 지원 모델)
      """
      pass
  ```

### 3.4 메인 애플리케이션
- **기능**:
  - 전체 파이프라인 통합
  - 사용자 인터페이스 제공 (CLI)
  - 에러 처리 및 로깅

## 4. 개발 일정 (예상)
1. **1일차**: 환경 설정 및 STT 모듈 개발
2. **2일차**: Gemma 3 API 연동
3. **3일차**: TTS 모듈 개발 및 통합
4. **4일차**: 테스트 및 최적화

## 5. 필요한 API 키 및 설정
1. **Google AI Studio API 키** (Gemma 3 사용을 위해 필요)
2. **ElevenLabs API 키** (TTS 서비스 사용을 위해 필요)
3. **오디오 장치 설정** (마이크/스피커)

## 6. 실행 방법
```bash
# 의존성 설치
pip install -r requirements.txt

# 애플리케이션 실행
python src/main.py
```

## 7. 향후 개선 사항
- 대화 컨텍스트 유지 기능 추가
- 더 자연스러운 대화를 위한 프롬프트 최적화
- GUI 애플리케이션으로 확장
- 오프라인 모드 지원 (경량 모델 사용)

## 8. 제한 사항
- Gemma 3 API 사용량에 따른 비용 발생 가능
- 인터넷 연결 필요 (API 호출을 위해)
- 대기 시간이 발생할 수 있음 (API 응답 시간에 따라)
