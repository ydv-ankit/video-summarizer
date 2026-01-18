from moviepy import VideoFileClip
import os 
from openai import OpenAI
import env
from pydub import AudioSegment

openai_client = OpenAI(api_key=env.OPENAI_API_KEY)

def process_video(video_path):
    """
    Process the video file
    """
    try:
        filename, _ = os.path.splitext(video_path)
        # extract audio
        clip = VideoFileClip(video_path)
        audioFilePath = f"{filename}.wav"
        clip.audio.write_audiofile(audioFilePath)
        # get transcription from audio
        transcription = transcribe(audio_path=audioFilePath)
        # summarize transcripted text
        print(transcription)
        summary = summarizer(transcription)
        # cleanup files
        return summary
    except Exception as e:
        print(e)
        return None
    
def convert_to_mono_16k(audio_file_path, output_dir="tmp"):
    """Converts audio to mono and 16kHz, returns the path to the converted audio."""
    sound = AudioSegment.from_file(audio_file_path)
    os.unlink(audio_file_path)
    sound = sound.set_channels(1)  # Mono
    sound = sound.set_frame_rate(16000)  # 16kHz

    converted_file_name = f"{audio_file_path.split('/')[-1]}"
    converted_file_path = os.path.join(output_dir, converted_file_name)

    # Export the converted audio file
    sound.export(converted_file_path, format="wav")
    return converted_file_path

def transcribe(audio_path):
    mono_audio = convert_to_mono_16k(audio_path)
    
    with open(mono_audio, "rb") as audio_file:
        transcript = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    return transcript

def summarizer(text: str):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are given a transcription of an audio file.
                    Your task is to summarize the given transcription and provide a summary containing important points.
                    Return the summary content in markdown compatible syntax that includes:
                        - summary of the content
                        - important points (if any)
                        - any other relevant information (if any)

                    Translate the summary to english language.
                    Don't give intermediate steps or your describing, give me only required content."""
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        summary_text = response.choices[0].message.content
        print(summary_text)
        return summary_text
    except Exception as e:
        print(e)
        return None
