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
def text_performent(data,silence_start,silence_end):
    relevant_timestamps = [
        item for item in data["body"]
        if silence_end >= item["from"] and  item["from"] >= silence_start
        ]
    inside_timestamps = [
        item for item in data["body"]
        if silence_end <= item["to"] and  item["from"] <= silence_start
        ]
  
    if  relevant_timestamps :
        return relevant_timestamps
    elif  relevant_timestamps == [] and inside_timestamps:
        return inside_timestamps
  
    
def convert_json_to_audio(json_file_path, output_file="output.mp3"):
    try:
        # Load timestamp
        framHaveText = image__to__text.handle_timestamp()
      
        # Read JSON
        with open(json_file_path, 'r', encoding="utf-8") as file:
            data = json.load(file)
        
        audio_segments = []
        lenaudio_segments = 0  # Tổng thời lượng audio đã xử lý
        last_ojbText = []
        repeat_text=[]
        # Xử lý các timestamp
        for i in range(0, len(framHaveText), 2):
            # Lấy khoảng silence
            silence_start = framHaveText[i]["timestamp"]
            silence_end = framHaveText[i + 1]["timestamp"]
            
            # Tìm các đoạn text trong khoảng này
            data_text_performent = text_performent(data, silence_start, silence_end)
            if i >0 :
                repeat_text = [item for item in data_text_performent if item["from"] == last_ojbText[0]["from"]]
            last_ojbText = data_text_performent
            if data_text_performent and repeat_text == []:
                 # Tính khoảng silence trước mỗi đoạn thoại
                if silence_start * 1000 > lenaudio_segments:
                    silence_duration = max(0, int((silence_start * 1000 - lenaudio_segments) ))
                    silence = AudioSegment.silent(duration=silence_duration)
                    audio_segments.append(silence)
                    lenaudio_segments += silence_duration  
                elif silence_start * 1000 < lenaudio_segments:
                    silence = AudioSegment.silent(duration=0)
                    audio_segments.append(silence)    
                for ts in data_text_performent:
                    # Chuyển đổi text thành audio
                    audio = convert_text_to_audio(ts["content"])
                    
                    # Kiểm tra và điều chỉnh tốc độ nếu cần
                    if len(audio) > 100 :
                        audio_segments.append(audio)
                        lenaudio_segments += len(audio)
                        
                

        # Kết hợp và xuất audio
        final_audio = sum(audio_segments, AudioSegment.silent(duration=0))
        final_audio.export(output_file, format="mp3")
        return output_file
    
    except Exception as e:
        logging.error(f"Error converting to audio: {e}")
        raise

convert_json_to_audio("C:/Users/pc/toolPy/functions/subtitlesViet.json", output_file="output.mp3")    



    