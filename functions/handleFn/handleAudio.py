import wave
import json
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

import os

def convert_mp3_to_wav(input_path, output_path):
    try:
        # Load audio file
        audio = AudioSegment.from_file(input_path)
        
        # Export as WAV
        audio.export(output_path, format="wav")
        return True
    except Exception as e:
        print(f"Error converting file: {e}")
        return False
# # Tải mô hình Vosk (tải mô hình từ https://alphacephei.com/vosk/models và giải nén vào thư mục)
model = Model("D:/vosk-model-cn-kaldi-multicn-0.15")
def sliceAudioHaveText(json_file_path):
    
    #  open json Sub chinese
    with open(json_file_path, 'r',encoding="utf-8") as file:
            data = json.load(file) 
    # open audio origin file          
    filetesst = AudioSegment.from_file("C:/Users/pc/toolPy/file_1.mp4")
    # find audio source have text and slice it
    for index,item in enumerate(data['body']):
        # Mở tệp âm thanh
        wf = wave.open(f"C:/Users/pc/toolPy/functions/AUDIOVIET/{index}.wav", "rb")
        # filetesst = AudioSegment.from_file(f"C:/Users/pc/toolPy/functions/AUDIOVIET/{index}.mp3")
        # Khởi tạo recognizer
        recognizer = KaldiRecognizer(model, wf.getframerate())
        #  Đọc dữ liệu âm thanh và chuyển đổi thành văn bản
        results = []
        while True:
            datas = wf.readframes(10)
            print(datas)
            if len(datas) == 0:
                break
            if recognizer.AcceptWaveform(datas):
                result = recognizer.Result()
                results.append(json.loads(result))
        # # Kết quả cuối cùng
        final_result = recognizer.FinalResult()
        results.append(json.loads(final_result))    
     # In ra văn bản chuyển đổi
    for result in results:
        print(result.get("text", ""))   
sliceAudioHaveText("C:/Users/pc/toolPy/functions/subtitles.json")        