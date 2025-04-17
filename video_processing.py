from moviepy import VideoFileClip
import os 
from google import genai
from google.genai import types
import env
from pydub import AudioSegment

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
    audio_file = gemini.files.upload(file=mono_audio)
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
                    - any other relevant information (if any)
                
                Don't give intermediate steps or your descibing, give me only required content.
            """),
        contents=text
        )
        print(response.text)
        # clean the response to get only the json part
        # clean_json_str = response.text.strip('```json')

        # data = json.loads(clean_json_str)
        # print(data)
        # return data[0]
        return response.text
    except Exception as e:
        print(e)
        return None
