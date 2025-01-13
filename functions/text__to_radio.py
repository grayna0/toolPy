import json
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import os
import logging
from pyttsx3 import init as pyttsx3_init
import sys
sys.path.append("C:/Users/pc/toolPy/functions/handleFn")
import handleFn.image__to__text as image__to__text
def convert_text_to_audio(text, lang='vi',speed=200):
    try:
        # Primary method - pyttsx3
        engine = pyttsx3_init()
        engine.setProperty('rate', speed) 
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
        if speed != 150:
            speed_change = speed / 150.0  # Calculate ratio
            audio = audio.speedup(playback_speed=speed_change)
        os.remove(temp_file)
        return audio
    # Read JSON
def convert_json_to_audio(json_file_path, output_file="output.mp3"):
    try:
        # load timestamp
        framHaveText = image__to__text.handle_timestamp()
      
        # Read JSON
        with open(json_file_path, 'r',encoding="utf-8") as file:
            data = json.load(file) 
        audio_segments = []
        # chuyển đổi text to audio và xử lý những timestamp không có lời
        for i in range(0, len(framHaveText), 2):
            # Lấy khoảng silence
            silence_start = framHaveText[i]["timestamp"] 
            silence_end = framHaveText[i + 1]["timestamp"]
             # Process each subtitle
                # Tìm các đoạn trong timestamps thuộc khoảng này
            
            relevant_timestamps = [
                item for item in data["body"]
                if silence_end >= item["from"] and  item["from"] >= silence_start
                ]
            print("relevant_timestamps",relevant_timestamps)
            if i == 0 :
                silence_duration = int((silence_start) * 1000 )  # Chuyển sang ms
                print("im lang 1",silence_duration)
                silence = AudioSegment.silent(duration=silence_duration)
                audio_segments.append(silence)
            else:
                if len(audio_segments) < framHaveText[i - 1]["timestamp"]:
                    
                    silence_duration = int((silence_start - framHaveText[i - 1]["timestamp"]) * 1000 )
                # else :
                    # silence_duration = int((silence_start - len(audio_segments)) * 1000 )
                    # Chuyển sang ms
                silence = AudioSegment.silent(duration=silence_duration)
                audio_segments.append(silence)
            if relevant_timestamps:
                for ts in relevant_timestamps:
                    audio = convert_text_to_audio(ts["content"])
                    audio_segments.append(audio)

                    
            
        # Combine and export
        final_audio = sum(audio_segments)
        final_audio.export(f"C:/Users/pc/toolPy/functions/audio/final.mp3", format="mp3")
        return output_file
        
    except Exception as e:
        logging.error(f"Error converting to audio: {e}")
        raise

convert_json_to_audio("C:/Users/pc/toolPy/functions/subtitlesViet.json", output_file="output.mp3")    
# C:/Users/pc/toolPy/file_1.mp4
# C:/Users/pc/toolPy/functions/subtitlesViet.json
# lengthAudio = AudioSegment.from_file("C:/Users/pc/toolPy/file_1.mp4")        
# print(len(lengthAudio))
#  223376 ban goc
# 227450 final tieng trung


    