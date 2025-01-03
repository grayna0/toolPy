from gtts import gTTS
import json
import os
from pydub import AudioSegment

def text_to_audio(json_data, output_dir="audio_files"):
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Parse JSON if string
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
            
        # Process each subtitle
        audio_segments = []
        for item in data['body']:
            # Create audio from text
            tts = gTTS(text=item['content'], lang='vie')
            temp_file = f"{output_dir}/temp_{item['sid']}.mp3"
            tts.save(temp_file)
            
            # Load audio segment
            audio = AudioSegment.from_mp3(temp_file)
            
            # Calculate duration and silence
            start_time = int(item['from'] * 1000)  # Convert to milliseconds
            end_time = int(item['to'] * 1000)
            
            # Add silence if needed
            if start_time > len(audio_segments):
                silence = AudioSegment.silent(duration=start_time - len(audio_segments))
                audio_segments.append(silence)
            
            # Add audio
            audio_segments.append(audio)
            
            # Cleanup temp file
            os.remove(temp_file)
        
        # Combine all segments
        final_audio = sum(audio_segments)
        final_audio.export(f"{output_dir}/final_audio.mp3", format="mp3")
        
        return f"{output_dir}/final_audio.mp3"
        
    except Exception as e:
        print(f"Error converting text to audio: {str(e)}")
        return None

# Usage example
if __name__ == "__main__":
    with open("subtitles.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    output_file = text_to_audio(json_data)
    print(f"Audio saved to: {output_file}")