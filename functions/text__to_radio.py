import json
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import os
import logging
from pyttsx3 import init as pyttsx3_init
import sys
sys.path.append("C:/Users/pc/toolPy/functions")
import image__to__text as image__to__text
from moviepy import TextClip,VideoFileClip,CompositeVideoClip

_path = os.path.dirname(os.path.abspath("functions"))
video_path= f"{_path}/file_0.mp4"

# Đường dẫn FFmpeg hỗ trợ CUDA
ffmpeg_cuda_path = "D:/ffmpeg-2024-12-23-git-6c9218d748-full_build/bin/ffmpeg"
def add_and_blur_text(data_text,start,end,index):
    # video_short= video[start:end]
    video_p= f"{_path}/file_{index}.mp4"
    video = VideoFileClip(video_p)
    text = TextClip(text=data_text,
    font="tahoma.ttf",
    font_size=20,
    color='black',
    bg_color="white",
    duration=end-start,
    size=(video.size[0], None)).with_start(start).with_position("bottom")
    return CompositeVideoClip([video, text])

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
        
        os.remove(temp_file)
        return audio
    # Read JSON
    
    
def text_performent(data,silence_start,silence_end):
    # front_timestamps = [item for item in data["body"]
    #     if silence_end <= item["to"] and  item["from"] >= silence_start]
    # front_relevant_timestamps = [
    #     item for item in data["body"]
    #     if silence_end >= item["to"] and  item["from"] >= silence_start
    #     ]
    # inside_timestamps = [
    #     item for item in data["body"]
    #     if silence_end <= item["to"] and  item["from"] <= silence_start
    #     ]
    # behide_timestamps = [
    #     item for item in data["body"]
    #     if silence_end >= item["to"] and  item["to"] >= silence_start
    #     ]
    # relevant_timestamps = [
    #     item for item in data["body"]
    #     if silence_end >= item["from"] and  item["from"] >= silence_start
    #     ]
    # inside_timestamps = [
    #     item for item in data["body"]
    #     if silence_end <= item["to"] and  item["from"] <= silence_start
    #     ]

    # if  relevant_timestamps :
    #     return relevant_timestamps
    # elif  relevant_timestamps == [] and inside_timestamps:
    #     return inside_timestamps
    arr=[]
    for item in data["body"]  :
        if item["from"] >= silence_start :
            if item["to"]   >= silence_end:
                      arr.append(item)
            elif item["to"]   <= silence_end:
                     arr.append(item)
        elif item["from"] <= silence_start :
            if item["to"]   >= silence_end:
                      arr.append(item)
            if item["to"]   <= silence_end:
                    arr.append(item)
    return arr
  
    
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
        video_segments = []
        index=0
        # Xử lý các timestamp
        for i in range(0, len(framHaveText), 2):
            # Lấy khoảng silence
            silence_start = framHaveText[i]["timestamp"]
            silence_end = framHaveText[i + 1]["timestamp"]
            
            # Tìm các đoạn text trong khoảng này
            data_text_performent = text_performent(data, silence_start, silence_end)
            if i >0 :
                repeat_text = [item for item in data_text_performent if item["from"] == last_ojbText[0]["from"]]
                if repeat_text:
                    continue
            last_ojbText = data_text_performent
            if data_text_performent :
                #  Tính khoảng silence trước mỗi đoạn thoại
                if silence_start * 1000 > lenaudio_segments:
                    silence_duration = max(0, int((silence_start * 1000 - lenaudio_segments) ))
                    silence = AudioSegment.silent(duration=silence_duration)
                    audio_segments.append(silence)
                    lenaudio_segments += silence_duration
              
                elif silence_start * 1000 < lenaudio_segments:
                    silence = AudioSegment.silent(duration=0)
                    audio_segments.append(silence)    
                for ts in data_text_performent:
            
                    audio = convert_text_to_audio(ts["content"])
                    index += 1
                  
                    if len(audio) > 100 :
                        audio_segments.append(audio)
                        lenaudio_segments += len(audio)
                        
                

        # Kết hợp và xuất audio
        final_audio = sum(audio_segments, AudioSegment.silent(duration=0))
        
        final_audio.export(output_file, format="mp3")
                # Kết hợp video

        
        return output_file
    
    except Exception as e:
        logging.error(f"Error converting to audio: {e}")
        raise

convert_json_to_audio("C:/Users/pc/toolPy/functions/subtitlesViet.json")


    