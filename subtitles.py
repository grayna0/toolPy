from pydub import AudioSegment
import os
from pyttsx3 import init as pyttsx3_init
from gtts import gTTS
 # Primary method - pyttsx3
 
arr1 =[{"tiem":1,"text":"hllee"},{"tiem":2,"text":"hllee"},{"tiem":3,"text":"hllee"}]
arr2 =[{"tiem":1,"text":"hllee"},{"tiem":4,"text":"hllee"},{"tiem":5,"text":"hllee"}]
repeat_text = [item for item in arr1 if int(item["tiem"]) == int(arr2[0]["tiem"])]
print(repeat_text)
# def convert_text_to_audio(text, lang='vi',speed=300):
#         # Primary method - pyttsx3
#         engine = pyttsx3_init()
#         engine.setProperty('rate', speed/150) 
#         temp_file = "temp_speech.mp3"
#         engine.save_to_file(text, temp_file)
#         engine.runAndWait()
        
#         tts = gTTS(text=text, lang=lang)
#         tts.save(temp_file)
#         audio = AudioSegment.from_mp3(temp_file)
#         return audio
    
# convert_text_to_audio("Pháp Nam Minh")