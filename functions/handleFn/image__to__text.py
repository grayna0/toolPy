
# COVER IMAGE TO TEXT BY PYTESSERACT


from PIL import ImageFilter
from PIL import Image,ImageDraw
from moviepy import VideoFileClip, TextClip, CompositeVideoClip,concatenate_videoclips,ImageClip
import numpy as np
import cv2
import easyocr
import concurrent.futures
from tqdm import tqdm
from functools import lru_cache
import multiprocessing
import torch
import gc
video_path = "C:/Users/pc/toolPy/file_0.mp4"

# Cache EasyOCR reader instance
@lru_cache(maxsize=1)
def get_reader():
    return easyocr.Reader(['ch_tra'], gpu=True)

def clear_gpu_memory():
    torch.cuda.empty_cache()
    gc.collect()

def process_image_batch(img_paths, batch_size=4):  # Reduced batch size
    reader = get_reader()
    results = []
    
    try:
        for batch in tqdm(np.array_split(img_paths, len(img_paths)//batch_size + 1)):
            # Monitor GPU memory
            if torch.cuda.is_available():
                memory_allocated = torch.cuda.memory_allocated(0) / 1024**2
                if memory_allocated > 8000:  # 4GB threshold
                    clear_gpu_memory()
            
            batch_results = reader.readtext(list(batch), detail=0)
            results.extend(batch_results)
            
            # Clear memory after each batch
            clear_gpu_memory()
            
    except RuntimeError as e:
        if "out of memory" in str(e):
            clear_gpu_memory()
            # Retry with smaller batch
            return process_image_batch(img_paths, batch_size=batch_size//2)
        raise e
        
    return results

def crop__image_fromVideo(video_path):
    # Open video file
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    timestampArr =[]
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Get current frame position
        frame_pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
        # Calculate timestamp in seconds
        timestamp = round(frame_pos / fps,2)
        int_timestamp = int(timestamp)
        if isinstance(int_timestamp,int)  :
            timestampArr.append(timestamp)
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            img_width= pil_image.size[0]
            img_hight= pil_image.size[1]
            half_width = int(img_width/2)
            crop = frame[img_hight-50:img_hight, half_width - 50: half_width + 50]
            
            output_path = f"C:/Users/pc/toolPy/functions/AUDIOVIET/frame_{timestamp}.png"
            cv2.imwrite(output_path, crop)
    return timestampArr
        
def check_text_in_frames():
    clear_gpu_memory()
    reader = get_reader()
    timestampData = crop__image_fromVideo(video_path)
    results = []

    try:
        for timestamp in tqdm(timestampData):
            frame_path = f"C:/Users/pc/toolPy/functions/AUDIOVIET/frame_{timestamp}.png"
            
            # Read image as numpy array
            frame = cv2.imread(frame_path)
            if frame is None:
                continue
                
            # Process image
            text_results = reader.readtext(frame,detail=0,batch_size=8)
            if text_results:
                if not results or text_results != results[-1]["text"]:
                 results.append({
                     'timestamp': timestamp,
                     'text': text_results
                 })
             
            
            # Clear GPU memory periodically
            if len(results) % 10 == 0:
                clear_gpu_memory()
    
    except Exception as e:
        print(f"Error processing frames: {e}")
        
    return results
if __name__ == '__main__':
    results = check_text_in_frames()
    valid_results = [r for r in results if r['text']]
    print(results)
    print(f"Found text in {len(valid_results)} frames")
