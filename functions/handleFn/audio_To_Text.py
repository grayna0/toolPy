
import whisper 

      
model = whisper.load_model("large")  # Hoặc 'tiny', 'small', 'medium', 'large'
result = model.transcribe("C:/Users/pc/toolPy/functions/AUDIOVIET/0.mp3")
print(result["text"])