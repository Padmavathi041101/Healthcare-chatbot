import whisper

model_size = "tiny.en"  
loaded_model = whisper.load_model(model_size)

# Simplified function for transcription that only accepts audio files
def whisper_transcript(audio_file):
    # Directly use the provided audio file for transcription
    options = whisper.DecodingOptions(without_timestamps=True)
    transcript = loaded_model.transcribe(audio_file, language="english")
    return transcript["text"]
