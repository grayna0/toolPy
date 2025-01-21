
# import whisper 

      
# model = whisper.load_model("large")  # Hoặc 'tiny', 'small', 'medium', 'large'
# result = model.transcribe("C:/Users/pc/toolPy/functions/AUDIOVIET/0.mp3")
# print(result["text"])
from moviepy import TextClip,VideoFileClip,CompositeVideoClip
video_path= "C:/Users/pc/toolPy/result2.mp4"
# Đường dẫn FFmpeg hỗ trợ CUDA
ffmpeg_cuda_path = "D:/ffmpeg-2024-12-23-git-6c9218d748-full_build/bin/ffmpeg"
def add_and_blur_text(data_text,start,end):
    video = VideoFileClip(video_path)
    text = TextClip(text=data_text,
    font="tahoma.ttf",
    font_size=20,
    color='black',
    bg_color="white",
    duration=end-start,
    size=(video.size[0] - 300, None)).with_start(start).with_position("bottom")
    final =CompositeVideoClip([video, text])
    final.write_videofile("result3.mp4", codec="h264_nvenc", fps=video.fps, remove_temp=True,
        ffmpeg_params=[
            "-preset", "fast",  # Tùy chỉnh hiệu suất CUDA
            "-b:v", "6000k"  # Bitrate video
        ])
    video.close()
add_and_blur_text("data_text",60,70)