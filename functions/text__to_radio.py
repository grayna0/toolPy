import json
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import os
import logging
from pyttsx3 import init as pyttsx3_init

def convert_text_to_audio(text, lang='vi'):
    """Convert text to audio using multiple engines"""
    try:
        # Primary method - pyttsx3
        engine = pyttsx3_init()
        engine.setProperty('rate', 250.0) 
        temp_file = "temp_speech.mp3"
        engine.save_to_file(text, temp_file)
        engine.runAndWait()
        
        audio = AudioSegment.from_mp3(temp_file)
        os.remove(temp_file)
        return audio
    except:
        # Fallback to gTTS
        tts = gTTS(text=text, lang=lang)
        tts.save(temp_file)
        audio = AudioSegment.from_mp3(temp_file)
        os.remove(temp_file)
        return audio
    # Read JSON
def convert_json_to_audio(json_file_path, output_file="output.mp3"):
    try:
        # Read JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file) 
        
        audio_segments = []
        
        # Process each subtitle
        for item in data['body']:
            audio = convert_text_to_audio(item['content'])
            # start_time = int(float(item['from']) / 60 )
            # end = int(float(item['to']) / 60 )
            # # final_audio = AudioSegment.silent(duration=end-start_time)
            # # Add silence if needed
            # if start_time > len(audio_segments):
            #     silence = AudioSegment.silent(duration=start_time - len(audio_segments))
            #     audio_segments.append(silence)
            
            audio_segments.append(audio)
       
        # Combine and export
        final_audio = sum(audio_segments)
        final_audio.export(output_file, format="mp3")
        return output_file
        
    except Exception as e:
        logging.error(f"Error converting to audio: {e}")
        raise

convert_json_to_audio("C:/Users/pc/toolPy/functions/subtitlesViet.json", output_file="output.mp3")    
