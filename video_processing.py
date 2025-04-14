from moviepy import VideoFileClip
import os 
from pydub import AudioSegment
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def process_video(video_path):
    """
    Process the video file
    """
    filename, _ = os.path.splitext(video_path)
    clip = VideoFileClip(video_path)
    audioFilePath = f"{filename}.wav"
    clip.audio.write_audiofile(audioFilePath)
    print(audioFilePath)
    transcribe_audio(audioFilePath)

def convert_to_mono_16k(audio_file_path, output_dir="tmp"):
    """Converts audio to mono and 16kHz, returns the path to the converted audio."""
    sound = AudioSegment.from_file(audio_file_path)
    sound = sound.set_channels(1)  # Mono
    sound = sound.set_frame_rate(16000)  # 16kHz

    # Generate a unique filename for the mono version
    converted_file_name = f"{audio_file_path.split('/')[-1]}"
    converted_file_path = os.path.join(output_dir, converted_file_name)

    # Export the converted audio file
    sound.export(converted_file_path, format="wav")
    return converted_file_path

def transcribe_audio(path):
    with open(path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

    print(transcript)
    return transcript.text

def summarizer(text: str):
    pass