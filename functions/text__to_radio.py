import json
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import os
import logging
from pyttsx3 import init as pyttsx3_init
from pydub.utils import make_chunks

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
        # Read JSON
        with open(json_file_path, 'r',encoding="utf-8") as file:
            data = json.load(file) 
        filetesst = AudioSegment.from_file("C:/Users/pc/toolPy/file_1.mp4")
        audio_segments = []
        
        # Process each subtitle
        for index,item in enumerate(data['body']):
            audio = convert_text_to_audio(item['content'])
            
            # audio_segments.append(audio)
            start_time = int(float(item['from']) * 1000 )
            end = int(float(item['to']) * 1000 )
            # totalDurationSentence= (end-start_time)
            datasound=filetesst[start_time:end]
            # if item["music"] > 0:
            #     print(item["music"])
            #     silence = AudioSegment.silent(duration=item["music"]*1000)
            #     # audio_segments.append(silence)
            # if totalDurationSentence > len(audio):
            #     silence = AudioSegment.silent(duration=(end-start_time) - len(audio))
            #     # print(f"durations: {end-start_time} timesSentence:{len(audio)},{len(silence)}")
            #     audio_segments.append(silence)
            #     audio_segments.append(audio)
            # elif totalDurationSentence < len(audio): 
            #          sliceAudio=audio[0:len(audio)]
            #         #  print(len(sliceAudio),len(audio))
            #          audio_segments.append(sliceAudio)   
            datasound.export(f"C:/Users/pc/toolPy/functions/AUDIOVIET/{index}.mp3", format="mp3")
            
       
        # Combine and export
        final_audio = sum(audio_segments)
        # final_audio.export(f"C:/Users/pc/toolPy/functions/audio/final.mp3", format="mp3")
        # return output_file
        
    except Exception as e:
        logging.error(f"Error converting to audio: {e}")
        raise

convert_json_to_audio("C:/Users/pc/toolPy/functions/subtitles.json", output_file="output.mp3")    
# C:/Users/pc/toolPy/file_1.mp4
# C:/Users/pc/toolPy/functions/subtitlesViet.json
# lengthAudio = AudioSegment.from_file("C:/Users/pc/toolPy/file_1.mp4")        
# print(len(lengthAudio))
#  223376 ban goc
# 227450 final tieng trung


    