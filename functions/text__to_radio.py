import json
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import os
import logging
from pyttsx3 import init as pyttsx3_init
from user_path import userPath, proxy_path, ffmpge_path
import sys
sys.path.append(userPath)
import image__to__text as image__to__text
from moviepy import TextClip, VideoFileClip, CompositeVideoClip


fontsize = 50
color = "white"
bg_color = "black"
font = "C:/Users/pc/toolPy/tahoma.ttf"  # Path to your .ttf font file


_path = os.path.dirname(os.path.abspath("functions"))
video_text_clips = "video_text_clips.mp4"

video_path = f"{_path}/file_0.mp4"
ffmpeg_cuda_path = ffmpge_path

def change_audio_speed(audio, speed_factor=1.3):
    return audio.speedup(playback_speed=speed_factor)
# CREATE TEXT CLIPS
def create_video_text_clips(text):
    text_clip = TextClip(
            text=text["content"],
            font_size=fontsize,
            color=color,
            font=font,
            bg_color=bg_color,
            size=(640, 100),
            duration=2
        ).with_start(text["from"]).with_end(text["to"])
    return text_clip

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
def convert_json_to_audio(json_file_path, output_file="output.mp3"):
    try:
        framHaveText = image__to__text.handle_timestamp()
        with open(json_file_path, 'r', encoding="utf-8") as file:
            data = json.load(file)

        audio_segments = []
        lenaudio_segments = 0
        last_ojbText = []
        repeat_text = []    
        index = 0
        video_text_clips = []

        for i in range(0, len(framHaveText) - 1, 2):  # Ensure index is within bounds
            if i + 1 >= len(framHaveText):
                break  # Prevent out-of-range access

            silence_start = framHaveText[i]["timestamp"]
            silence_end = framHaveText[i + 1]["timestamp"]
            data_text_performent = text_performent(data, silence_start, silence_end)
            if i > 0:
                repeat_text =  [item for item in data_text_performent if item in last_ojbText]
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
                    _text = create_video_text_clips(ts)
                    video_text_clips.append(_text)
                    
                    audio = convert_text_to_audio(ts["content"])
                    index += 1
                  
                    if len(audio) > 100 :
                        audio_segments.append(audio)
                        lenaudio_segments += len(audio)
                        
                

        # Export the video
        final_video = CompositeVideoClip(video_text_clips)

        final_video.write_videofile(video_text_clips, fps=30, codec="libx264")
        final_audio = sum(audio_segments, AudioSegment.silent(duration=0))
        final_audio.export(output_file, format="mp3")
        return output_file
    except Exception as e:
        logging.error(f"Error converting to audio: {e}")
        raise

convert_json_to_audio("C:/Users/pc/toolPy/functions/subtitlesViet.json")
