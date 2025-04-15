from moviepy import VideoFileClip
import os 
import json
from google import genai
from google.genai import types
import env

gemini = genai.Client(api_key=env.GEMINI_API_KEY)

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
        summary = summarizer(transcription)
        # cleanup files
        cleanup([video_path, audioFilePath])
        return summary
    except Exception as e:
        print(e)
        return None

def transcribe(audio_path):
    audio_file = gemini.files.upload(file=audio_path)
    prompt = 'Generate a transcript of the speech.'

    response = gemini.models.generate_content(
        model='gemini-2.0-flash',
        contents=[prompt, audio_file]
    )
    return response.text

def summarizer(text: str):
    try:
        response = gemini.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="""
                You are given a transcription of a audio file.
                Your task is to summarize given transcription and provide a summary containing important points.
                Return the summary content into markdown compatible syntax that includes:
                    - summary of the content
                    - important points (if any)
                
                Don't give intermediate steps or your descibing, give me only required content.
                ---
                Use this JSON schema:

                Summary= {'summary': str, 'important_points': List[str]}
                Return: list[Summary]
            """),
        contents=text
        )
        clean_json_str = response.text.strip('```json')

        data = json.loads(clean_json_str)
        print(data)
        return data[0]
    except Exception as e:
        print(e)
        return None
    
def cleanup(files: list[str]):
    for path in files:
        os.unlink(path)