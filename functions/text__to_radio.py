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
        framHaveText = image__to__text.check_text_in_frames()
        timestampArray = []
        for index , i in enumerate(framHaveText):
            
            if i["text"] != framHaveText[index -1]["text"] :
               timestampArray.append(i) 
        # Read JSON
        print(timestampArray)
        with open(json_file_path, 'r',encoding="utf-8") as file:
            data = json.load(file) 
        audio_segments = []
        # chuyển đổi text to audio và xử lý những timestamp không có lời
        for index,item in enumerate(timestampArray):
            wrap__from =int(float(timestampArray[index]["timestamp"]) *1000)
            wrap__to =int(float(timestampArray[index + 1]["timestamp"]) *1000)
        # Process each subtitle
            for id,item in enumerate(data['body']):
                start_time = int(float(item['from']) * 1000 )
                
                end = int(float(item['to']) * 1000 )
                
                audio = convert_text_to_audio(item['content'])
                
                from__text =int(timestampArray[index]["timestamp"])
                
                checkWrap =wrap__from >= end and end <= wrap__to
                if  checkWrap:
            
                    audio_segments.append(audio)
                else:
                    silence = AudioSegment.silent(duration=wrap__to  - len(audio_segments))
                    audio_segments.append(silence) 
                    
            
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


    