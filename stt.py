import whisper
import os

print("Loading Whisper model. This might take a few seconds...")
model = whisper.load_model("base")
print("Whisper model loaded successfully.")

def transcribe_audio(file_path: str) -> str:
    """
    This function takes the path to an audio file,
    processes it using the Whisper model,
    and returns the transcribed text.
    """

    print("Transcription started.")
    print(f"Audio file to transcribe: {file_path}")

    if not os.path.exists(file_path):
        print("Error: Audio file does not exist at the specified path.")
        return ""

    try:
        # Performing transcription using Whisper
        result = model.transcribe(file_path)
        
        # Extracting and returning the transcribed text
        transcribed_text = result["text"]
        print("Transcription completed successfully.")
        print(f"Transcribed Text: {transcribed_text}")
        return transcribed_text

    except Exception as e:
        print("An error occurred while transcribing the audio.")
        print("Error:", e)
        return ""
