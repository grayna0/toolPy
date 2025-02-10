import json
from gtts import gTTS
from pydub import AudioSegment
import os
import logging
from pyttsx3 import init as pyttsx3_init
import ast
from user_path import userPath, proxy_path, ffmpge_path
import sys
sys.path.append(userPath)
import image__to__text as image__to__text
fontsize = 20
color = "white"
bg_color = "black"
font = "C:/Users/pc/toolPy/tahoma.ttf"  # Path to your .ttf font file


_path = os.path.dirname(os.path.abspath("functions"))
video_path = f"{_path}/file_0.mp4"
ffmpeg_cuda_path = ffmpge_path
def change_audio_speed(audio, speed_factor=1.3):
    return audio.speedup(playback_speed=speed_factor)
# CREATE TEXT CLIPS
# CONVERT TEXT TO AUDIO WITH SPEED 1.3X
def convert_text_to_audio(text, lang='vi', speed=200):
    try:
        tts = gTTS(text=text, lang=lang)
        temp_file = "temp_speech.mp3"
        tts.save(temp_file)
        audio = AudioSegment.from_mp3(temp_file)
        os.remove(temp_file)
        speed_factor = speed / 150.0
        faster_audio = audio.speedup(playback_speed=speed_factor)
        return faster_audio
    except Exception as e:
        return None
last_dataT =[]
def text_performent(data, silence_start, silence_end):
    
    global last_dataT
    
    with open(f"{userPath}/subtitlesViet.json", 'r', encoding="utf-8") as file:
        data = json.load(file)
    data_remain = data["body"][len(last_dataT):]    
    front_relevant_timestamps = [
        item for item in data_remain
        if silence_end >= item["to"] and  item["from"] >= silence_start
        ]
    inside_timestamps = [
        item for item in data_remain
        if silence_end <= item["to"] and  item["from"] <= silence_start
        ]
    behide_timestamps = [
        item for item in data_remain
        if silence_end >= item["to"] and  item["to"] >= silence_start
        ]
    if  front_relevant_timestamps and behide_timestamps:
        if  front_relevant_timestamps[0]["from"] < behide_timestamps[0]["from"]:
            last_dataT= front_relevant_timestamps
            return front_relevant_timestamps
        elif  front_relevant_timestamps[0]["from"] > behide_timestamps[0]["from"]:
            last_dataT= behide_timestamps
            return behide_timestamps
    elif  front_relevant_timestamps or behide_timestamps :
        
        if  front_relevant_timestamps:
            last_dataT= front_relevant_timestamps
            return front_relevant_timestamps
        elif  behide_timestamps:
            last_dataT= behide_timestamps
            return behide_timestamps
    elif  front_relevant_timestamps == [] and behide_timestamps == [] and inside_timestamps:
            last_dataT= inside_timestamps
            return inside_timestamps
            
    else:
        return last_dataT
    # return last_dataT
def convert_json_to_audio( output_file="output.mp3"):
    try:
        with open("C:/Users/pc/toolPy/data_text_performent.txt", 'r+', encoding="utf-8") as file:
            content = file.read().strip()
            parsed_data = ast.literal_eval(content)
            print(type(parsed_data))
        audio_segments = []
        lenaudio_segments = 0
        index = 0
        
        for item in parsed_data:
          
            silence_start = item[0]["from"]
    


                #  Tính khoảng silence trước mỗi đoạn thoại
            if silence_start * 1000 > lenaudio_segments:
                silence_duration = max(0, int((silence_start * 1000 - lenaudio_segments) ))
                silence = AudioSegment.silent(duration=silence_duration)
                audio_segments.append(silence)
                lenaudio_segments += silence_duration
            elif silence_start * 1000 < lenaudio_segments:
                silence = AudioSegment.silent(duration=0)
                audio_segments.append(silence)    
            for ts in item:
            
                audio = convert_text_to_audio(ts["content"])
                index += 1
                if len(audio) > 100 :
                    audio_segments.append(audio)
                    lenaudio_segments += len(audio)


            # Export the video
            
        final_audio = sum(audio_segments, AudioSegment.silent(duration=0))
        final_audio.export(output_file, format="mp3")
        return output_file
    except Exception as e:
        logging.error(f"Error converting to audio: {e}")
        raise
convert_json_to_audio()
