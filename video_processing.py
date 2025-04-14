from moviepy import VideoFileClip
import os 
from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv 
from pydantic import BaseModel

load_dotenv(dotenv_path=".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def process_video(video_path):
    """
    Process the video file
    """
    filename, _ = os.path.splitext(video_path)
    clip = VideoFileClip(video_path)
    audioFilePath = f"{filename}.wav"
    clip.audio.write_audiofile(audioFilePath)
    transcription = transcribe_audio(audioFilePath)
    summary = summarizer(transcription)
    return summary

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

def transcribe_audio(audio_path):
    # convert to mono and 16kHz audio
    mono_audio_path = convert_to_mono_16k(audio_path)
    print(mono_audio_path)

    with open(mono_audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)

    print(transcript)
    return transcript.text

# to get formatted response from LLM
class SummarizerFormat(BaseModel):
    summary: str

def summarizer(text: str):
    data = client.beta.chat.completions.parse(
        messages=[
               {
                      "role": "system",
                      "content": """
                        You are given a transcription of a video file.
                        Your task is to summarize given transcription and provide a summary containing important points.
                        Return the summary content into markdown compatible syntax.

					return response in json format.
                        """,
               },
               { "role": "user", "content": f"{text}" },
        ],
        model="gpt-4o-mini",
        response_format=SummarizerFormat
	);

    return data.choices[0].message.content