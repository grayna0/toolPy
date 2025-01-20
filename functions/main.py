import tkinter as tk
from tkinter import ttk
import Get_Sub_bilibili
import downloadVideo
import sys
sys.path.append("C:/Users/pc/toolPy/functions")
import image__to__text as image__to__text
import text__to_radio as text__to_radio
import os


_path = os.path.dirname(os.path.abspath("functions"))

def translateFn():
    print("translatsse")
class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tool reup")
        self.root.geometry("400x300")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Input fields
        ttk.Label(main_frame, text="Video URL:").grid(row=0, column=0, sticky=tk.W)
        self.url_input = ttk.Entry(main_frame, width=40)
        self.url_input.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(main_frame, text="authen-key:").grid(row=1, column=0, sticky=tk.W)
        self.key_input = ttk.Entry(main_frame, width=40)
        self.key_input.grid(row=1, column=1, padx=5, pady=5)
        
        # Button
        ttk.Button(main_frame, text="Translate", 
                  command=self.start_translation).grid(row=2, column=1, pady=20)
      
    def start_translation(self):
        authen__key = self.key_input.get()
        url = self.url_input.get()
        # Add translation logic here
        downloadVideo.downloadAudio(url)
        Get_Sub_bilibili.getSub(api_url=authen__key,video_id=url)
        # text__to_radio.convert_json_to_audio(f"{_path}/functions/subtitlesViet.json", output_file="output.mp3")     
def main():
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()