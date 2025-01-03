
# COVER IMAGE TO TEXT BY PYTESSERACT


import pytesseract
from PIL import ImageFilter
from PIL import Image,ImageDraw
from moviepy import VideoFileClip, TextClip, CompositeVideoClip,concatenate_videoclips,ImageClip
import numpy as np


video = VideoFileClip("video(online-video-cutter.com).mp4")
frames = []
for frame in video.iter_frames():
    frames.append(Image.fromarray(frame))

# Initialize Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'

# Load image
image = Image.open("test.png")

# Convert to grayscale
gray_image = image.convert('L')

# Convert to binary black and white using threshold
threshold = 128  # Adjust this value between 0-255 to change the threshold
binary_image = gray_image.point(lambda x: 0 if x < threshold else 255, '1')

# Save the result
binary_image.save("bw_test.png")

# For OCR
text = pytesseract.image_to_string(binary_image, lang='chi_tra')

for frame in frames:
    text = pytesseract.image_to_string(frame,lang='eng')
    if text.strip():
        frame = frame.filter(ImageFilter.BLUR)  # Example: Apply blur to remove text
for i in range(len(frames)):
    frame = frames[i]
    text_img = Image.new('RGBA', frame.size, (255, 255, 255, 225))
    draw = ImageDraw.Draw(text_img)
    draw.text((10, 10), "New Text", fill=(255, 255, 255, 225))
    combined = Image.alpha_composite(frame.convert('RGBA'), text_img)
    frames[i] = combined
fps=video.fps
final_clips = [ImageClip(np.array(frame)).with_duration(1.0 / fps) for frame in frames]
final_video = concatenate_videoclips(final_clips,method="chain")
final_video.write_videofile("output_video_with_replaced_text.mp4", fps=fps)