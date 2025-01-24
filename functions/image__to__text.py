
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
import write_sub_to_json
_path = os.path.dirname(os.path.abspath("functions"))
video_path = f"C:/Users/pc/toolPy/file_0.mp4"
print(video_path)

# Cache EasyOCR reader instance
@lru_cache(maxsize=1)
def get_reader():
    return easyocr.Reader(['ch_tra'], gpu=True)

def clear_gpu_memory():
    torch.cuda.empty_cache()
    gc.collect()

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
# ################################
# def process_frame_with_retry(frame_path, retries=3):
#     reader = get_reader()
#     for attempt in range(retries):
#         try:
#             frame = cv2.imread(frame_path)
#             if frame is None:
#                 return None
#             return reader.readtext(frame, detail=0)
#         except Exception as e:
#             print(f"Retry {attempt + 1} for {frame_path} due to error: {e}")
#             clear_gpu_memory()
#     return None  # Trả về None nếu hết retry

# def process_frames_parallel(timestampArr):
#     frame_paths = [f"{_path}/functions/AUDIOVIET/frame_{ts}.png" for ts in timestampArr]
#     with Pool(cpu_count()) as pool:
#         results = list(tqdm(pool.imap(process_frame_with_retry, frame_paths), total=len(frame_paths)))

#     processed_results = []
#     for i, text_result in enumerate(results):
#         if text_result:
#             processed_results.append({'timestamp': timestampArr[i], 'text': text_result})
#     return processed_results

# ################################

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
            text_results = reader.readtext(frame,detail=0,batch_size=8)
          
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
def removeImage():
    for filename in os.listdir(_path+"/functions/AUDIOVIET"):
        if filename.endswith(".png"):
            os.remove(os.path.join(_path+"/functions/AUDIOVIET", filename))
   
def handle_timestamp():
    results = check_text_in_frames()
    filtered_results = []
    # for index ,frame in enumerate(results -1):
        
    #     next_text = results[index + 1]["text"] 
        
    #     if len(frame["text"]) > 0 and len(next_text) == 0  :
    #         print("none",frame)
    #         filtered_results.append(frame)
    #     if len(frame["text"]) == 0  and len(next_text) > 0:
    #         print("TẼTXT",frame)
            
    #         filtered_results.append(results[index + 1])
    for i, frame in enumerate(results[:-1]):  # Duyệt qua các frame trừ frame cuối
        next_text = results[i + 1]["text"]
        if frame["text"] != "" and next_text == "" or []:  # Text biến mất
            filtered_results.append(frame)
        elif frame["text"] == "" or [] and next_text != "":  # Text xuất hiện
            filtered_results.append(results[i + 1])
       

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

result = handle_video_processing()
