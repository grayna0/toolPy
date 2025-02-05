
# COVER IMAGE TO TEXT BY PYTESSERACT


from PIL import ImageFilter
from PIL import Image,ImageDraw
from moviepy import VideoFileClip, TextClip, CompositeVideoClip,ImageClip
import numpy as np
import cv2
import easyocr
import concurrent.futures
from tqdm import tqdm
from functools import lru_cache
from multiprocessing import Pool, cpu_count
import torch
import gc
import os
from user_path import userPath ,path_video

_path = os.path.dirname(os.path.abspath("functions"))
video_path = f"{path_video}/file_1.mp4"

# Cache EasyOCR reader instance
@lru_cache(maxsize=1)
def get_reader():
    return easyocr.Reader(['ch_tra'], gpu=True)

def clear_gpu_memory():
    torch.cuda.empty_cache()
    gc.collect()
    
    
# crop image width=100 and height=65

def crop__image_fromVideo(video_path, interval=0.5):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval)  # Lấy frame mỗi 'interval' giây
    timestampArr = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:  # Chỉ xử lý frame theo interval
            timestamp = round(frame_count / fps, 2)
            timestampArr.append(timestamp)

            # Crop vùng cần thiết
            img_h, img_w = frame.shape[:2]
            half_width = img_w // 2
            crop = frame[img_h - 80:img_h - 15, half_width - 50: half_width + 50]
            
            output_path = f"{_path}/functions/AUDIOVIET/frame_{timestamp}.png"
            cv2.imwrite(output_path, crop)

        frame_count += 1

    cap.release()
    return timestampArr

def check_text_in_frames():
    clear_gpu_memory()
    reader = get_reader()
    timestampData = crop__image_fromVideo(video_path)
    results = []

    try:
        for timestamp in tqdm(timestampData):
            frame_path = f"{_path}/functions/AUDIOVIET/frame_{timestamp}.png"
            
            # Read image as numpy array
            frame = cv2.imread(frame_path)
            if frame is None:
                continue
                
            # Process image
            text_results = reader.readtext(frame_path,batch_size=8,detail=0)
            # if text_results:
            #     x_min, y_min = text_results[0][0][0][0], text_results[0][0][0][1]
            #     x_max, y_max = text_results[0][0][2][0], text_results[0][0][2][1]
            #     text_final=crop_image_again(x_min, y_min, x_max, y_max,frame_path)
            results.append({
                    'timestamp': timestamp,
                    'text': text_results
                })
            
             
            # Clear GPU memory periodically
            if len(results) % 10 == 0:
                clear_gpu_memory()
        print(results)
    except Exception as e:
        print(f"Error processing frames: {e}")
        
    return results
def removeImage():
    for filename in os.listdir(_path+"/functions/AUDIOVIET"):
        if filename.endswith(".png"):
            os.remove(os.path.join(_path+"/functions/AUDIOVIET", filename))
   
def handle_timestamp():
    results = check_text_in_frames()
    filtered_results = []
    for index ,frame in enumerate(results[:-1]):
        
        next_text = results[index + 1]["text"] 
        
        if len(frame["text"]) > 0 and len(next_text) == 0  :
            filtered_results.append(frame)
        if len(frame["text"]) == 0  and len(next_text) > 0:
            filtered_results.append(results[index + 1])
    # for i, frame in enumerate(results[:-1]):  # Duyệt qua các frame trừ frame cuối
    #     next_text = results[i + 1]["text"]
    #     if frame["text"] != "" and next_text == "" or []:  # Text biến mất
    #         filtered_results.append(frame)
    #     elif frame["text"] == "" or [] and next_text != "":  # Text xuất hiện
    #         filtered_results.append(results[i + 1])
       

    # removeImage()
    return filtered_results
def handle_video_processing():
    try:
        results = handle_timestamp()
        for result in results:
            print(result["timestamp"], result["text"])
    except Exception as e:
        print(f"Error in processing video: {e}")
    finally:
        print(11)
        # removeImage()  # Đảm bảo xóa ảnh tạm dù xảy ra lỗi

